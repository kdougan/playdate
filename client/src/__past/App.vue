<template>
  <b-container id="app" class="app" fluid>
    <Auth v-if="!isAuthenticated" />
    <b-container v-else class="app-layout" fluid>
      <Navbar class="app-navbar" />
      <b-container class="app-content" fluid>
        <CalendarRoute />
        <modals-container />
      </b-container>
    </b-container>
  </b-container>
</template>

<script>
import Auth from '@/components/Auth';
import Navbar from '@/components/layout/Navbar';
import CalendarRoute from '@/components/layout/CalendarRoute';

import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'App',
  components: {
    Auth,
    Navbar,
    CalendarRoute
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  methods: {
    ...mapActions(['checkAuth'])
  },
  created() {
    this.checkAuth();
  }
};
</script>

<style lang="scss">
@import url('https://use.fontawesome.com/releases/v5.0.6/css/all.css');

@import './style/_variables';
@import './style/_tooltip';

*,
*:before,
*:after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {
  width: 100%;
  height: 100%;
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
    background-color: rgba($purple, 0.6) !important;
  }

  *::-webkit-scrollbar-thumb:hover {
    background-color: rgba($purple, 1) !important;
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
  overflow: hidden;

  .app-layout {
    padding: 0;
    display: grid;
    grid-template-rows: 3rem 1fr;
    height: 100%;

    .app-navbar {
      padding: 0;
    }

    .app-content {
      padding: 0;
      height: 100%;
      overflow: hidden;
      position: relative;
    }
  }

  .v--modal-overlay {
    position: absolute;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
  }

  .event-modal-container {
    background-color: black;
    overflow: hidden;
    padding: 0;
    position: absolute !important;
    height: auto !important;
    bottom: 0 !important;
    box-shadow: 0 0 2rem -1rem black, 0 0 0 1px rgba(black, 0.2);
  }

  .scale-enter-active,
  .scale-leave-active {
    transition: all 0.25s ease-out;
  }

  .scale-enter,
  .scale-leave-active {
    opacity: 0;
    transform: translateX(580px);
    width: 0;
  }
}
</style>
