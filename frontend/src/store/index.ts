import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const API = 'http://localhost:5000/api';

export default new Vuex.Store({
  state: {
    currentUser: null as any,
    userType: '',
    doctors: [],
    nurses: [],
    patients: [],
    reports: [],
  },
  mutations: {
    setUserType(state, payload) {
      state.userType = payload;
      state.currentUser = null;
      state.reports = [];
    },
    setCurrentUser(state, payload) {
      state.currentUser = payload;
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
    setReports(state, payload) {
      state.reports = payload;
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
    async getReports({ commit, state }) {
      const response = await fetch(`${API}/reports?patient_id=${state.currentUser.id}`);
      const json = await response.json();
      commit('setReports', json);
    },
    async query1({ commit }) {
      const response = await fetch(`${API}/doctors/query1`);
      const json = await response.json();
      commit('setDoctors', json);
    }
  },
  getters: {
    canSeeReports: (state) => state.currentUser != null && ['doctor', 'patient'].includes(state.userType),
  },
});
