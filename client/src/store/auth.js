import { HTTP } from '../service/common';

const setHeaders = (token = null) => {
  if (token) HTTP.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  else HTTP.defaults.headers.common['Authorization'] = null;
};

export default {
  state: {
    authenticated: false,
    token: null,
  },
  getters: {
    isAuthenticated: state => state.authenticated == true,
    token: state => state.token,
  },
  mutations: {
    SET_AUTHENTICATED: state => (state.authenticated = true),
    SET_TOKEN: (state, token) => {
      localStorage.setItem('playDate:jwt', token);
      state.token = token;
      state.authenticated = true;
      setHeaders(token);
    },
    CLEAR_AUTHENTICATED: state => {
      localStorage.removeItem('playDate:jwt');
      state.authenticated = false;
      state.token = null;
      setHeaders();
    },
  },
  actions: {},
};
