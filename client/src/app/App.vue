<template>
  <div class="app">
    <div v-if="alert.message" :class="`alert ${alert.type}`">{{ alert.message }}</div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
export default {
  name: 'app',
  computed: {
    ...mapGetters({
      alert: 'alert/alert'
    })
  },
  methods: {
    ...mapActions({
      clearAlert: 'alert/clear'
    })
  },
  watch: {
    $route() {
      this.clearAlert();
    }
  }
};
</script>

<style lang="scss">
@import url('https://use.fontawesome.com/releases/v5.0.6/css/all.css');

@import '@/style/_variables';
@import '@/style/_tooltip';

html,
body {
  width: 100%;
  height: 100%;
  background-color: $body-bg;
  overflow: hidden;
}
body {
  *::-webkit-scrollbar {
    width: 0.5rem !important;
    height: 0.5rem !important;
  }

  *::-webkit-scrollbar-track {
    background-color: rgba(black, 0.2) !important;
  }

  *::-webkit-scrollbar-thumb {
    background-color: rgba($green, 0.6) !important;
  }

  *::-webkit-scrollbar-thumb:hover {
    background-color: rgba($green, 1) !important;
  }

  *::-webkit-scrollbar-button {
    display: none !important;
  }
}

.app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: $body-color;
  background-color: $body-bg;
  position: absolute;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0 !important;
}
</style>
