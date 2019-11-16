<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title style="margin-right: 20px;" class="headline text-uppercase">
        <span>Hospital</span>
      </v-toolbar-title>

      <v-btn text to="/doctors">
        Doctors
      </v-btn>
      
      <v-btn text to="/patients">
        Patients
      </v-btn>
      
      <v-btn v-if="$store.getters.canSeeReports" text to="/reports">
        My Reports
      </v-btn>

      <v-spacer></v-spacer>
      <v-btn
        text
        to="/login"
      >
        Login
      </v-btn>
    </v-app-bar>

    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'App',
  data: () => ({
    //
  }),
});
</script>
