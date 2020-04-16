import { createApolloFetch } from 'apollo-fetch';
import { authHeader } from '../_helpers';
import { store } from '../_store';

export const qfetch = createApolloFetch({
  uri: '/graphql',
});

qfetch.use(({ options }, next) => {
  if (!options.headers) {
    options.headers = {}; // Create the headers object if needed.
  }
  options = { ...options, ...authHeader };

  next();
});
qfetch.useAfter(({ response }, next) => {
  if (response.status === 401) {
    store.dispatch('authentication/logout');
  }
  next();
});
