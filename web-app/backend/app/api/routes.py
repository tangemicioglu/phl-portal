import uuid
from flask import (
    jsonify,
    request,
    redirect,
    send_from_directory,
    current_app,
    abort as fabort,
    make_response,
)
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.services import s3, fingering, chunking, evaluation
from app.database.models import Score, Recording
from werkzeug.utils import secure_filename
from music21 import musicxml, converter, midi
from sqlalchemy import or_
import os


@bp.route("/score", methods=["POST"])
@token_auth.login_required
def upload_score():
    # gather form data

    try:
        form_data = request.form.to_dict()
        title = form_data["title"]
        composer = form_data["composer"]
        file = request.files["file"]
        print("recieved score.")

        # generate fingerings and lessons for uploaded score
        annotated_score = fingering.generate_fingerings(file)
        print("fingerings generated.")
        lessons = chunking.generate_lessons(annotated_score)
        print("lessons created.")
        tactile_stimuli = chunking.generate_tactile_stimuli(annotated_score)
        print("tactile stimuli generated.")
        print(annotated_score)
        print("score annotated successfully!")

        # save annotated file to local filesystem or AWS S3 depending on environment
        annotated_score_binary = musicxml.m21ToXml.GeneralObjectExporter(
            annotated_score
        ).parse()

        print("score binary generated.")

        filename = secure_filename(file.filename)

        if os.environ["FLASK_ENV"] == "development":
            with open(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    "musicxml",
                    secure_filename(filename),
                ),
                "wb",
            ) as fp:
                fp.write(annotated_score_binary)
                fp.close()
        else:
            s3.upload_file(annotated_score_binary, secure_filename(filename))

        print("score saved to filesystem.")

        # add Score object to database
        score = Score(
            title=title,
            composer=composer,
            filename=filename,
            lessons=lessons,
            tactile_stimuli=tactile_stimuli,
            inDefaultCorpus=False,
            user_id=token_auth.current_user().id,
        )
        db.session.add(score)
        db.session.commit()

        print("score saved to database")
        return jsonify(score.to_dict())
    except Exception as e:
        abort(400, str(e))


@bp.route("/scores", methods=["GET"])
@token_auth.login_required
def get_scores():
    current_user_id = token_auth.current_user().id
    scores = Score.query.filter(
        or_(Score.user_id == current_user_id, Score.inDefaultCorpus == True)
    )
    # scores = Score.query.filter_by(user_id=token_auth.current_user().id).all()

    return jsonify([score.to_dict() for score in scores])


@bp.route("/score/<id>", methods=["GET"])
@token_auth.login_required
def get_score_file(id):
    score = Score.query.get_or_404(uuid.UUID(id))
    if os.environ["FLASK_ENV"] == "development":
        return send_from_directory(
            os.path.join(current_app.config["UPLOAD_FOLDER"], "musicxml"),
            score.filename,
            as_attachment=True,
        )
    else:
        return s3.get_presigned_url(score.filename)


@bp.route("/midi/<id>", methods=["GET"])
@token_auth.login_required
def get_midi_file(id):
    recording = Recording.query.get_or_404(uuid.UUID(id))
    if os.environ["FLASK_ENV"] == "development":
        return send_from_directory(
            os.path.join(current_app.config["UPLOAD_FOLDER"], "midi"),
            recording.filename,
            as_attachment=True,
        )
    else:
        return s3.get_presigned_url(recording.filename)


@bp.route("/score/<id>/midi", methods=["POST"])
@token_auth.login_required
def upload_midi(id):
    # Retrieve score XML
    try:
        score = Score.query.get_or_404(uuid.UUID(id))
        if os.environ["FLASK_ENV"] == "development":
            score_xml = os.path.join(
                current_app.config["UPLOAD_FOLDER"], "musicxml", score.filename
            )
            score_stream = converter.parse(score_xml)
        else:
            score_xml = s3.download_file(score.filename)
            score_stream = converter.parse(score_xml.read())

        # Convert score XML to MIDI
        score_midi = midi.translate.streamToMidiFile(score_stream)

        # Prepare recording for upload
        file = request.files["file"]
        filename = secure_filename(file.filename)

        # Convert recording MIDI to MidiFile object
        file_content = file.read()
        file_midi = midi.MidiFile()
        file_midi.readstr(file_content)

        # Evaluate the recording against the original score_midi
        match_cost, time_cost, percentage = evaluation.Evaluate(score_midi, file_midi)

        # Upload the file to S3 / Local folder
        file.seek(0)  # Set cursor to the start of the file
        if os.environ["FLASK_ENV"] == "development":
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        else:
            s3.upload_file(file, filename)

        recording = Recording(
            filename=filename,
            matching_score=match_cost,
            timing_score=time_cost,
            score_id=score.id,
            user_id=token_auth.current_user().id,
        )
        score.recordings.append(recording)
        db.session.commit()
        return jsonify(recording.to_dict())
    except Exception as e:
        abort(400, str(e))


def abort(status_code, message=""):
    response = make_response(f"{status_code}\n{message}")
    response.status_code = status_code
    fabort(response)
