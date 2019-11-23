<template>
  <div class="home" style="padding: 2em; background-color: white;">
    <h1>DMD project - Phase 3</h1>
    <h2>Team members:</h2>
    <ul>
      <li>Abdelrahman Abounegm</li>
      <li>Gosha Stepanov</li>
      <li>Pavel Tishkin</li>
      <li>Vitaliy Korbashov</li>
      <li>Yulia Chukanova</li>
    </ul>
    <p class="subtitle-1 font-italic font-weight-medium">Group 4</p>
    <p class="body-1">
      Browse through the project using the links at the top.
    </p>
    <p class="body-2 font-italic font-weight-light">
      Some queries require being logged in as a doctor or patient.
    </p>
    <v-divider />
    <p class="title" style="margin-top:3em;">(4) By applying the following pricing rules:</p>
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
    <p class="headline font-weight-light">The hospital would earn: {{ sum }} Rub.</p>
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
