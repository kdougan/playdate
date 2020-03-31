<template>
  <div class="calendar">
    <Fullcalendar
      ref="fullCalendar"
      :plugins="calendarPlugins"
      :themeSystem="'bootstrap'"
      :header="{
        left: 'prev today next',
        center: 'title',
        right: 'dayGridMonth, timeGridWeek, timeGridDay, listWeek',
      }"
      :selectable="true"
      :events="events"
      :datesRender="renderDates"
      @select="handleSelect"
      @eventClick="handleClick"
    />
    <modals-container />
  </div>
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

import events from '@/service/events';
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    calendarPlugins: [
      Bootstrap,
      DayGridPlugin,
      InteractionPlugin,
      ListPlugin,
      TimeGridPlugin,
    ],
    modalProps: {
      adaptive: true,
      height: 'auto',
      scrollable: true,
      classes: ['event-modal-container'],
    },
    start_time: 'asd',
  }),
  components: { Fullcalendar },
  computed: {
    ...mapGetters(['events']),
  },
  methods: {
    handleSelect(arg) {
      this.$modal.show(
        CreateEventModal,
        {
          save: this.save,
          event: arg,
        },
        this.modalProps
      );
    },
    handleClick(arg) {
      this.$modal.show(
        ViewEventModal,
        {
          text: 'this is from the component',
          event: arg.event,
        },
        this.modalProps
      );
    },
    renderDates(arg) {
      events.getEvents(arg.view.activeStart, arg.view.activeEnd);
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

.calendar,
.event-modal-container {
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 2rem -1rem black;
  background-color: $gray-800;
}

.fc-event {
  background-color: $purple;
  border-color: $purple;
}
.alert-info {
  background-color: rgba($purple, 0.25) !important;
}
</style>
