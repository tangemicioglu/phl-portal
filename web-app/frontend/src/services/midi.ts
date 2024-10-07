import {
  Input, Output,
} from 'webmidi';

const navigator = (window.navigator as any);

const MIDDLE_C = 60;
const NOTE_ON = 0x93;
// LK-S250 takes MIDI in channel as 3 for Left hand and 4 for Right hand.
// Since we are not looking to send two hands separately, either of 0x92 or 0x93 works
const NOTE_OFF = 0x83;
//  "In practice, musicians and software refer to the MIDI channels by
// counting them from 1 to 16, so that there is a difference of 1 when you
// program them in hexadecimal (channel "1" is coded "0", channel "10" is
// coded "9" and channel 16 is coded "F")."
const NOTE_OVERLAP_BUFFER = 10;
// const NOTE_DURATION = 300;

type MIDIStateChangeCallback = (midiAccess) => void;

function extractMIDIInput(midiAccess): Input {
  const { inputs } = midiAccess;
  return inputs.values().next().value;
}

function extractMIDIOutput(midiAccess): Output {
  const { outputs } = midiAccess;
  return outputs.values().next().value;
}

function onMIDIFailure(error: string) {
  console.log(error);
}

async function requestMIDIAccess(stateChangeCallback: MIDIStateChangeCallback) {
  return navigator.requestMIDIAccess().then((midiAccess) => {
    midiAccess.onstatechange = stateChangeCallback;
  }, onMIDIFailure);
}

function playNote(output: Output, note: number, duration: number) {
  output.send([NOTE_ON, MIDDLE_C + note, 0x7f]);
  setTimeout((_: any) => {
    output.send([NOTE_OFF, MIDDLE_C + note, 0x7f]);
  }, duration - NOTE_OVERLAP_BUFFER);
}

export default {
  requestMIDIAccess, extractMIDIInput, extractMIDIOutput, playNote,
};
