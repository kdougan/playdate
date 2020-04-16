import Vue from 'vue';
import service from '../service';
export default {
  state: {
    event: null,
    events: [],
    eventData: {},
    disabledSubs: [],
    isLoadingEvents: false,
    isLoadingEvent: false
  },
  getters: {
    event: state => state.event,
    events: state => {
      return state.events.filter(
        e => !state.disabledSubs.includes(state.eventData[e.id])
      );
    },
    eventData: state => state.eventData,
    isLoadingEvents: state => state.isLoadingEvents,
    isLoadingEvent: state => state.isLoadingEvent
  },
  mutations: {
    SET_IS_LOADING_EVENT: state => {
      state.isLoadingEvent = true;
    },
    CLEAR_IS_LOADING_EVENT: state => {
      state.isLoadingEvent = false;
    },
    CLEAR_EVENT: state => {
      state.event = null;
    },
    SET_EVENT: (state, event) => {
      state.event = event;
    },
    SET_IS_LOADING_EVENTS: state => {
      state.isLoadingEvents = true;
    },
    CLEAR_IS_LOADING_EVENTS: state => {
      state.isLoadingEvents = false;
    },
    CLEAR_EVENTS: state => {
      state.events = [];
    },
    ADD_EVENT: (state, event) => {
      state.events.push(event);
      state.eventData[event.id] = event;
    }
  },
  actions: {
    clearEvent({ commit }) {
      commit('CLEAR_EVENT');
    },
    getEvent({ commit }, payload) {
      console.log('getEvent');
      commit('SET_IS_LOADING_EVENT');
      service.event.getOne(
        payload.eventId,
        event => {
          commit('SET_EVENT', event);
          commit('CLEAR_IS_LOADING_EVENT');
        },
        () => {
          commit('CLEAR_IS_LOADING_EVENT');
        }
      );
    },
    getEvents({ commit }, payload) {
      commit('SET_IS_LOADING_EVENTS');
      service.event.getMany(
        payload.startTime,
        payload.endTime,
        events => {
          commit('CLEAR_EVENTS');
          events.forEach(event => {
            commit('ADD_EVENT', {
              id: event.id,
              title: event.title,
              start: Vue.moment.utc(event.start_time).toDate(),
              end: Vue.moment.utc(event.end_time).toDate(),
              meta: event,
              color: event.color
            });
          });
          commit('CLEAR_IS_LOADING_EVENTS');
        },
        () => {
          commit('CLEAR_IS_LOADING_EVENTS');
        }
      );
    },
    createEvent({ commit }, event) {
      const payload = {
        description: event.description,
        duration: event.duration,
        start_time: Vue.moment(event.start_time)
          .utc()
          .format('YYYY-MM-DD HH:mm:ss'),
        title: event.title
      };
      service.event.create(payload, event => {
        commit('ADD_EVENT', {
          id: event.id,
          title: event.title,
          start: Vue.moment.utc(event.start_time).toDate(),
          end: Vue.moment.utc(event.end_time).toDate(),
          duration: event.duration,
          description: event.description
        });
      });
    }
  }
};
