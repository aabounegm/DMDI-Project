<template>
  <v-container>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="$store.state.doctors"
        :search="search"
        @item-expanded="getHours"
        show-expand
        single-expand
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
        <template v-slot:expanded-item="props">
          <td :colspan="headers.length">
            <v-sheet height="400">
              <v-calendar
                :start="today"
                :value="today"
                :events="hours"
                color="primary"
                type="week"
                interval-count="24"
                interval-height="100"
              ></v-calendar>
            </v-sheet>
          </td>
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
        { text: '', value: 'data-table-expand' },
      ],
      hours: [] as any[],
      today: '2019-09-01',
    };
  },
  created() {
    this.$store.dispatch('getDoctors');
  },
  methods: {
    ...mapActions(['query1', 'query5']),
    async getHours({item, value}: {item: any, value: boolean}) {
      if (!value) {
        return;
      }
      this.hours = [];
      const hours: any[] = await this.$store.dispatch('doctor_working_hours', item.id);
      this.hours = hours.map((slot: any) => ({
        start: `2019-09-${1 + slot.day} ${slot.start_time}`,
        end: `2019-09-${1 + slot.day} ${slot.end_time}`,
        name: 'Shift',
      }));
    },
  },
});
</script>
