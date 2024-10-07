<template>
  <div>
    <b-card title="Default Corpus">
      <p v-if="corpus !== null && corpus.length === 0">
        There are no corpus scores accessible at the moment.
      </p>
      <b-table
        v-else
        :items="corpus"
        :fields="fields"
        hover
        selectable
        @row-selected="onRowSelected"
      >
      </b-table>
    </b-card>
    <br />
    <b-card title="My Score Library" hover>
      <p v-if="library !== null && library.length === 0">
        You haven't uploaded any scores yet.
      </p>
      <b-table
        v-else
        :items="library"
        :fields="fields"
        hover
        selectable
        @row-selected="onRowSelected"
      >
      </b-table>
      <b-button v-b-modal.add-score-modal> Add Score </b-button>
    </b-card>
    <scoreUploadModal />
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex';
import router from '@/router';
import ScoreUploadModal from './ScoreUploadModal.vue';

export default {
  data() {
    return {
      fields: ['title', 'composer'],
    };
  },
  computed: {
    ...mapState('music', ['activeScore', 'scores']),
    corpus() {
      return this.scores ? this.scores.filter((score) => score.inDefaultCorpus) : null;
    },
    library() {
      return this.scores ? this.scores.filter((score) => !score.inDefaultCorpus) : null;
    },
  },
  components: {
    ScoreUploadModal,
  },
  methods: {
    ...mapMutations('music', ['setActiveScore']),
    ...mapActions('music', ['fetchScores']),
    onRowSelected(items) {
      const score = items[0];
      const scoreIndex = this.scores.indexOf(score);
      this.setActiveScore(scoreIndex);
      router.push(`/score/${this.activeScore.id}`);
    },
  },
  beforeMount() {
    this.fetchScores();
  },
};
</script>
