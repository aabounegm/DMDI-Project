<template>
  <div class="home">
    <h2>Welcome to our DMD project. Login and then select a feature to test</h2>
    (4) By applying the following pricing rules:
    <v-simple-table>
      <thead>
        <tr>
          <th class="text-left"></th>
          <th class="text-left">Appointments per month &lt; 3</th>
          <th class="text-left">Appointments per month &gt;= 3</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Age &lt; 50</td>
          <td>200 Rub</td>
          <td>250 Rub</td>
        </tr>
        <tr>
          <td>Age &gt;= 50</td>
          <td>400 Rub</td>
          <td>500 Rub</td>
        </tr>
      </tbody>
    </v-simple-table>
    The hospital would earn: {{ sum }} Rub.
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
  data() {
    return {
      sum: '...',
    };
  },
  created() {
    this.$store.dispatch('query4').then((s) => this.sum = s.sum);
  },
};
</script>
