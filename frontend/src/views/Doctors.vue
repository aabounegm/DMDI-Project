<template>
  <v-container>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="$store.state.doctors"
        :search="search"
      >
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>Doctors</v-toolbar-title>
            <v-divider
              class="mx-4"
              inset
              vertical
            ></v-divider>
            <v-btn @click="query1">
              (1) First/Last = M/L
            </v-btn>
            <v-btn @click="query5">
              (5) patients>=5/year (100 total) 
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
        { text: 'Phone #', value: 'phone_number' },
        { text: 'Cost', value: 'cost' },
        { text: 'Room #', value: 'room' },
        { text: 'Speciality', value: 'speciality' },
      ],
    };
  },
  created() {
    this.$store.dispatch('getDoctors');
  },
  methods: mapActions(['query1', 'query5']),
});
</script>
