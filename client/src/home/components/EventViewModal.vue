<template>
  <div class="event-view-modal" v-if="event.loading || event.item">
    <div class="content-wrapper">
      <div class="content">
        <template v-if="event.item">
          <!-- splash -->
          <div class="splash">
            <div class="host">
              <img :src="avatarAssetPath" />
            </div>
            <div class="date">
              <div class="day">{{ startMoment | moment('DD') }}</div>
              <div class="month">{{ startMoment | moment('MMM') }}</div>
            </div>
            <div v-if="event.item.meta.activity" class="activity">
              {{ event.item.meta.activity }}
            </div>
            <img
              v-if="splashAssetPath"
              class="event-splash"
              :src="splashAssetPath"
            />
          </div>
          <!-- date-string -->
          <div class="date-string">
            {{ startMoment | moment('dddd, MMM Do') }} @
            {{ startMoment | moment('hh:mm a') }} - duration:
            {{ durationString }}
          </div>
          <!-- information-->
          <div class="information">
            <h1 class="title">{{ event.item.title }}</h1>
            <h2 class="sub_title">{{ countdown.text }}</h2>
            <div class="description">
              <div v-html="markedDescription"></div>
            </div>
          </div>
          <!-- Meta -->
          <div class="meta">
            <span class="participant-count">
              <i class="fa fa-users"></i>
              {{ filledSlotCount }}/{{ totalSlotCount }} participants
            </span>
            <span class="follower-count">
              <i class="fa fa-bell"></i>
              {{ event.item.subscribers.length }} following
            </span>
          </div>
        </template>
        <loading
          :active.sync="event.loading"
          :color="'green'"
          :is-full-page="false"
        ></loading>
      </div>
    </div>
    <div
      class="overlay"
      :class="{ show: event.loading || event.item }"
      @click="clearEvent"
    />
  </div>
</template>

<script>
import Vue from 'vue';
import marked from 'marked';
import Loading from 'vue-loading-overlay';

import { mapGetters, mapActions } from 'vuex';

export default {
  components: { Loading },
  data() {
    return {
      countdown: { text: '-' },
    };
  },
  computed: {
    ...mapGetters({
      event: 'events/event',
    }),
    startMoment() {
      return Vue.moment(this.event.item.startTime);
    },
    avatarAssetPath() {
      return `assets/${this.event.item.owner.asset.thumb_256x256_path}`;
    },
    splashAssetPath() {
      return `assets/${this.event.item.asset.thumb_540x360_path}`;
    },
    durationString() {
      if (this.event.item.duration === 0 || isNaN(this.event.item.duration))
        return '0 minutes';
      const hours = Math.floor(this.event.item.duration / 60);
      const minutes = this.event.item.duration % 60;
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
      return marked(this.event.item.description);
    },
    totalSlotCount() {
      if (!this.event.item.groups) return 0;
      return this.event.item.groups
        .map((group) => group.slotCount)
        .reduce((a, b) => a + b);
    },
    filledSlotCount() {
      if (!this.event.item.groups) return 0;
      return this.event.item.groups
        .map((group) => group.members.length)
        .reduce((a, b) => a + b);
    },
  },
  watch: {
    event() {
      if (this.event.item) {
        this.countdown = {
          text: this.startMoment.fromNow(),
          timer: setInterval(() => {
            this.countdown.text = this.startMoment.fromNow();
          }, 1000),
        };
      } else if (this.countdown.timer) {
        clearInterval(this.countdown.timer);
        this.countdown = { text: '-' };
      }
    },
  },
  methods: {
    ...mapActions({
      clearEvent: 'events/clearEvent',
    }),
  },
};
</script>

<style lang="scss" scoped>
@import '@/style/_variables';

.event-view-modal {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 99;

  .overlay {
    position: absolute;
    opacity: 0;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: rgba(black, 0.5);
    z-index: 1;
    transition: all 250ms;

    &.show {
      opacity: 1;
    }
  }

  .content-wrapper {
    position: absolute;
    right: 0;
    width: 32rem;
    height: 100%;
    background-color: white;
    z-index: 2;
    box-shadow: 0 0 2rem -1rem black, 0 0 0 1px rgba(black, 0.2);
    overflow: hidden;
    padding: 0;
    height: 100%;

    .content {
      position: relative;
      display: grid;
      width: 100%;
      height: 100%;
      margin: 0;
      grid-template-rows: 15rem 3rem 1fr 2rem;
      grid-template-areas: 'splash' 'date-string' 'information' 'meta';

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
          top: 1.5rem;
          left: 1.5rem;
          z-index: 2;
          background: $green;
          width: 7rem;
          height: 7rem;
          color: #ffffff;
          font-weight: 700;
          text-align: center;
          overflow: hidden;
          border-radius: 50%;
          box-shadow: 0 0 0 0.25rem $green;

          img {
            width: 100%;
            height: 100%;
            object-fit: cover;
          }
        }

        .date {
          position: absolute;
          top: 0;
          right: 1.5rem;
          z-index: 1;
          background: $green;
          width: 4rem;
          height: 7rem;
          padding: 3rem 0;
          color: #ffffff;
          font-weight: 700;
          text-align: center;

          &:after {
            position: absolute;
            bottom: -0.5rem;
            left: 0;
            width: 0;
            height: 0;
            content: '';
            border-top: 0.5rem solid $green;
            border-left: 4rem solid transparent;
          }

          .day {
            font-size: 18pt;
          }

          .month {
            font-size: 12pt;
            text-transform: uppercase;
          }
        }

        .activity {
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
        &:hover .activity {
          bottom: 0;
        }

        .event-splash {
          width: 100%;
          height: 100%;
          object-fit: cover;
          object-position: top;
        }
      }

      .date-string {
        grid-area: date-string;
        height: 100%;
        background: $green;
        padding: 0.75rem 1rem;
        color: #ffffff;
        font-size: 12pt;
        font-weight: 600;
        text-transform: uppercase;
        z-index: 2;
      }

      .information {
        grid-area: information;
        height: 100%;
        background: #ffffff;
        width: 100%;
        padding: 2rem 2rem 0;

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

      .meta {
        grid-area: meta;
        display: flex;
        justify-content: space-around;
        margin: 0.5rem 1rem 0.5rem;
        color: #999999;
        height: 3rem;

        & > * {
          margin-right: 1rem;
        }

        a {
          color: #999999;
          text-decoration: none;
          margin-left: 0.5rem;
        }
      }
    }
  }

  .slide-enter-active,
  .slide-leave-active {
    transition: all 0.25s ease-out;
  }

  .slide-enter,
  .slide-leave-active {
    opacity: 0;
    transform: translateX(580px);
    width: 0;
  }
}
</style>
