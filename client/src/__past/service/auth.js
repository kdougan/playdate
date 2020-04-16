import { HTTP, graphql } from './common';

export default {
  login: (email, password, success = null, error = null) => {
    HTTP.post(`/v1/auth/login`, { email, password })
      .then(response => {
        if (success) success(response);
      })
      .catch(e => {
        console.log('auth:login:error', e);
        if (error) error(e);
      });
  },
  checkAuth: (success = null, error = null) => {
    HTTP.post('/v1/auth/verify')
      .then(response => {
        if (success) success(response);
      })
      .catch(e => {
        console.log('auth:checkAuth:error', e);
        if (error) error(e);
      });
  },
  getConfig: (success = null, error = null) => {
    HTTP.get('/v1/config')
      .then(response => {
        if (success) success(response);
      })
      .catch(e => {
        console.log('auth:getConfig:error', e);
        if (error) error(e);
      });
  },
  getGraphqlConfig: (email, success = null, error = null) => {
    console.log(`getGraphqlConfig: ${email}`);
    graphql(
      {
        query: `query ($email: String!)
        {
          getPerson(email: $email) {
            id
            pk
            name
            email
            meta
            calendarSubscriptions {
              subscription: edges {
                subscription: node {
                  meta
                  calendar {
                    id
                    pk
                  }
                  person {
                    id
                    pk
                    handle
                  }
                }
              }
            }
            eventSubscriptions {
              subscription: edges {
                subscription: node {
                  meta
                  event {
                    id
                    pk
                  }
                  person {
                    id
                    pk
                    handle
                  }
                }
              }
            }
          }
        }`,
        variables: {
          email: 'kdougan@gmail.com'
        }
      },
      data => {
        success(data);
      },
      e => {
        error(e);
      }
    );
  }
};
