<template>
  <div id="app">
    <Agenda />
  </div>
</template>

<script>
import Agenda from './components/Agenda';
export default {
  name: 'App',
  components: {
    Agenda,
  },
};
</script>

<style lang="scss">
@import url('https://use.fontawesome.com/releases/v5.0.6/css/all.css');
@import './style/bootstrap.min';

@import './style/_variables';

*,
*:before,
*:after {
  box-sizing: border-box;
}
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $body-color;
  background-color: $body-bg;
  width: 100%;
  height: 100%;
}
</style>
