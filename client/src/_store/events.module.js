import { eventService } from '../_services';

export const events = {
  namespaced: true,
  state: {
    event: {},
    events: {},
  },
  getters: {
    event: (state) => state.event,
    events: (state) => state.events,
  },
  mutations: {
    getEventRequest(state) {
      state.event = { loading: true };
    },
    getEventSuccess(state, event) {
      state.event = { item: event };
    },
    getEventFailure(state, error) {
      state.event = { error };
    },
    clearEvent(state) {
      state.event = {};
    },
    getEventsRequest(state) {
      state.events = { loading: true };
    },
    getEventsSuccess(state, events) {
      state.events = { items: events };
    },
    getEventsFailure(state, error) {
      state.events = { error };
    },
  },
  actions: {
    getEvents({ commit }, arg) {
      commit('getEventsRequest');
      eventService.getEvents(arg.startTime, arg.endTime, arg.personId).then(
        (events) => commit('getEventsSuccess', events),
        (error) => commit('getEventsFailure', error)
      );
    },
    getEvent({ commit }, id) {
      commit('getEventRequest');
      eventService.getEvent(id).then(
        (event) => commit('getEventSuccess', event),
        (error) => commit('getEventFailure', error)
      );
    },
    clearEvent({ commit }) {
      commit('clearEvent');
    },
  },
};
