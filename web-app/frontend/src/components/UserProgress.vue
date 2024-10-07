<template>
  <b-card no-body>
    <b-card-header header-tag="nav">
      <b-nav card-header tabs>
        <b-nav-item active> Recordings </b-nav-item>
      </b-nav>
    </b-card-header>
    <b-card-body>
      <p v-if="this.activeScore.recordings.length === 0">
        Upload a recording to get your performance evaluated.
      </p>
      <b-list-group v-else>
        <template v-for="recording in activeScore.recordings" >
        <b-list-group-item v-if = "recording.user_id===user.id"
        :key="recording.id">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">{{ recording.filename }}</h5>
            <small>Timestamp</small>
          </div>
          <p class="mb-1">
            Matching Cost: {{ recording.matchingScore }}, Timing Cost:
            {{ recording.timingScore }}
          </p>
      </b-list-group-item>
          <!-- <small>More Data</small> -->
        </template>
      </b-list-group>
    </b-card-body>
  </b-card>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {};
  },
  computed: {
    ...mapState('music', ['activeScore']),
    ...mapState('auth', ['user']),
  },
  components: {},
  methods: {},
};
</script>
