import Vue from 'vue';
import Vuex from 'vuex';

import auth from './auth';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    events: [],
  },
  getters: {
    events: state => state.events,
  },
  mutations: {
    CLEAR_EVENTS: state => {
      state.events = [];
    },
    ADD_EVENT: (state, event) => {
      console.log('store:ADD_EVENT', event);
      state.events.push(event);
    },
  },
  actions: {},
  modules: {
    auth,
  },
});

export default store;
