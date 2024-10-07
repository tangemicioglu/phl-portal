<template>
  <b-card
    header="PHL Glove"
    header-tag="header"
    :border-variant="isGloveConnected ? 'success' : 'danger'"
  >
    <b-card-title>
      <b-icon
        :icon="isGloveConnected ? 'check2-circle' : 'x-circle'"
        :variant="isGloveConnected ? 'success' : 'danger'"
        aria-hidden="true"
      />
      {{
        isGloveConnected ? `Connected to ${glove.name}` : 'No Gloves Connected'
      }}
    </b-card-title>
    <b-card-text v-if="!isGloveConnected">
      Connect your PHL Gloves to enable Passive training.
    </b-card-text>
    <b-button v-if="isGloveConnected" @click="disconnectFromGlove">
      Disconnect
    </b-button>
    <b-button-toolbar v-else>
      <b-button class="mx-1" @click="scanOrConnectGlove">
        Connect Gloves over Bluetooth
      </b-button>
    </b-button-toolbar>
  </b-card>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import bluetoothServices from '../services/bluetooth';

export default {
  computed: {
    ...mapState('bluetooth', ['glove', 'characteristic', 'isGloveConnected']),
  },
  methods: {
    ...mapActions('bluetooth', ['scanForGlove', 'connectToGlove', 'disconnectFromGlove']),
    async scanOrConnectGlove() {
      if (this.glove) {
        const success = await this.connectToGlove(this.glove);
        if (success) return;
      }
      this.scanForGlove();
    },
  },
  beforeMount() {
    window.addEventListener('beforeunload', (e) => {
      if (this.glove != null) {
        bluetoothServices.disconnectFromDevice(this.glove);
      }
    });
  },
};
</script>
