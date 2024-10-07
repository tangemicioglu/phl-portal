import midiServices from '@/services/midi';

const initialState = {
  midiAccess: null,
  midiInput: null,
  midiOutput: null,
  isMIDIDeviceConnected: false,
};

const midi = {
  namespaced: true,
  state: {
    midiAccess: null,
    midiInput: null,
    midiOutput: null,
    isMIDIDeviceConnected: false,
  },
  mutations: {
    setDisconnected(state) {
      state.isMIDIDeviceConnected = false;
    },
    updateMIDIAccess(state, event) {
      state.isMIDIDeviceConnected = event.port.state === 'connected';
      state.midiAccess = event.target;
      state.midiInput = midiServices.extractMIDIInput(state.midiAccess);
      state.midiOutput = midiServices.extractMIDIOutput(state.midiAccess);
    },
  },
};

export default midi;
