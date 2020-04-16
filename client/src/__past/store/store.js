import Vue from 'vue';
import Vuex from 'vuex';

import event from './event';
import auth from './auth';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    subSidebarCollapse: false,
  },
  getters: {
    subSidebarCollapse: state => state.subSidebarCollapse,
  },
  mutations: {
    TOGGLE_SUB_SIDEBAR: state => {
      state.subSidebarCollapse = !state.subSidebarCollapse;
    },
  },
  actions: {
    toggleSubSidebar({ commit }) {
      commit('TOGGLE_SUB_SIDEBAR');
    },
  },
  modules: {
    auth,
    event,
  },
});

export default store;
