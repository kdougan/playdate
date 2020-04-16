import Vue from 'vue';
import { qfetch } from './common';

import { eventsForRangeAndPerson, eventForPk } from './graphql';

export const eventService = {
  getEvents,
  getEvent,
};

function getEvents(startTime, endTime, personId) {
  return qfetch(eventsForRangeAndPerson(startTime, endTime, personId)).then(
    ({ data }) => {
      const rtn = [];
      data.eventRangeForPerson.forEach((event) => {
        rtn.push({
          id: event.pk,
          title: event.title,
          start: Vue.moment.utc(event.startTime).toDate(),
          end: Vue.moment.utc(event.endTime).toDate(),
          ownerId: event.calendar.owner.pk,
        });
      });
      return rtn;
    }
  );
}

function getEvent(id) {
  return qfetch(eventForPk(id)).then(({ data }) => {
    const event = data.eventForPk;
    const rtn = {
      id: event.pk,
      title: event.title,
      description: event.description,
      asset: event.asset,
      startTime: event.startTime,
      endTime: event.endTime,
      duration: event.duration,
      meta: event.meta,
      owner: {
        id: event.calendar.owner.pk,
        handle: event.calendar.owner.handle,
        asset: event.calendar.owner.asset,
      },
      groups: [],
      subscribers: [],
    };
    event.groups.edges.forEach((edge) =>
      rtn.groups.push({
        id: edge.node.pk,
        slotCount: edge.node.slotCount,
        meta: edge.node.meta,
        members: edge.node.members.edges.map((edge) => ({
          meta: edge.node.meta,
          created: edge.node.created,
          id: edge.node.person.pk,
          handle: edge.node.person.handle,
          asset: edge.node.person.asset,
        })),
      })
    );
    event.calendar.subscribers.edges.forEach((edge) => {
      rtn.subscribers.push(edge.node.person.handle);
    });
    event.subscribers.edges.forEach((edge) => {
      rtn.subscribers.push(edge.node.person.handle);
    });
    return rtn;
  });
}
