import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Doctors from '../views/Doctors.vue';
import Patients from '../views/Patients.vue';
import Reports from '../views/Reports.vue';
import Stats from '../views/Statistics.vue';
import store from '../store/index';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/doctors',
      name: 'doctors',
      component: Doctors,
    },
    {
      path: '/patients',
      name: 'patients',
      component: Patients,
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: Stats,
      beforeEnter(from, to, next) {
        if (store.state.currentUser == null || store.state.userType !== 'doctor') {
          next('/login');
        }
        next();
      },
    },
    {
      path: '/reports',
      name: 'Reports',
      component: Reports,
      beforeEnter(from, to, next) {
        if (store.state.currentUser == null) {
          next('/login');
        }
        next();
      },
    },
  ],
});

export default router;
