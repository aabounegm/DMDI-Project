import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userType: '',
  },
  mutations: {
    setUserType(state, payload) {
      state.userType = payload;
    },
  },
  actions: {
  },
  modules: {
  },
});
