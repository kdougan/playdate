import { HTTP } from './common';
import store from '../store/store';

export default {
  login: (username, password, success = null, error = null) => {
    HTTP.post(`/v1/auth/login`, { username, password })
      .then(response => {
        store.commit('SET_TOKEN', response.data.access_token);
        if (success) success(response);
      })
      .catch(e => {
        console.log('auth:login:error', e);
        if (error) error(e);
      });
  },
  checkAuth: (success = null, error = null) => {
    const token = localStorage.getItem('playDate:jwt');
    store.commit('SET_TOKEN', token);
    HTTP.post('/v1/auth/verify')
      .then(response => {
        store.commit('SET_AUTHENTICATED');
        if (success) success(response);
      })
      .catch(e => {
        console.log('auth:checkAuth:error', e);
        store.commit('CLEAR_AUTHENTICATED');
        if (error) error(e);
      });
  },
};
