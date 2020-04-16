<template>
  <div class="event-modal view-event-modal">
    <loading :active.sync="isLoadingEvent"></loading>
    <div class="dismiss-modal" @click="$emit('close')">close</div>
    <!-- Post-->
    <div class="post-module">
      <!-- splash-->
      <div class="splash">
        <div class="host">
          <img :src="`assets/${ownerAvatar}`" />
        </div>
        <div class="date">
          <div class="day">{{ start | moment('DD') }}</div>
          <div class="month">{{ start | moment('MMM') }}</div>
        </div>
        <div v-if="gameTitle" class="game-title">playing {{ gameTitle }}</div>
        <img v-if="splash" class="event-splash" :src="`assets/${splash}`" />
      </div>
      <!-- Category -->
      <div class="category">
        {{ start | moment('dddd, MMMM Do') }} @
        {{ start | moment('hh:mm a') }} - duration:
        {{ durationString }}
      </div>
      <!-- Post Content-->
      <div class="post-content">
        <h1 class="title">{{ title }}</h1>
        <h2 class="sub_title">{{ countdown }}</h2>
        <div class="description">
          <div v-html="markedDescription"></div>
        </div>
      </div>
      <!-- Meta -->
      <div class="post-meta">
        <span class="participant-count">
          <i class="fa fa-users"></i>
          {{ participants.length }}/{{ totalSlots }} participants
        </span>
        <span class="follower-count">
          <i class="fa fa-bell"></i>
          <a href="#">{{ followers }} following</a>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import marked from 'marked';
import Loading from 'vue-loading-overlay';
import { mapGetters } from 'vuex';

export default {
  components: { Loading },
  data: () => ({
    group_count: 0,
    countdown: '-',
    gameTitle: 'Call of Duty: Modern Warfare (2019)',
    participants: [1, 2, 3, 4, 5, 6],
    followers: 39,
    totalSlots: 10
  }),
  props: {
    text: String,
    event: Object
  },
  computed: {
    ...mapGetters(['isLoadingEvent']),
    id() {
      return this.event.id;
    },
    owner_id() {
      return this.event.owner_id;
    },
    title() {
      return this.event.title;
    },
    start() {
      return this.event.start_time;
    },
    end() {
      return this.event.end_time;
    },
    duration() {
      return this.event.duration;
    },
    description() {
      return this.event.description;
    },
    ownerAvatar() {
      return this.event.owner.asset.medium;
    },
    splash() {
      if (this.event) {
        return this.event.asset;
      }
      return null;
    },
    durationString() {
      if (this.duration === 0 || isNaN(this.duration)) return '0 minutes';
      const hours = Math.floor(this.duration / 60);
      const minutes = this.duration % 60;
      const parts = [];
      if (hours) {
        if (hours == 1) parts.push(`1 hr`);
        else parts.push(`${hours} hrs`);
      }
      if (minutes) {
        if (minutes == 1) parts.push(`1 min`);
        else parts.push(`${minutes} mins`);
      }
      return parts.join(' ');
    },
    markedDescription() {
      return marked(this.description);
    }
  },
  mounted() {
    this.countdown = Vue.moment(this.start).fromNow();
    setInterval(() => {
      this.countdown = Vue.moment(this.start).fromNow();
    }, 1000);
  }
};
</script>

<style lang="scss" scoped>
@import '@/style/_variables';

.event-modal {
  margin: 0;
  height: 100%;
  position: relative;

  .dismiss-modal {
    position: absolute;
    top: 0;
    left: 0;
    padding: 0 1rem;
    z-index: 2;
    font-size: 16pt;
    color: white;
    font-variant: small-caps;
    opacity: 60%;
    cursor: pointer;
    transition: all 250ms;

    &:hover {
      opacity: 100%;
      background-color: rgba(black, 0.25);
    }
  }
}
.post-module {
  position: relative;
  display: grid;
  grid-template-rows: 15rem 3rem 1fr 2rem;
  grid-template-areas: 'splash' 'category' 'post-content' 'post-meta';
  height: 100%;
  min-height: 36rem;
  transition: all 0.3s linear 0s;
  background-color: $white;
  z-index: 0;

  .category {
    grid-area: category;
    height: 100%;
    background: $purple;
    padding: 0.75rem 1rem;
    color: #ffffff;
    font-size: 12pt;
    font-weight: 600;
    text-transform: uppercase;
    z-index: 2;
  }

  .splash img,
  .hover .splash img {
    transform: scale(1.1);
  }

  .splash {
    grid-area: splash;
    position: relative;
    background: #000000;
    overflow: hidden;
    z-index: 1;

    & > img {
      opacity: 0.5;
    }

    .host {
      position: absolute;
      top: 3rem;
      left: 1rem;
      z-index: 2;
      // background: $purple;
      width: 7rem;
      height: 7rem;
      color: #ffffff;
      font-weight: 700;
      text-align: center;
      overflow: hidden;
      border-radius: 50%;
      box-shadow: 0 0 0 0.25rem $purple;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .date {
      position: absolute;
      top: 0;
      right: 1rem;
      z-index: 1;
      background: $purple;
      width: 4rem;
      height: 7rem;
      padding: 3rem 0;
      color: #ffffff;
      font-weight: 700;
      text-align: center;

      .day {
        font-size: 18pt;
      }

      .month {
        font-size: 12pt;
        text-transform: uppercase;
      }
    }

    .game-title {
      position: absolute;
      bottom: -3rem;
      height: 3rem;
      width: 100%;
      background: rgba($black, 0.5);
      padding: 0.75rem 1rem;
      color: #ffffff;
      font-size: 12pt;
      font-weight: 600;
      text-transform: uppercase;
      z-index: 2;
      transition: all 0.2s linear 0s;
    }
    &:hover .game-title {
      bottom: 0;
    }

    .event-splash {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top;
    }
  }

  .post-content {
    grid-area: post-content;
    height: 100%;
    background: #ffffff;
    width: 100%;
    padding: 2rem;

    overflow-y: auto;
    transition: all 0.3s cubic-bezier(0.37, 0.75, 0.61, 1.05) 0s;
    z-index: 1;

    .title {
      margin: 0;
      padding: 0 0 10px;
      color: #333333;
      font-size: 26px;
      font-weight: 700;
    }

    .sub_title {
      margin: 0;
      padding: 0 0 20px;
      color: $purple;
      font-size: 20px;
      font-weight: 400;
    }

    .description {
      color: #666666;
      font-size: 14pt;
      line-height: 1.8em;
    }
  }
  .post-meta {
    grid-area: post-meta;
    margin: 0.5rem 1rem 0.5rem;
    color: #999999;
    height: 3rem;

    & > * {
      margin-right: 1rem;
    }

    a {
      color: #999999;
      text-decoration: none;
    }
  }
}
</style>
