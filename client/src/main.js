import Vue from 'vue';
import App from './App.vue';
import store from './store/store';

import VueModal from 'vue-js-modal';
import VueMoment from 'vue-moment';

Vue.config.productionTip = false;

Vue.use(VueModal, { dynamic: true, dialog: true });
Vue.use(VueMoment);

new Vue({
  render: h => h(App),
  store,
}).$mount('#app');
