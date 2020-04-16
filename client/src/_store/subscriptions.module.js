import { subscriptionService } from '../_services';

export const subscriptions = {
  namespaced: true,
  state: {
    subscriptions: {},
  },
  getters: {
    subscriptions: (state) => state.subscriptions,
  },
  mutations: {
    getSubscriptionsRequest(state) {
      state.subscriptions = { loading: true };
    },
    getSubscriptionsSuccess(state, subscriptions) {
      state.subscriptions = { items: subscriptions };
    },
    getSubscriptionsFailure(state, error) {
      state.subscriptions = { error };
    },
  },
  actions: {
    getSubscriptions({ commit }, id) {
      commit('getSubscriptionsRequest');
      subscriptionService.getSubscriptions(id).then(
        (subscriptions) => commit('getSubscriptionsSuccess', subscriptions),
        (error) => commit('getSubscriptionsFailure', error)
      );
    },
  },
};
