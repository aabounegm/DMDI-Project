import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Doctors from '../views/Doctors.vue';
import Reports from '../views/Reports.vue';
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
