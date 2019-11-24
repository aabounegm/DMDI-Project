import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
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
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/doctors',
      name: 'doctors',
      component: () => import('../views/Doctors.vue'),
    },
    {
      path: '/patients',
      name: 'patients',
      component: () => import('../views/Patients.vue'),
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('../views/Statistics.vue'),
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
      component: () => import('../views/Reports.vue'),
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
