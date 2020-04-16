<template>
  <b-container
    class="sub-sidebar-item"
    v-tooltip.right-start="{
      content: itemData.handle,
      trigger: 'hover',
      classes: displayNone
    }"
  >
    <div class="icon" :style="iconStyle">
      <img v-if="itemData.asset" :src="`assets/${itemData.asset.small}`" />
    </div>
    <span v-if="!collapse" class="handle">{{ itemData.handle }}</span>
  </b-container>
</template>

<script>
export default {
  props: {
    itemData: Object,
    collapse: Boolean
  },
  data: () => ({}),
  computed: {
    iconStyle() {
      return {
        boxShadow: `0 0 3px black, 0 0 0 5px ${this.itemData.color}, 0 0 3px 5px black`
      };
    },
    displayNone() {
      return !this.collapse ? 'displayNone' : null;
    }
  },
  methods: {
    toggleItem: itemId => this.$emit('toggleItem', itemId)
  }
};
</script>

<style lang="scss" scoped>
@import '@/style/_variables';

.sub-sidebar-item {
  display: flex;
  flex-wrap: nowrap;
  height: 3rem;
  padding: 1rem 0.75rem;
  align-items: center;

  .icon {
    width: 2.5rem;
    height: 2.5rem;
    background-color: $gray-400;
    display: inline-block;
    border-radius: 50%;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
  .handle {
    padding-left: 1rem;
  }
}
</style>
