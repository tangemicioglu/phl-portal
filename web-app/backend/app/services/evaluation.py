from music21 import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


class Notes:
    def __init__(self, note, time, note_status, ctime, cticks, velocity):
        self.note = note
        self.time = time
        self.cumulativeTime = ctime
        self.keyPressDuration = None
        self.cticks = cticks
        if note_status == "note_on" and velocity > 0:
            self.keyPressed = 1
        else:  # status = "note_off" or velocity = 0
            self.keyPressed = 0

    def Print(self):
        print(
            "Note:",
            self.note,
            ",Time:",
            self.time,
            ",Cumulative Time:",
            self.cumulativeTime,
            ",Cumulative Ticks:",
            self.cticks,
            ",Key Pressed:",
            self.keyPressed,
            ",Key Press duration:",
            self.keyPressDuration,
        )


def getFirstTrack(MidiFile):
    """Returns the first MidiTrack that has NOTE_ON events"""
    for track in MidiFile.tracks:
        if track.hasNotes():
            return track


def dist(i, j):
    if i == j:
        return 0
    else:
        return 1


def SeqAlignment(a, b):
    gap = -1
    mismatch = -1
    opt = np.empty((len(a) + 1, len(b) + 1))
    for i in range(0, len(a) + 1):
        opt[i, 0] = i * gap
    for j in range(0, len(b) + 1):
        opt[0, j] = j * gap
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                mismatch = +1
            else:
                mismatch = -1
            opt[i, j] = max(
                mismatch + opt[i - 1, j - 1], gap + opt[i - 1, j], gap + opt[i, j - 1]
            )
    return opt


def SeqAlignPath(
    opt, a, b, tempa, tempb, timeThreshold
):  # DP matrix,OG,test,tempa,tempb,timeThreshold
    n = len(a)
    i = opt.shape[0] - 1
    j = opt.shape[1] - 1
    align_a = []  # list of tuple of (matched note,time)
    align_b = []
    while i >= 1 or j >= 1:
        if dist(tempa[i - 1], tempb[j - 1]) == 0:
            match = 1
        if dist(tempa[i - 1], tempb[j - 1]) == 1:
            match = -1
        if i >= 1 and j >= 1 and opt[i, j] == match + opt[i - 1, j - 1]:
            align_a.append(a[i - 1])
            align_b.append(b[j - 1])
            i -= 1
            j -= 1
        elif j >= 1 and opt[i, j] == -1 + opt[i, j - 1]:
            align_a.append("-")
            align_b.append(b[j - 1])
            j -= 1
        elif i >= 1 and opt[i, j] == -1 + opt[i - 1, j]:
            align_a.append(a[i - 1])
            align_b.append("-")
            i -= 1
    matchcost = 0
    align_a.reverse()
    align_b.reverse()
    time_a = []  # list of time from a of matching notes
    time_b = []  # list of time from b of matching notes
    time_ratio = []

    # Fix for note matching issues. Convert all notes to chords and treat chords as a set to prevent duplicates.

    for i in range(len(align_a)):
        if align_a[i][0] != None:
            if isinstance(align_a[i], str):
                continue
            align_a[i][2] = set([align_a[i][0]])
            align_a[i][0] = None
        else:
            align_a[i][2] = set(align_a[i][2])
    for i in range(len(align_b)):
        if isinstance(align_b[i], str):
            continue
        if align_b[i][0] != None:
            align_b[i][2] = set([align_b[i][0]])
            align_b[i][0] = None
        else:
            align_b[i][2] = set(align_b[i][2])

    for i in range(len(align_a)):
        if (
            align_a[i][0] != align_b[i][0]
        ):  # notes matched are not the same, incorrect note
            matchcost += 1
        else:  # notes matched are the same
            if align_a[i][0] == None:  # chord
                if set(align_a[i][2]) != set(
                    align_b[i][2]
                ):  # Set is an unordered collection
                    matchcost += 1  # incorrect chord cost
            time_ratio.append(
                abs(align_b[i][1] / align_a[i][1])
            )  ######## !!!!will raise error with chords- denominator will be 0!!!!

            time_a.append(align_a[i][1])
            time_b.append(align_b[i][1])

    timecost = 0
    if (
        len(time_ratio) != 0
    ):  # if there are no matching notes at all throughout the song, the time_ratio list will be empty. In this case, we keep the time_cost 0 as no matching notes are there, to stay consistent
        time_ratio = np.asarray(time_ratio)
        hist, bin_edges, _ = plt.hist(time_ratio, bins="auto")
        max_index = np.argmax(hist)
        sum = 0
        count = 0
        for i in time_ratio:
            if i >= bin_edges[max_index] and i < bin_edges[max_index + 1]:
                sum = sum + i
                count += 1

        time_b = np.asarray(time_b) / (sum / count)  # scaling the test file
        # time_a = np.asarray(time_a) * (sum/count) #scaling the original file
        for i in range(len(time_a)):
            if abs(time_a[i] - time_b[i]) > timeThreshold:
                timecost += 1

    return matchcost, timecost, n  # *(sum/count)


def updateKeyPressDuration(list, BPM, ppq):  # list is list of objects of class Notes
    noteTime = []
    i = 0
    chordWindow = 25  # +-10 ticks for chord #parameter to be tuned
    while i in range(len(list) - 1):
        if list[i].keyPressed == 1:
            j = i + 1
            count = 0
            while j < len(list) - 1 and (
                (list[j].keyPressed != 1)
                or (
                    list[j].keyPressed == 1
                    and (
                        list[j].cticks <= list[i].cticks + chordWindow
                        and list[j].cticks >= list[i].cticks - chordWindow
                    )
                )
            ):  # increment j till the next key is not pressed, or it is a chord
                temp = j + 1
                if (
                    list[j].keyPressed == 1
                ):  # and (list[j].cticks <= list[i].cticks+chordWindow and list[j].cticks >= list[i].cticks-chordWindow )): #instead of exactly equal(for chord detection), cticks within a range of 10(chordWindow) difference - tune this parameter
                    count += 1
                    end = temp

                j += 1
                # check if condition1 and then condition2 within the same loop is a possiibility? -> yes, added variable check
                # if(count !=0 and !(list[j].keyPressed == 1 and list[j].ctime == list[i].ctime)): #there was a chord but it has ended
            diff = (60 / (BPM * ppq)) * (list[j].cticks - list[i].cticks)
            if diff < 0:  # REMOVE
                print("!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!")
                print(
                    list[j].cumulativeTime,
                    list[i].cumulativeTime,
                    list[j].cticks,
                    list[i].cticks,
                )
            if count != 0:
                chordNotes = []
                for k in range(i, end):
                    if list[k].keyPressed == 1:
                        list[k].keyPressDuration = diff
                        chordNotes.append(list[k].note)
                noteTime.append(
                    (None, list[k].keyPressDuration, chordNotes)
                )  # first element = None in case of chord -> used to detect chord, any one keyPressDuration of the chord elements saved as they are all almost equal
            else:
                list[
                    i
                ].keyPressDuration = diff  # duration between two consecutive key presses, 0 in case of chords
                noteTime.append(
                    (list[i].note, list[i].keyPressDuration, None)
                )  # list of tuples (note, duration,) ###TODO: Cap the keyPressDuration according to "Sustain"
            i = j
    return list, np.array(noteTime, dtype=object)


def preProcess(mf):
    """Returns a list where each entry is a note_on event containing the event time and the MidiEvent"""

    # mf = midi.MidiFile()
    # mf.open(str(file))
    # mf.read()
    # mf.close()
    tracklist = []
    for track in mf.tracks:
        if track.hasNotes():
            tracklist.append(track)
    # TODO: insert merge sort by time for multiple tracks
    # print(mf.ticksPerQuarterNote)
    ppq = mf.ticksPerQuarterNote
    notes_og = []  # list is list of objects of class Notes

    tempo_check = 0  #  to check if tempo has been read once, and not read again-> causing issues with B._Bartok_Children_at_Play.mid, cumulative time decreases in consecutive midi elements on merging tracks (tempo changes multiple times in track0)
    for MidiTrack in tracklist:
        allNotes = []
        index = 0
        ctime = 0
        tempo = 500000  # default
        BPM = 60000000 / tempo  # default
        for event in MidiTrack.events:
            index += 1
            # TODO: read tempo
            if (
                event.type == midi.MetaEvents.SET_TEMPO
            ):  ########TODO : Noah midi/Moonlight_cropped3.mid has multiple set_tempo events, how to proceed?? https://stackoverflow.com/questions/59502210/why-are-there-multiple-set-tempo-meta-midi-messages-and-how-to-deal
                if (
                    tempo_check == 0
                ):  ##  to check if tempo has been read once, and not read again, keep one tempo for one midi file
                    tempo = int.from_bytes(event.data, "big")
                    BPM = 60000000 / tempo
                    tempo_check += 1
            if event.isNoteOn() or event.isNoteOff():
                allNotes.append((event.time, event))
                t = MidiTrack.events[index - 2].time
                ctime = ctime + t
                if event.isNoteOn():
                    type = "note_on"
                else:
                    type = "note_off"
                ctimesec = (60 / (BPM * ppq)) * ctime
                noteObj = Notes(event.pitch, t, type, ctimesec, ctime, event.velocity)
                notes_og.append(noteObj)

    # TODO: Apply merge sort on multiTrackNoteTime- OPTIMIZE SORT
    notes_og.sort(key=lambda x: x.cticks, reverse=False)
    notes_og, noteTimeOG = updateKeyPressDuration(
        notes_og, BPM, ppq
    )  # Return noteTime values here, notes_og: same list with updated duration, noteTimeOG: list of tuples (note, duration)
    return noteTimeOG


# allNotesOn = preProcess(file)#firstTrack, PPQ) #ticksPerQuarterNote is same as ppq
def Evaluate(midi_OG, midi_test, timeThreshold=0.2, timeweight=1, matchweight=1):
    OG = preProcess(midi_OG)

    test = preProcess(midi_test)

    tempa = []  # a[:,0] #list of only notes
    for i in range(len(OG)):
        if OG[i, 0] == None:  # chord
            tempa.append(set(OG[i, 2]))
        else:
            tempa.append(OG[i, 0])
    tempb = []  # b[:,0] #list of only notes
    for i in range(len(test)):
        if test[i, 0] == None:
            tempb.append(set(test[i, 2]))
        else:
            tempb.append(test[i, 0])
    tempa = np.array(tempa)
    tempb = np.array(tempb)
    for i in range(len(tempa)):
        if isinstance(tempa[i], set):
            if len(tempa[i]) == 1:
                tempa[i] = tempa[i].pop()

    for i in range(len(tempb)):
        if isinstance(tempb[i], set):
            if len(tempb[i]) == 1:
                tempb[i] = tempb[i].pop()
    matchcost, timecost, n = SeqAlignPath(
        SeqAlignment(tempa, tempb), OG, test, tempa, tempb, timeThreshold
    )  # TODO: OG[17:34,0],test[17:34,0] getting stuck , CHECK WHY
    matchcost *= matchweight
    timecost *= timeweight
    percentage = ((n - matchcost - timecost) * 100) / n
    return matchcost, timecost, percentage


# midi_OG = 'Noah midi/B._Bartok_Children_at_Play.mid' #Noah midi/Moonlight_cropped3.mid
# midi_test = 'Noah midi/children_at_play.MID' #Noah midi/moon test.mid
# match_cost , time_cost, percentage = Evaluate(midi_OG,midi_test)
# print("Total Cost:",match_cost + time_cost,"Seq Alignment Cost:",match_cost,"Timing Cost:",time_cost)
# print("Percentage =", percentage )
