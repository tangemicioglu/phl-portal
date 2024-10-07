from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Boolean, String, DateTime, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db, login
from flask_login import UserMixin
import base64
from datetime import datetime, timedelta
import uuid
import os

class User(UserMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(db.String(32), index=True, unique=True)
    token_expiration = Column(db.DateTime)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(db.String(128))
    scores = relationship("Score", backref="owner", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

    def from_dict(self, data, is_new_user=False):
        for field in ["username", "email"]:
            if field in data:
                setattr(self, field, data[field])
        if is_new_user and "password" in data:
            self.set_password(data["password"])

    def get_token(self, expires_in=28800):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    return User.query.get(uuid.UUID(id))

class Score(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(140))
    inDefaultCorpus = Column(Boolean)
    title = Column(String(140))
    composer = Column(String(64))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    lessons = Column(ARRAY(db.Integer))
    tactile_stimuli = Column(db.ARRAY(db.String(64)))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    recordings = relationship("Recording", backref="score", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "composer": self.composer,
            "filename": self.filename,
            "lessons": self.lessons,
            "tactileStimuli": self.tactile_stimuli,
            "inDefaultCorpus": self.inDefaultCorpus,
            "recordings": [recording.to_dict() for recording in self.recordings],
        }

    def __repr__(self):
        return "<Score {}>".format(self.title)

class Recording(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(140))
    matching_score = Column(Integer)
    timing_score = Column(Integer)
    score_id = Column(UUID(as_uuid=True), ForeignKey("score.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "matchingScore": self.matching_score,
            "timingScore": self.timing_score,
            "user_id": self.user_id,
        }

    def __repr__(self):
        return "<Recording {}>".format(self.filename)