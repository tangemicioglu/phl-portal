<template>
  <b-card
    header="MIDI Device"
    header-tag="header"
    :border-variant="this.connectionVariant"
  >
    <b-card-title>
      <b-icon
        :icon="this.isMIDIDeviceConnected ? 'check2-circle' : 'x-circle'"
        :variant="this.connectionVariant"
        aria-hidden="true"
      />
      {{
        this.isMIDIDeviceConnected
          ? `Connected to ${this.midiInput.name}`
          : 'No MIDI Device Connected'
      }}
    </b-card-title>
    <b-card-text v-if="!this.isMIDIDeviceConnected">
      Connect a compatible MIDI Device to expand the capabilites of your Active
      practice sessions.
    </b-card-text>
  </b-card>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import { OpenSheetMusicDisplay } from 'opensheetmusicdisplay';
import AudioPlayer from 'osmd-audio-player';
import store from '@/store';
import LessonUploadModal from './LessonUploadModal.vue';
import RecordingUploadModal from './RecordingUploadModal.vue';
import midiServices from '../services/midi';

export default {
  computed: {
    ...mapState('midi', ['midiAccess', 'midiInput', 'midiOutput', 'isMIDIDeviceConnected']),
    ...mapState('music', ['activeScore']),
    ...mapState('bluetooth', ['isGloveConnected']),
    connectionVariant() {
      return this.isMIDIDeviceConnected ? 'success' : 'danger';
    },
  },
  methods: {
    ...mapActions('midi', []),
  },
  onMIDIMessage(event) {
    console.log('**', event);
  },
  beforeMount() {
    navigator.requestMIDIAccess().then((midiAccess) => {
      midiAccess.inputs.forEach((input) => {
        input.onmidimessage = this.onMIDIMessage;
      });
      store.commit('midi/setDisconnected');
      midiAccess.onstatechange = function (e) {
        if (e.port.state === 'disconnected') {
          store.commit('midi/setDisconnected');
        } else {
          store.commit('midi/updateMIDIAccess', e);
        }
      };
    });
  },
};
</script>
