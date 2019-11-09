import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const API = 'http://localhost:5000/api';

export default new Vuex.Store({
  state: {
    userType: '',
    doctors: [],
    nurses: [],
    patients: [],
  },
  mutations: {
    setUserType(state, payload) {
      state.userType = payload;
    },
    setDoctors(state, payload) {
      state.doctors = payload;
    },
    setNurses(state, payload) {

    },
    setPatients(state, payload) {

    },
  },
  actions: {
    async getAllUsers({ dispatch }) {
      dispatch('getDoctors');
      dispatch('getNurses');
      dispatch('getPatients');
    },
    async getDoctors({ commit }) {
      let response = await fetch(`${API}/doctors`);
      let json = await response.json();
      commit('setDoctors', json);
    },
    async getNurses({ commit }) {

    },
    async getPatients({ commit }) {

    },
  },
  modules: {
  },
});
