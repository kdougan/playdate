export const personSubscriptionsQuery = (id) => ({
  query: `query ($id: Int!)
  {
    personByPk(id: $id) {
      id
      pk
      name
      email
      handle
      meta
      calendarSubscriptions {
        subscriptions: edges {
          subscription: node {
            meta
            calendar {
              id
              pk
              owner {
                id
                pk
                handle
                asset
              }
            }
          }
        }
      }
      eventSubscriptions {
        subscriptions: edges {
          subscription: node {
            meta
            event {
              id
              pk
              calendar {
                owner {
                  id
                  pk
                  handle
                  asset
                }
              }
            }
          }
        }
      }
    }
  }`,
  variables: {
    id,
  },
});
