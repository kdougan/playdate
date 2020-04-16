<template>
  <b-navbar class="app-navbar" toggleable="sm" type="dark">
    <b-navbar-brand href="#" @click="toggleSubSidebar">playdate.gg</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">Calendar</b-nav-item>
        <b-nav-item href="#">Following</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>
            <em>User</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  data: () => ({}),
  methods: {
    ...mapActions(['toggleSubSidebar'])
  }
};
</script>

<style lang="scss" scoped>
@import '@/style/_variables';

.app-navbar {
  height: 100%;
  text-align: left;
  background-color: $gray-800;
  padding: 0 2rem;
  color: white;
  box-shadow: 0 0 1rem -0.5rem black, 0 0 0 1px rgba(black, 0.2);
  z-index: 1;

  & > * {
    height: 100%;
    .nav-item:not(:last-of-type) {
      margin-right: 1rem;
    }
  }

  &:after,
  &:before {
    content: '';
    display: block;
    clear: both;
  }

  .navbar-brand {
    padding: 0.5rem 1rem;
    color: $white;
    background-color: $purple;
    font-weight: 800;
    font-variant: small-caps;
  }
}
</style>
