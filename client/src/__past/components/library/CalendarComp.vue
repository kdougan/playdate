<template>
  <b-container class="calendar-container" fluid>
    <Fullcalendar
      ref="fullCalendar"
      :plugins="calendarPlugins"
      class="table-dark"
      :header="{
        left: '',
        center: 'title',
        right: ''
      }"
      :selectable="mode == 'create'"
      :events="events"
      :datesRender="renderDates"
      @select="handleSelect"
      @eventClick="handleClick"
    />
  </b-container>
</template>

<script>
import Fullcalendar from '@fullcalendar/vue';
import Bootstrap from '@fullcalendar/bootstrap';
import DayGridPlugin from '@fullcalendar/daygrid';
import TimeGridPlugin from '@fullcalendar/timegrid';
import InteractionPlugin from '@fullcalendar/interaction';
import ListPlugin from '@fullcalendar/list';

import ViewEventModal from './ViewEventModal';
import CreateEventModal from './CreateEventModal';

import { mapGetters, mapActions } from 'vuex';

export default {
  data: () => ({
    calendarPlugins: [
      Bootstrap,
      DayGridPlugin,
      InteractionPlugin,
      ListPlugin,
      TimeGridPlugin
    ],
    modalProps: {
      adaptive: true,
      height: '100%',
      pivotX: 1,
      width: '580',
      classes: ['event-modal-container'],
      transition: 'scale'
    },
    mode: 'view'
  }),
  components: { Fullcalendar },
  computed: {
    ...mapGetters(['events', 'eventData', 'subSidebarCollapse', 'event'])
  },
  watch: {
    subSidebarCollapse() {
      this.$refs.fullCalendar.getApi().updateSize();
    },
    event() {
      if (this.event) {
        this.$modal.show(
          ViewEventModal,
          {
            event: this.event
          },
          {
            ...this.modalProps,
            'before-close': () => {
              this.clearEvent();
            }
          }
        );
      }
    }
  },
  methods: {
    ...mapActions(['getEvents', 'getEvent']),
    handleSelect(arg) {
      this.$modal.show(
        CreateEventModal,
        {
          save: this.save,
          event: arg
        },
        this.modalProps
      );
    },
    handleClick(arg) {
      this.getEvent({ eventId: arg.event.id });
    },
    renderDates(arg) {
      this.getEvents({
        startTime: arg.view.activeStart,
        endTime: arg.view.activeEnd
      });
    }
  }
};
</script>

<style lang="scss">
@import '~@fullcalendar/core/main.min';
@import '~@fullcalendar/daygrid/main.min';
@import '~@fullcalendar/timegrid/main.min';
@import '~@fullcalendar/bootstrap/main';

@import '@/style/_variables';

.calendar-container {
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 2rem -0.75rem $black;
  background-color: $gray-800;

  .fc {
    background-color: transparent;
    .fc-head {
      td,
      th {
        border: none;
      }
    }
    .fc-event {
      background-color: darken($purple, 10%);
      border-color: $purple;
      cursor: pointer;
    }
    .fc-today:not(.fc-day-top) {
      background-color: rgba($purple, 0.1);
      box-shadow: inset 0 0 0.5rem 1px $purple;
    }
  }
}
</style>
