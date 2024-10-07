import Vue from 'vue';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import fab from 'vue-fab';
import App from './App.vue';
import router from './router';
import store from './store';
import midiServices from './services/midi';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
const VueSelect = {
  install(Vue, options) {
    Vue.component('vue-fab', fab);
  },
};
Vue.use(VueSelect);
const app = new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
