<template>
  <div class="event-modal">
    <form id="create-event-form" @submit="createEvent">
      <h2>New Event</h2>
      <p>
        <label for="title">Title</label>
        <input id="title" v-model="title" type="text" />
      </p>
      <p>
        <label for="description">Description</label>
        <textarea id="description" v-model="description" type="text" />
      </p>
      <p>
        <label for="date">Date</label>
        <input id="date" v-model="date" type="date" />
      </p>
      <p>
        <label for="time">Start Time</label>
        <input id="time" v-model="time" type="time" />
      </p>
      <p>
        <label for="duration">Duration</label>
        <span id="duration">
          <label for="hours">Hours</label>
          <input id="hours" v-model="hours" type="number" />
          <label for="minutes">Minutes</label>
          <input id="minutes" v-model="minutes" type="number" />
        </span>
      </p>
      <input type="submit" @click="createEvent" value="Create" />
      <input type="button" @click="$emit('close')" value="Cancel" />
    </form>
  </div>
</template>

<script>
import Vue from 'vue';
import eventService from '@/service/events';
export default {
  data: () => ({
    title: '',
    description: '',
    date: '',
    time: '',
    hours: 0,
    minutes: 0,
    private: false,
    errors: [],
  }),
  props: {
    save: Function,
    event: Object,
  },
  methods: {
    createEvent(e) {
      e.preventDefault();
      ['title', 'date', 'time'].forEach(key => {
        if (!this[key]) this.errors.push(key);
      });
      const duration = parseInt(this.hours) * 60 + parseInt(this.minutes);
      if (duration <= 0) this.errors.push('duration');
      if (this.errors.length > 0) return false;
      eventService.createEvent(
        {
          description: this.description,
          duration: duration,
          start_time: `${this.date} ${this.time}:00`,
          title: this.title,
        },
        () => {
          this.$emit('close');
        }
      );
    },
  },
  mounted() {
    const start = Vue.moment(this.event.start);
    const end = Vue.moment(this.event.end);
    const minutes = Vue.moment.duration(end.diff(start)).asMinutes();
    this.date = start.format('YYYY-MM-DD');
    this.time = start.format('hh:mm');
    this.hours = Math.floor(minutes / 60);
    this.minutes = minutes % 60;
  },
};
</script>

<style lang="scss">
.event-modal {
  margin: 2rem;
  text-align: left;

  label {
    display: block;
  }
  input,
  textarea {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 0.25rem;
    margin-bottom: 0.5rem;
    width: 100%;
    box-sizing: border-box;
    font-family: montserrat;
    color: #2c3e50;
    font-size: 16pt;
  }
}
</style>
