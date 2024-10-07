from music21 import converter
from music21.articulations import Fingering

from .hand import Hand
from .scorereader import reader

def generate_fingerings(
                file,
                n_measures=100,
                start_measure=1,
                depth=0,
                rbeam=0,
                lbeam=1,
                below_beam=False,
                left_only=False,
                right_only=False,
                hand_size='M'
            ):
    class Args(object):
        pass
    args = Args()
    args.file = file
    args.n_measures = n_measures
    args.start_measure = start_measure
    args.depth = depth
    args.rbeam = rbeam
    args.lbeam = lbeam
    args.below_beam = below_beam
    args.left_only = left_only
    args.right_only = right_only
    args.hand_size = hand_size

    annotated_score = annotate(args)
    print("returning fully annotated stream.")
    return annotated_score

def annotate_fingers_xml(stream, hand, args, is_right=True):
    hand_part = stream.parts[args.rbeam if is_right else args.lbeam]
    index = 0
    hand_notes = hand_part.flat.notes
    for note in hand_notes:
        if hasattr(note, 'tie') and note.tie and (note.tie.type == 'continue' or note.tie.type=='stop'): continue
        elif note.isNote:
            n = hand.noteseq[index]
            if hand.lyrics:
                note.addLyric(n.fingering)
            else:
                note.articulations.append(Fingering(n.fingering))
            index += 1
        elif note.isChord:
            for j, chordnote in enumerate(note.pitches):
                n = hand.noteseq[index]
                if hand.lyrics:
                    nl = len(chordnote.chord21.pitches) - chordnote.chordnr
                    note.addLyric(chordnote.fingering, nl)
                else:
                    note.articulations.append(Fingering(n.fingering))
                index += 1
    print('finished annotating a hand.')
    return stream

def annotate(args):

    hand_size = args.hand_size
    file = args.file
    file.seek(0)
    score = converter.parse(file.read().decode('utf-8'))

    if not args.left_only:
        rh_noteseq = reader(score, beam=args.rbeam)
        rh = Hand(side="right", noteseq=rh_noteseq, size=hand_size)
        rh.verbose = False
        if args.depth == 0:
            rh.autodepth = True
        else:
            rh.autodepth = False
            rh.depth = args.depth
        rh.lyrics = args.below_beam
        rh.generate(args.start_measure, args.n_measures)
        score = annotate_fingers_xml(score, rh, args, is_right=True)

    if not args.right_only:
        lh_noteseq = reader(score, beam=args.lbeam)
        lh = Hand(side="left", noteseq=lh_noteseq, size=hand_size)
        lh.verbose = False
        if args.depth == 0:
            lh.autodepth = True
        else:
            lh.autodepth = False
            lh.depth = args.depth
        lh.lyrics = args.below_beam
        lh.generate(args.start_measure, args.n_measures)
        score = annotate_fingers_xml(score, lh, args, is_right=False)

    return score