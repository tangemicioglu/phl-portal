from music21 import note, chord, stream, articulations

QUARTER_LENGTH_TO_MS = 500
OST_OFFSET_MS = 50

def generate_lessons(s, min_stimuli=10, max_stimuli=17):
    lessons = []
    curr_num_stimuli = 0
    total_num_stimuli = 1
    offsetIterator = stream.iterator.OffsetIterator(s.recurse())
    for elements in offsetIterator:
        for element in elements:
            if isinstance(element, stream.Measure):
                if curr_num_stimuli in range(min_stimuli, max_stimuli):
                    lessons.append(total_num_stimuli)
                    total_num_stimuli += curr_num_stimuli
                    curr_num_stimuli = 0
            if isinstance(element, note.Note):
                curr_num_stimuli += 1
            if isinstance(element, chord.Chord):
                curr_num_stimuli += len(element.notes)
    lessons.append(total_num_stimuli)
    return lessons

def generate_tactile_stimuli(s):
    tactile_stimuli = []
    finger_durations = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    notes = s.recurse().notes
    noteOffsetIterator = stream.iterator.OffsetIterator(notes)
    prev_offset = 0;
    for noteGroup in noteOffsetIterator:

        # calculate offset since last note group
        offset = noteGroup[0].offset
        offset_difference = offset - prev_offset;
        prev_offset = offset
        
        # append tactile stimuli for previous note group
        tactile_stimulus = ("".join(map(lambda duration: str(1 if duration > 0 else 0), finger_durations)) + " " + str(int(offset_difference * QUARTER_LENGTH_TO_MS)))
        tactile_stimulus = tactile_stimulus[0:5] + ' ' + tactile_stimulus[5:]
        tactile_stimuli.append(tactile_stimulus)

        # subtract lapsed duration from remaining notes
        finger_durations[:] = [(duration - offset_difference if duration >= offset_difference else 0) for duration in finger_durations]

        # add duration of all notes in current group
        for n in noteGroup:
            part = n.getContextByClass(stream.Part)
            isLeftHand = (part is s.parts[0])
            if isinstance(n, chord.Chord):
                fingerings = [a for a in n.articulations if isinstance(a, articulations.Fingering)]
                for fingering in fingerings:
                    durationIndex = fingering.fingerNumber - 1 if isLeftHand else fingering.fingerNumber + 4
                    finger_durations[durationIndex] += n.quarterLength
            else:
                fingering = next((a for a in n.articulations if isinstance(a, articulations.Fingering)), articulations.Fingering(3))
                durationIndex = fingering.fingerNumber - 1 if isLeftHand else fingering.fingerNumber + 4
                finger_durations[durationIndex] += n.quarterLength
    
    # append stimulus for final note group
    final_tactile_stimulus = ("".join(map(lambda duration: str(1 if duration > 0 else 0), finger_durations)) + " " + str(int(offset_difference * QUARTER_LENGTH_TO_MS)))
    final_tactile_stimulus = final_tactile_stimulus[0:5] + ' ' + final_tactile_stimulus[5:]
    tactile_stimuli.append(final_tactile_stimulus)

    return tactile_stimuli