<template>
  <div class="home-view">
    <sidebar />
    <calendar />
  </div>
</template>

<script>
import Sidebar from './components/Sidebar';
import Calendar from './components/Calendar';
export default {
  components: {
    Sidebar,
    Calendar,
  },
  computed: {},
  methods: {},
};
</script>

<style lang="scss">
.home-view {
  overflow: hidden;
  display: grid;
  grid-template-columns: 5rem 1fr;
  height: 100%;
  position: relative;
}
</style>
