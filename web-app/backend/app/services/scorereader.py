"""
Created on Thu Nov 26 19:22:20 2015
@author: marco musy
"""
from music21.articulations import Fingering

from .utils import keypos, keypos_midi
from operator import attrgetter

#####################################################
class INote:
    def __init__(self):
        self.name     = None
        self.isChord  = False
        self.isBlack  = False
        self.pitch = 0
        self.octave   = 0
        self.x        = 0.0
        self.time     = 0.0
        self.duration = 0.0
        self.fingering= 0
        self.measure  = 0
        self.chordnr  = 0
        self.NinChord = 0
        self.chordID  = 0
        self.noteID   = 0

#####################################################
def get_finger_music21(n, j=0):
    fingers = []
    for art in n.articulations:
        if type(art) == Fingering:
            fingers.append(art.fingerNumber)
    finger = 0
    if len(fingers) > j:
        finger = fingers[j]
    return finger


def reader(sf, beam=0):

    noteseq = []

    if hasattr(sf, 'parts'):
        if len(sf.parts) <= beam:
            return []
        strm = sf.parts[beam].flat
    elif hasattr(sf, 'elements'):
        if len(sf.elements)==1 and beam==1:
            strm = sf[0]
        else:
            if len(sf) <= beam:
                return []
            strm = sf[beam]
    else:
        strm = sf.flat

    print('Reading beam', beam, 'with', len(strm), 'objects in stream.')

    chordID = 0
    noteID = 0
    for n in strm.getElementsByClass("GeneralNote"):

        if n.duration.quarterLength==0: continue

        if hasattr(n, 'tie'): # address bug https://github.com/marcomusy/pianoplayer/issues/29
            if n.tie and (n.tie.type == 'continue' or n.tie.type=='stop'): continue

        if n.isNote:
            if len(noteseq) and n.offset == noteseq[-1].time:
                # print "doppia nota", n.name
                continue
            an        = INote()
            an.noteID = noteID
            an.note21 = n
            an.isChord= False
            an.name   = n.name
            an.octave = n.octave
            an.measure= n.measureNumber
            an.x      = keypos(n)
            an.pitch  = n.pitch.midi
            an.time   = n.offset
            an.duration = n.duration.quarterLength
            an.isBlack= False
            pc = n.pitch.pitchClass
            an.isBlack = False
            if pc in [1, 3, 6, 8, 10]:
                an.isBlack = True
            if n.lyrics:
                an.fingering = n.lyric

            an.fingering = get_finger_music21(n)
            noteseq.append(an)
            noteID += 1

        elif n.isChord:

            if n.tie and (n.tie.type=='continue' or n.tie.type=='stop'): continue
            sfasam = 0.05 # sfasa leggermente le note dell'accordo

            for j, cn in enumerate(n.pitches):
                an = INote()
                an.chordID  = chordID
                an.noteID = noteID
                an.isChord = True
                an.pitch = cn.midi
                an.note21  = cn
                an.name    = cn.name
                an.chordnr = j
                an.NinChord = len(n.pitches)
                an.octave  = cn.octave
                an.measure = n.measureNumber
                an.x       = keypos(cn)
                an.time    = n.offset-sfasam*(len(n.pitches)-j-1)
                an.duration= n.duration.quarterLength+sfasam*(an.NinChord-1)
                if hasattr(cn, 'pitch'):
                    pc = cn.pitch.pitchClass
                else:
                    pc = cn.pitchClass
                if pc in [1, 3, 6, 8, 10]:
                    an.isBlack = True
                else:
                    an.isBlack = False
                an.fingering = get_finger_music21(n, j)
                noteID += 1
                noteseq.append(an)
            chordID += 1

    if len(noteseq) < 2:
        print("Beam is empty.")
        return []
    return noteseq