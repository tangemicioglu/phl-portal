import authServices from '../services/auth';

const initialState = {
  user: null,
  token: null,
};

const auth = {
  namespaced: true,
  state: initialState,
  getters: {
    isUserLoggedIn: (state) => (state.token !== null),
  },
  mutations: {
    loginSuccess(state, { user, token }) {
      state.user = user;
      state.token = token;
    },
    logout(state) {
      state.user = null;
      state.token = null;
    },
  },
  actions: {
    async register(_, { email, username, password }) {
      try {
        await authServices.register(email, username, password);
        return true;
      } catch (error) {
        console.log(error);
        return false;
      }
    },
    async login({ commit }, { username, password }) {
      try {
        const response = await authServices.login(username, password);
        commit('loginSuccess', response);
        return true;
      } catch (e) {
        console.log(e);
        return false;
      }
    },
    logout({ commit }) {
      commit('logout');
    },
  },
};

export default auth;
