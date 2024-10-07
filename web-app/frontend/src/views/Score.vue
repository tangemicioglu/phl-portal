<template>
  <div>
    <Navbar />
    <br />
    <b-card-group deck>
      <GloveConnector />
      <MIDIConnector />
    </b-card-group>
    <br />
    <SheetMusic />
    <br />
    <UserProgress />
  </div>
</template>

<script>
import GloveConnector from '../components/GloveConnector.vue';
import MIDIConnector from '../components/MIDIConnector.vue';
import SheetMusic from '../components/SheetMusic.vue';
import UserProgress from '../components/UserProgress.vue';
import Navbar from '../components/Navbar.vue';

export default {
  components: {
    Navbar,
    GloveConnector,
    MIDIConnector,
    SheetMusic,
    UserProgress,
  },
};
</script>
