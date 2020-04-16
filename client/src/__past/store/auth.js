import { HTTP } from '../service/common';

import service from '../service';

const setHeaders = (token = null) => {
  if (token) HTTP.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  else HTTP.defaults.headers.common['Authorization'] = null;
};
const getStoredToken = () => localStorage.getItem('playDate:jwt');

export default {
  state: {
    storedToken: getStoredToken(),
    authenticated: false,
    token: null,
    refreshToken: null,
    config: {}
  },
  getters: {
    isAuthenticated: state => state.authenticated == true,
    token: state => state.token,
    refreshToken: state => state.refreshToken,
    config: state => state.config
  },
  mutations: {
    SET_AUTHENTICATED: state => (state.authenticated = true),
    CLEAR_AUTHENTICATED: state => (state.authenticated = false),
    SET_TOKEN: (state, token) => (state.token = token),
    CLEAR_TOKEN: state => (state.token = null),
    SET_CONFIG: (state, config) => (state.config = config)
  },
  actions: {
    setAuthToken: ({ commit }, token) => {
      localStorage.setItem('playDate:jwt', token);
      commit('SET_TOKEN', token);
      commit('SET_AUTHENTICATED', true);
      setHeaders(token);
    },
    clearAuthToken: ({ commit }) => {
      localStorage.removeItem('playDate:jwt');
      commit('CLEAR_AUTHENTICATED');
      commit('CLEAR_TOKEN');
      setHeaders();
    },
    login: ({ dispatch }, kwargs) => {
      service.auth.login(kwargs.email, kwargs.password, response => {
        dispatch('setAuthToken', response.data.access_token);
        dispatch('getConfig');
      });
    },
    checkAuth: ({ dispatch }) => {
      setHeaders(getStoredToken());
      service.auth.checkAuth(
        () => {
          dispatch('setAuthToken', getStoredToken());
          dispatch('getConfig');
          dispatch('getGraphqlConfig');
        },
        () => dispatch('clearAuthToken')
      );
    },
    getConfig: ({ commit }) => {
      console.log('getConfig');
      service.auth.getConfig(response => commit('SET_CONFIG', response.data));
    },
    getGraphqlConfig: () => {
      console.log('getGraphqlConfig');
      service.auth.getGraphqlConfig(data => console.log(data));
    }
  }
};
