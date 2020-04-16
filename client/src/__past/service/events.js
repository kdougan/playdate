import Vue from 'vue';

import { HTTP } from './common';

const path = '/v1/event';

export default {
  getMany(startTime, endTime, success, error) {
    const st = Vue.moment(startTime).format('YYYY-MM-DD HH:mm:ss');
    const et = Vue.moment(endTime).format('YYYY-MM-DD HH:mm:ss');
    HTTP.get(`${path}?start_time=${st}&end_time=${et}`)
      .then(response => {
        if (success) success(response.data);
      })
      .catch(e => {
        console.log('events:getMany:error', e);
        if (error) error(e);
      });
  },
  getOne(eventId, success, error) {
    HTTP.get(`${path}/${eventId}`)
      .then(response => {
        if (success) success(response.data);
      })
      .catch(e => {
        console.log('events:create:error', e);
        if (error) error(e);
      });
  },
  create(event, success, error) {
    HTTP.post(`${path}`, event)
      .then(response => {
        if (success) success(response.data);
      })
      .catch(e => {
        console.log('events:create:error', e);
        if (error) error(e);
      });
  }
};
