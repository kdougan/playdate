<template>
  <div class="sidebar">
    <div class="header">playrcal</div>
    <!-- <sidebar-item :subscription="person" /> -->
    <div class="sidebar-item-container" v-if="subscriptions.items">
      <div v-for="(value, key) in subscriptions.items" :key="key">
        <sidebar-item
          v-for="sub in value"
          :key="sub.calendarId"
          :subscription="sub"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import SidebarItem from './SidebarItem';

export default {
  components: { SidebarItem },
  computed: {
    ...mapGetters({
      person: 'authentication/person',
      subscriptions: 'subscriptions/subscriptions',
    }),
    // subForamttedPerson() {
    //   return {
    //     ...this.person,
    //   };
    // },
  },
  methods: {
    ...mapActions({
      getSubscriptions: 'subscriptions/getSubscriptions',
    }),
  },
  created() {
    this.getSubscriptions(this.person.id);
  },
};
</script>

<style lang="scss" scoped>
@import '@/style/_variables';

.sidebar {
  padding: 0;
  overflow: hidden;

  .header {
    width: 5rem;
    height: 1.5rem;
    text-align: center;
    font-variant: small-caps;
    font-size: 14pt;
    font-weight: 800;
    color: $gray-800;
    background-color: $green;
    position: relative;
    z-index: 2;

    &:after {
      position: absolute;
      bottom: -0.5rem;
      left: 0;
      width: 0;
      height: 0;
      content: '';
      border-top: 0.5rem solid $green;
      border-right: 5rem solid transparent;
    }
  }
  .sidebar-item-container {
    overflow-y: auto;
    display: block;
    height: 100%;
    padding: 1rem 0.5rem;
  }
}
</style>
