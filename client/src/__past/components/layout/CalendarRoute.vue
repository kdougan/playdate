<template>
  <b-container
    class="calendar-view"
    :class="{ 'sidebar-collapse': subSidebarCollapse }"
    fluid
  >
    <loading :active.sync="isLoadingEvents" :is-full-page="true"></loading>
    <SubSidebarComp :collapse="subSidebarCollapse" />
    <b-container class="calendar-content" fluid>
      <CalendarComp />
    </b-container>
  </b-container>
</template>

<script>
import CalendarComp from '@/components/library/CalendarComp';
import SubSidebarComp from '@/components/library/SubSidebarComp';
import Loading from 'vue-loading-overlay';
import { mapGetters } from 'vuex';
export default {
  components: { CalendarComp, SubSidebarComp, Loading },
  data: () => ({}),
  computed: {
    ...mapGetters(['subSidebarCollapse', 'isLoadingEvents'])
  }
};
</script>

<style lang="scss">
@import '@/style/_variables';

.calendar-view {
  padding: 0 !important;
  margin: 0;
  display: grid;
  grid-template-columns: 16rem 1fr;
  height: 100%;
  position: relative;

  &.sidebar-collapse {
    grid-template-columns: 4rem 1fr;
  }

  .calendar-content {
    overflow-y: auto;
    padding: 2rem;
    z-index: 1;
  }

  .details {
    $width: 24rem;
    position: absolute;
    top: 0;
    right: -$width;
    height: 100%;
    width: $width;
    z-index: 2;
    overflow-y: auto;
    background-color: $gray-800;
    box-shadow: 0 0 2rem -1rem black;
    &.open {
      right: 0;
    }
  }
}
</style>
