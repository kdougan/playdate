import { personSubscriptionsQuery } from './graphql';
import { qfetch } from './common';

export const subscriptionService = {
  getSubscriptions,
};

function getSubscriptions(id) {
  return qfetch(personSubscriptionsQuery(id)).then(({ data }) => {
    const subs = data.personByPk;
    const rtn = { calendars: [], events: [] };
    subs.calendarSubscriptions.subscriptions.forEach((item) => {
      rtn.calendars.push({
        meta: item.subscription.meta,
        calendarId: item.subscription.calendar.pk,
        person: {
          id: item.subscription.calendar.owner.pk,
          handle: item.subscription.calendar.owner.handle,
          asset: item.subscription.calendar.owner.asset,
        },
      });
    });
    subs.eventSubscriptions.subscriptions.forEach((item) => {
      rtn.events.push({
        meta: item.subscription.meta,
        eventId: item.subscription.event.pk,
        person: {
          id: item.subscription.event.calendar.owner.pk,
          handle: item.subscription.event.calendar.owner.handle,
          asset: item.subscription.event.calendar.owner.asset,
        },
      });
    });
    return rtn;
  });
}
