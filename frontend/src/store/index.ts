import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const API = process.env.NODE_ENV === 'development' ? 'http://localhost:5000/api' : '/api';

export default new Vuex.Store({
  state: {
    currentUser: null as any,
    userType: 'guest',
    doctors: [],
    nurses: [],
    patients: [],
    reports: [],
    statistics: [],
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
      payload.forEach((element: any) => {
        const name = element.emergency_contact_name || '';
        const phone = element.emergency_contact_phone_number || '';
        const relation = element.emergency_contact_relation || '';
        element.emergency_contact = `${name} (${phone}) [${relation}]`;
        if (element.emergency_contact === ' () []') {
          element.emergency_contact = '';
        }
        element.date_of_birth = new Date(element.date_of_birth).toLocaleDateString('ru');
      });
      state.patients = payload;
    },
    setReports(state, payload) {
      state.reports = payload;
    },
    setStatistics(state, payload) {
      state.statistics = payload;
    },
  },
  actions: {
    async getAllUsers({ dispatch }) {
      dispatch('getDoctors');
      dispatch('getNurses');
      dispatch('getPatients');
    },
    async getDoctors({ commit }) {
      const response = await fetch(`${API}/doctors/`);
      const json = await response.json();
      commit('setDoctors', json);
    },
    async getNurses({ commit }) {
      const response = await fetch(`${API}/nurses/`);
      const json = await response.json();
      commit('setNurses', json);
    },
    async getPatients({ commit }) {
      const response = await fetch(`${API}/patients/`);
      const json = await response.json();
      commit('setPatients', json);
    },
    async getReports({ commit, state }) {
      const response = await fetch(`${API}/reports/?${state.userType}_id=${state.currentUser.id}`);
      const json = await response.json();
      json.forEach((element: any) => {
        if (element.needs_follow_up) {
          element.needs_follow_up = 'Yes';
        } else {
          element.needs_follow_up = 'No';
        }
      });
      commit('setReports', json);
    },
    async query1({ commit, state }) {
      if (state.userType !== 'patient' || state.currentUser == null) {
        alert('Please select a valid patient!');
        return;
      }
      const response = await fetch(`${API}/doctors/query1?patient_id=${state.currentUser.id}`);
      const json = await response.json();
      commit('setDoctors', json);
    },
    async query2({ commit, state }) {
      if (state.userType !== 'doctor' || state.currentUser == null) {
        alert('Please select a valid doctor!');
        return;
      }
      const response = await fetch(`${API}/doctors/query2?doctor_id=${state.currentUser.id}`);
      const json = await response.json();
      commit('setStatistics', json);
    },
    async query3({ commit }) {
      const response = await fetch(`${API}/patients/query3`);
      const json = await response.json();
      commit('setPatients', json);
    },
    async query4({ commit }) {
      const response = await fetch(`${API}/query4`);
      const json = await response.json();
      return json;
    },
    async query5({ commit }) {
      const response = await fetch(`${API}/doctors/query5`);
      const json = await response.json();
      commit('setDoctors', json);
    },
    async doctor_working_hours(context, payload) {
      if (payload == null) {
        throw new Error('Please pass a valid doctor id');
      }
      const response = await fetch(`${API}/doctors/working_hours?doctor_id=${payload}`);
      const json = await response.json();
      return json;
    },
  },
  getters: {
    canSeeReports: (state) => state.currentUser != null && ['doctor', 'patient'].includes(state.userType),
  },
});
