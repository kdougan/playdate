import { personService } from '../_services';
import { router, jwtLocalStorageKey } from '../_helpers';

const person = JSON.parse(localStorage.getItem(jwtLocalStorageKey));
const initialState = person
  ? { status: { loggedIn: true }, person }
  : { status: {}, person: null };

export const authentication = {
  namespaced: true,
  state: initialState,
  getters: {
    person: state => state.person,
    loggedIn: state => state.status.loggedIn,
    loggingIn: state => state.status.loggingIn
  },
  actions: {
    login({ dispatch, commit }, { email, password }) {
      commit('loginRequest', { email });

      personService.login(email, password).then(
        person => {
          commit('loginSuccess', person);
          router.push('/');
        },
        error => {
          commit('loginFailure', error);
          dispatch('alert/error', error, { root: true });
        }
      );
    },
    logout({ commit }) {
      personService.logout();
      commit('logout');
    }
  },
  mutations: {
    loginRequest(state, person) {
      state.status = { loggingIn: true };
      state.person = person;
    },
    loginSuccess(state, person) {
      state.status = { loggedIn: true };
      state.person = person;
    },
    loginFailure(state) {
      state.status = {};
      state.person = null;
    },
    logout(state) {
      state.status = {};
      state.person = null;
    }
  }
};
