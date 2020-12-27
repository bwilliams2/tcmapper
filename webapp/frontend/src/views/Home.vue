<template>
  <div class="home">
    <v-app>
      <v-app-bar app color="primary" dark>
        <template v-if="routeIsMap">
          <router-link to="/" tag="v-btn" @click.native="resetAddress">
            <v-btn>
              <v-icon>mdi-arrow-left-bold</v-icon>
              <span class="mr-2">Reset Map</span>
            </v-btn>
          </router-link>
        </template>
        <div class="d-flex align-center">
          <!-- <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
            transition="scale-transition"
            width="40"
          />

          <v-img
            alt="Vuetify Name"
            class="shrink mt-1 hidden-sm-and-down"
            contain
            min-width="100"
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
            width="100"
          /> -->
        </div>

        <v-spacer></v-spacer>

        <!-- <v-btn
          href="https://github.com/vuetifyjs/vuetify/releases/latest"
          target="_blank"
          text
        >
          <span class="mr-2">Latest Release</span>
          <v-icon>mdi-open-in-new</v-icon>
        </v-btn> -->
      </v-app-bar>
      <v-main>
        <router-view></router-view>
        <!-- <template v-if="!addressInfo.title">
        <Landing />
      </template>
      <template v-if="addressInfo.title">
        <Map />
      </template> -->
      </v-main>
    </v-app>
    <v-overlay :value="overlay" :style="{ zIndex: 1000 }">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
      <div :class="['text-h6']" v-bind:style="{ textAlign: 'center' }">
        Calculating Stats
      </div>
    </v-overlay>
  </div>
</template>

<script lang="ts">
declare global {
  interface Window {
    H: any;
    hereCallback: any;
    L: any;
  }
}
import Vue from "vue";
import { mapState } from "vuex";

export default Vue.extend({
  name: "Home",

  // components: {
  // },

  data: () => ({
    //
  }),
  computed: {
    ...mapState(["addressInfo"]),
    routeIsMap() {
      return this.$route.name && this.$route?.name.includes("map");
    },
    overlay() {
      return this.$store.state.ui.showLoadingOverlay;
    },
  },
  methods: {
    resetAddress() {
      this.$store.dispatch("resetAnalysis");
    },
  },
});
</script>
