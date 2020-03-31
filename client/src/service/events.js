import Vue from 'vue';
import { HTTP } from './common';
import store from '../store/store';

export default {
  getEvents(startTime, endTime, success, error) {
    const st = Vue.moment(startTime).format('YYYY-MM-DD HH:mm:ss');
    const et = Vue.moment(endTime).format('YYYY-MM-DD HH:mm:ss');
    HTTP.get(`/v1/event?start_time=${st}&end_time=${et}`)
      .then(response => {
        store.commit('CLEAR_EVENTS');
        response.data.forEach(event => {
          store.commit('ADD_EVENT', {
            id: event._id.$oid,
            title: event.title,
            start: event.start_time.$date,
            end: event.end_time.$date,
            duration: event.duration,
          });
        });
        if (success) success(response);
      })
      .catch(e => {
        console.log('events:getEvents:error', e);
        if (error) error(e);
      });
  },
  createEvent(event, success, error) {
    const payload = {
      description: event.description,
      duration: event.duration,
      start_time: event.start_time,
      title: event.title,
    };
    console.log('events:createEvent:event', event);
    console.log('events:createEvent:payload', payload);
    HTTP.post(`/v1/event`, payload)
      .then(response => {
        const event = response.data;
        store.commit('ADD_EVENT', {
          id: event._id.$oid,
          title: event.title,
          start: event.start_time.$date,
          end: event.end_time.$date,
          duration: event.duration,
        });
        if (success) success(event);
      })
      .catch(e => {
        console.log('events:createEvent:error', e);
        if (error) error(e);
      });
  },
};
