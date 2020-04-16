<template>
  <b-container class="calendar-view" fluid>
    <div class="calendar-wrapper">
      <Fullcalendar
        ref="fullCalendar"
        :plugins="calendarPlugins"
        class="table-dark"
        :header="{
          left: '',
          center: 'title',
          right: '',
        }"
        :selectable="mode == 'create'"
        :events="processedEvents"
        :datesRender="renderDates"
        @select="handleSelect"
        @eventClick="handleClick"
      />
    </div>
    <eventViewModal />
  </b-container>
</template>

<script>
import Fullcalendar from '@fullcalendar/vue';
import Bootstrap from '@fullcalendar/bootstrap';
import DayGridPlugin from '@fullcalendar/daygrid';
import TimeGridPlugin from '@fullcalendar/timegrid';
import InteractionPlugin from '@fullcalendar/interaction';
import ListPlugin from '@fullcalendar/list';

import EventViewModal from './EventViewModal';

import { mapGetters, mapActions } from 'vuex';
export default {
  data: () => ({
    calendarPlugins: [
      Bootstrap,
      DayGridPlugin,
      InteractionPlugin,
      ListPlugin,
      TimeGridPlugin,
    ],
    mode: 'view',
  }),
  components: { Fullcalendar, EventViewModal },
  computed: {
    ...mapGetters({
      person: 'authentication/person',
      subscriptions: 'subscriptions/subscriptions',
      events: 'events/events',
    }),
    subscriptionsColors() {
      if (!this.subscriptions.items) return {};
      const subs = { calendars: {}, events: {} };
      this.subscriptions.items.calendars.forEach((sub) => {
        subs.calendars[sub.person.id] = sub.meta.color;
      });
      this.subscriptions.items.events.forEach((sub) => {
        subs.events[sub.event.id] = sub.meta.color;
      });
      return subs;
    },
    processedEvents() {
      if (!this.events.items) return [];
      return this.events.items.map((event) => {
        if (event.ownerId in this.subscriptionsColors.calendars) {
          event.color = this.subscriptionsColors.calendars[event.ownerId];
        } else if (event.id in this.subscriptionsColors.events)
          event.color = this.subscriptionsColors.events[event.id];
        return event;
      });
    },
  },
  methods: {
    ...mapActions({
      getEvent: 'events/getEvent',
      getEvents: 'events/getEvents',
    }),
    handleSelect(arg) {
      console.log('handleSelect:arg', arg);
    },
    handleClick(arg) {
      this.getEvent(arg.event.id);
    },
    renderDates(arg) {
      this.getEvents({
        startTime: arg.view.activeStart,
        endTime: arg.view.activeEnd,
        personId: this.person.id,
      });
    },
  },
};
</script>

<style lang="scss">
@import '~@fullcalendar/core/main.min';
@import '~@fullcalendar/daygrid/main.min';
@import '~@fullcalendar/timegrid/main.min';
@import '~@fullcalendar/bootstrap/main';

@import '@/style/_variables';

.calendar-view {
  padding: 1rem;
  box-shadow: 0 0.5rem 2rem -0.75rem $black;
  background-color: $gray-900;
  z-index: 1;
  height: 100vh;
  position: relative;

  .calendar-wrapper {
    height: 100%;
    padding: 2rem;
    overflow: hidden;
    overflow-y: auto;
  }

  .fc {
    background-color: transparent;
    .fc-head {
      td,
      th {
        border: none;
      }
    }
    .fc-event {
      background-color: darken($green, 20%);
      border-color: $green;
      cursor: pointer;
    }
    .fc-today.fc-day-top {
      color: black;
      font-weight: 600;
    }
    .fc-today:not(.fc-day-top) {
      position: relative;
      background-color: transparent;
      box-shadow: inset 0 0 0 1px $green;

      &:after {
        position: absolute;
        display: block;
        right: 0;
        width: 0;
        height: 0;
        content: '';
        border-top: 2.5rem solid $green;
        border-left: 2.5rem solid transparent;
      }
    }
  }
}
</style>
