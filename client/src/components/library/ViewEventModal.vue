<template>
  <div class="event-modal">
    <fieldset>
      <legend>Event Details</legend>
      <p><b>ID:</b> {{ event.id }}</p>
      <p><b>Title:</b> {{ event.title }}</p>
      <p><b>Start:</b> {{ event.start }}</p>
      <p><b>End:</b> {{ event.end }}</p>
    </fieldset>
    <br />
    <fieldset>
      <legend>Edit Event</legend>
      <p>
        <label for=""
          >Title
          <input v-model="title" type="text" />
        </label>
      </p>
      <p>
        <label for=""
          >Start
          <input v-model="start" type="date" />
        </label>
      </p>
      <p>
        <label for=""
          >Duration
          <input v-model="duration" type="number" />
        </label>
      </p>
    </fieldset>
  </div>
</template>

<script>
export default {
  data: () => ({
    id: '',
    title: '',
    start: {},
    end: {},
    duration: 0,
  }),
  props: {
    text: String,
    event: Object,
  },
  mounted() {
    this.id = this.event.id;
    this.title = this.event.title;
    this.start = this.event.start;
    this.end = this.event.end;
    this.duration = this.event.duration;
  },
};
</script>

<style lang="scss">
.event-modal {
  margin: 2rem;
}
</style>
