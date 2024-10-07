<template>
  <div>
    <Navbar />
    <br />
    <ScoreList />
  </div>
</template>

<script lang="ts">
import Navbar from '@/components/Navbar.vue';
import ScoreList from '@/components/ScoreList.vue';

export default {
  components: {
    Navbar,
    ScoreList,
  },
};
</script>
