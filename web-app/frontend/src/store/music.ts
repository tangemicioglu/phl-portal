import databaseServices from '@/services/database';

const initialState = {
  activeScore: null,
  scores: null,
};

const music = {
  namespaced: true,
  state: {
    activeScore: null,
    scores: null,
  },
  mutations: {
    addScore(state, score) {
      state.scores = [...state.scores, score];
    },
    addRecording(state, recording) {
      state.activeScore.recordings.push(recording);
    },
    updateScores(state, scores) {
      state.scores = scores;
    },
    setActiveScore(state, scoreIndex) {
      state.activeScore = state.scores[scoreIndex];
    },
    cacheXML(state, xml) {
      state.activeScore.xml = xml;
    },
  },
  actions: {
    async uploadScore({ commit, rootState }, { title, composer, file }) {
      const { token } = rootState.auth;
      const score = await databaseServices.uploadScore(title, composer, file, token);
      commit('addScore', score);
      return true;
    },
    async uploadRecording({ commit, rootState }, { file }) {
      const { token } = rootState.auth;
      const { id } = rootState.music.activeScore;
      const recording = await databaseServices.uploadRecording(file, id, token);
      commit('addRecording', recording);
      return true;
    },
    async fetchScores({ commit, rootState }) {
      const { token } = rootState.auth;
      const scores = await databaseServices.getScores(token);
      commit('updateScores', scores);
      return true;
    },
    async fetchXML({ commit, rootState }) {
      const { token } = rootState.auth;
      const { id } = rootState.music.activeScore;
      const xml = await databaseServices.getXML(id, token);
      commit('cacheXML', xml);
      return true;
    },
  },
};

export default music;
