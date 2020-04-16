<template>
  <b-container class="sub-sidebar" fluid>
    <b-container
      class="sub-sidebar-section"
      v-for="section in orderedSections"
      :key="section.title"
    >
      <b-container v-if="collapse" class="sub-sidebar-icon" fluid>
        <i :class="`far fa-${section.icon}`" />
      </b-container>
      <b-container v-else class="sub-sidebar-title" fluid>{{section.title}}</b-container>
      <SubSidebarItem
        v-for="item in section.items"
        :key="item.id"
        class="sub-sidebar-item"
        :itemData="item"
        :collapse="collapse"
      />
    </b-container>
  </b-container>
</template>

<script>
import SubSidebarItem from '@/components/library/SubSidebarItem';

import { mapGetters } from 'vuex';

export default {
  components: { SubSidebarItem },
  props: { collapse: Boolean },
  data: () => ({}),
  computed: {
    ...mapGetters(['config']),
    subs() {
      return this.config && 'subs' in this.config
        ? Object.values(this.config.subs)
        : [];
    },
    sections() {
      return [
        {
          title: 'subscriptions',
          icon: 'star',
          items: this.subs,
          order: 1
        },
        {
          title: 'suggestions',
          icon: 'chart-bar',
          items: [],
          order: 2
        }
      ];
    },
    orderedSections() {
      if (this.sections.length == 0) return [];
      const sections = this.sections.filter((a) => a.items.length > 0);
      sections.sort((a, b) => a.order - b.order);
      return sections;
    }
  }
};
</script>

<style lang="scss" scoped>
@import '@/style/_variables';

.sub-sidebar {
  overflow: hidden;
  overflow-y: auto;
  width: 100%;
  background-color: $gray-800;
  padding: 0;

  .sub-sidebar-section {
    padding: 1rem 0;

    &:not(:last-of-type) {
      border-bottom: 1px solid $gray-600;
    }

    .sub-sidebar-icon,
    .sub-sidebar-title {
      font-size: 18pt;
      padding: 0 1rem;
    }
    .sub-sidebar-icon {
      text-align: center;
    }
    .sub-sidebar-title {
      font-variant: small-caps;
    }
  }
}
</style>
