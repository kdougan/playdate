<template>
  <b-container
    class="sidebar-item"
    v-tooltip.right="{
      content: person.handle,
      trigger: 'hover',
      offset: 8
    }"
  >
    <div class="icon" :style="iconStyle">
      <img v-if="thumbnail" :src="`/assets/${thumbnail}`" />
    </div>
  </b-container>
</template>

<script>
export default {
  props: ['subscription'],
  computed: {
    person() {
      return this.subscription.person;
    },
    thumbnail() {
      return this.person.asset ? this.person.asset.thumb_64x64_path : null;
    },
    iconStyle() {
      return {
        boxShadow: `0 0 3px black, 0 0 0 5px ${this.subscription.meta.color}, 0 0 3px 5px black`
      };
    }
  }
};
</script>

<style lang="scss" scoped>
.sidebar-item {
  display: block;
  height: 3rem;
  width: 3rem;
  padding: 0.25rem;
  margin-bottom: 1rem;
  align-items: center;

  .icon {
    width: 2.5rem;
    height: 2.5rem;
    background-color: black;
    display: inline-block;
    border-radius: 50%;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
}
</style>
