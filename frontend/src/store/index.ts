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
      state.nurses = payload;
    },
    setPatients(state, payload) {
      state.patients = payload;
    },
  },
  actions: {
    async getAllUsers({ dispatch }) {
      dispatch('getDoctors');
      dispatch('getNurses');
      dispatch('getPatients');
    },
    async getDoctors({ commit }) {
      const response = await fetch(`${API}/doctors`);
      const json = await response.json();
      commit('setDoctors', json);
    },
    async getNurses({ commit }) {
      const response = await fetch(`${API}/nurses`);
      const json = await response.json();
      commit('setNurses', json);
    },
    async getPatients({ commit }) {
      const response = await fetch(`${API}/patients`);
      const json = await response.json();
      commit('setPatients', json);
    },
  },
});
