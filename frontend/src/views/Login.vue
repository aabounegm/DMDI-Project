<template>
  <v-container>
    <pre>Current User: {{ currentUser | pretty }}</pre>
    <v-radio-group v-model="userType">
      <v-radio v-for="(value, type) in users" :key="type" :value="type">
        <template v-slot:label>
          {{ type }}
          <v-select style="margin-left: 50px;" :items="value" v-model="currentUser">
            <template v-slot:item="{ item }">
              {{ item | name }}
            </template>
            <template v-slot:selection="{ item }">
              {{ item | name }}
            </template>
          </v-select>
        </template>
      </v-radio>
      <v-radio label="Guest" value="guest"></v-radio>
    </v-radio-group>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapState } from 'vuex';
export default Vue.extend({
  data() {
    return {
    };
  },
  computed: {
    userType: {
      get() { return this.$store.state.userType; },
      set(val) { this.$store.commit('setUserType', val); },
    },
    currentUser: {
      get() { return this.$store.state.currentUser; },
      set(val) { this.$store.commit('setCurrentUser', val); },
    },
    ...mapState({
      users(state: any) {
        return {
          doctor: state.doctors,
          nurse: state.nurses,
          patient: state.patients,
        };
      },
    }),
  },
  mounted() {
    this.$store.dispatch('getAllUsers');
  },
  filters: {
    name(item: any) {
      if (typeof item.name === 'string') {
        return item.name;
      }
      return `${item.first_name} ${item.last_name}`;
    },
    pretty(value: Object) {
      return JSON.stringify(value, null, 4);
    },
  },
});
</script>
