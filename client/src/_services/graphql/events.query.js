export const eventsForRangeAndPerson = (startTime, endTime, personId) => ({
  query: `query ($startTime:DateTime!, $endTime:DateTime!, $personId:Int!)
  {
    eventRangeForPerson(
      startTime: $startTime,
      endTime: $endTime,
      personId: $personId
    ) {
      id
      pk
      title
      startTime
      endTime
      calendar {
        owner {
          id
          pk
        }
      }
    }
  }`,
  variables: {
    startTime,
    endTime,
    personId,
  },
});

export const eventForPk = (id) => ({
  query: `query ($id: Int!)
  {
    eventForPk(id: $id) {
      id
      pk
      title
      description
      asset
      startTime
      endTime
      duration
      groups {
        edges {
          node {
            id
            pk
            slotCount
            meta
            members {
              edges {
                node {
                  meta
                  created
                  person {
                    id
                    pk
                    handle,
                    asset
                  }
                }
              }
            }
          }
        }
      }
      calendar {
        owner {
          id
          pk
          handle
          asset
        }
        subscribers {
          edges {
            node {
              person {
                id
                pk
                handle
              }
            }
          }
        }
      }
      subscribers {
        edges {
          node {
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
    id,
  },
});
