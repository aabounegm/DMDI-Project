<template>
  <v-container>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="$store.state.patients"
        :search="search"
      >
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>Patients</v-toolbar-title>
            <v-divider
              class="mx-4"
              inset
              vertical
            ></v-divider>
            <v-btn @click="query3">
              (3) Two visits weekly
            </v-btn>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-toolbar>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapActions } from 'vuex';
export default Vue.extend({
  data() {
    return {
      search: '',
      headers: [
        { text: 'First name', value: 'first_name' },
        { text: 'Last name', value: 'last_name' },
        { text: 'Blood Type', value: 'blood_type' },
        { text: 'Birth date', value: 'date_of_birth' },
        { text: 'Syndicate', value: 'syndicate_name' },
        { text: 'Emergency contact', value: 'emergency_contact' },
      ],
    };
  },
  created() {
    this.$store.dispatch('getPatients');
  },
  methods: mapActions(['query3']),
});
</script>
