<template>
<v-container>
  <v-row>
    Select the doctor: 
  </v-row>
  <v-row>
    <v-col>
      <v-sheet height="560">
        <v-calendar
          :start="today"
          :value="today"
          :events="events"
          color="primary"
          type="week"
          interval-count="24"
          interval-height="100"
        ></v-calendar>
      </v-sheet>
    </v-col>
  </v-row>
</v-container>
</template>

<script lang="ts">
import Vue from 'vue';
export default Vue.extend({
  data() {
    return {
      today: '2019-09-01',
    };
  },
  computed: {
    events() {
      return this.$store.state.statistics.map((stat: any) => {
        const start = new Date(2019, 9, stat.weekday + 1, stat.hours);
        return {
          name: `Avg: ${stat.average_num.toFixed(3)}, Total: ${stat.total_num}`,
          start: `${start.getFullYear()}-${start.getMonth()}-${stat.weekday + 1} ${stat.hours}:00`,
          end: `${start.getFullYear()}-${start.getMonth()}-${stat.weekday + 1} ${stat.hours + 1}:00`,
        };
      });
    },
  },
  created() {
    this.$store.dispatch('query2');
  },
});
</script>
