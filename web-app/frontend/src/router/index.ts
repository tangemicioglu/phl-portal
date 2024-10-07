import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import store from '@/store';
import Home from '../views/Home.vue';
import Auth from '../views/Auth.vue';
import Score from '../views/Score.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth,
  },
  {
    path: '/score/:id',
    name: 'Score',
    component: Score,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeResolve((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/auth'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = store.getters['auth/isUserLoggedIn'];
  if (authRequired && !loggedIn) {
    return next('/auth');
  }
  return next();
});

export default router;
