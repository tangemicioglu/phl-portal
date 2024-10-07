import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

import auth from './auth';
import bluetooth from './bluetooth';
import midi from './midi';
import music from './music';

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  modules: {
    auth,
    bluetooth,
    midi,
    music,
  },
});
