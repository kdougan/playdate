import Vue from 'vue';

import { store } from './_store';
import { router } from './_helpers';
import App from './app/App';

import VueModal from 'vue-js-modal';
import VueMoment from 'vue-moment';
import VTooltip from 'v-tooltip';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';

import 'vue-loading-overlay/dist/vue-loading.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false;

Vue.use(VueModal, { dynamic: true, dialog: true });
Vue.use(VueMoment);
Vue.use(VTooltip, { defaultBoundariesElement: document.body });
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app');
