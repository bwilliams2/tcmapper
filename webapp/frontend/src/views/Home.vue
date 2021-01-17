<template>
  <div class="home">
    <v-app>
      <v-app-bar app color="primary" dark>
        <v-container :style="{ zIndex: 10001 }">
          <v-row no-gutters>
            <v-col cols="2">
              <div
                :style="{
                  fontSize: 'x-large',
                  fontWeight: 'bold',
                }"
              >
                TC Mapper
              </div>
            </v-col>
          </v-row>
        </v-container>
        <template v-if="routeIsMap">
          <router-link to="/" tag="v-btn" @click.native="resetAnalysis">
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

        <v-btn href="https://github.com/vuetifyjs/vuetify/releases/latest" text>
          <span class="mr-2">About</span>
          <v-icon>mdi-open-in-new</v-icon>
        </v-btn>
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
import { RootStateType } from "@/store/state";
import Vue from "vue";
import { mapState } from "vuex";
import _ from "lodash";

export default Vue.extend({
  name: "Home",

  // components: {
  // },

  data: () => ({
    ranges: [
      { text: "1 km", value: 1000 },
      { text: "5 km", value: 5000 },
      { text: "10 km", value: 10000 },
    ],
    selectStyle: {
      paddingTop: "25px",
      marginRight: "10px",
    },
  }),
  computed: {
    ...mapState({
      years: function (state: RootStateType) {
        const years = state.plotData.histData.map((el) => el.YEAR_BUILT);
        const sortYears = _.range(
          Math.min(...years),
          Math.max(...years) + 1
        ).reverse();
        return sortYears;
      },
      endYears: function (state: RootStateType) {
        const years = state.plotData.histData.map((el) => el.YEAR_BUILT);
        return _.range(Math.min(...years), Math.max(...years) + 1)
          .map((el) => ({
            value: el,
            text: el,
            disabled: el < state.plotControls.startYear,
          }))
          .reverse();
      },
      addressInfo: (state: RootStateType) => state.addressInfo,
      analysisRange: (state: RootStateType) => state.plotControls.analysisRange,
      startYear: (state: RootStateType) => state.plotControls.startYear,
      endYear: (state: RootStateType) => state.plotControls.endYear,
    }),
    routeIsMap() {
      return this.$route.name && this.$route?.name.includes("map");
    },
    overlay() {
      return this.$store.state.ui.showLoadingOverlay;
    },
  },
  methods: {
    resetAnalysis() {
      this.$store.dispatch("resetAnalysis");
    },
    updateRange(newValue: number) {
      this.$store.dispatch("updateAnalysisRange", newValue);
    },
    updateStartYear(newValue: number) {
      this.$store.dispatch("updateStartYear", newValue);
    },
    updateEndYear(newValue: number) {
      this.$store.dispatch("updateEndYear", newValue);
    },
  },
});
</script>
