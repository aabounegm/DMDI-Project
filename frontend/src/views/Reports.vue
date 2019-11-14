<template>
  <v-container>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="$store.state.reports"
        :search="search"
      >
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>Reports</v-toolbar-title>
            <v-divider
              class="mx-4"
              inset
              vertical
            ></v-divider>
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
export default Vue.extend({
  data() {
    return {
      search: '',
      headers: [
        { text: 'Patient', value: 'patient_name' },
        { text: 'Doctor', value: 'doctor_name' },
        { text: 'Diagnosis', value: 'diagnosis' },
        { text: 'Date', value: 'date' },
        { text: 'Need followup?', value: 'needs_follow_up' },
        { text: 'Additional Notes', value: 'additional_notes' },
      ],
    };
  },
  created() {
    this.$store.dispatch('getReports');
  },
});
</script>
