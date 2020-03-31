<template>
  <div class="agenda">
    <Auth v-if="!isAuthenticated" />
    <Calendar v-else />
  </div>
</template>

<script>
import Calendar from './library/Calendar';
import Auth from './Auth';
import authService from '../service/auth';
import { mapGetters } from 'vuex';

export default {
  components: { Auth, Calendar },
  data: () => {
    return {};
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  created() {
    authService.checkAuth();
  }
};
</script>

<style lang="scss" scoped>
.agenda {
  padding: 1rem;
}
</style>
