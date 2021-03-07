<template>
  <div class="home">
    <v-app>
      <v-app-bar app color="#454545" dark>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

        <v-container :style="{ zIndex: 10001 }">
          <v-row no-gutters>
            <v-col cols="4">
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
      </v-app-bar>
      <v-navigation-drawer
        v-model="drawer"
        absolute
        bottom
        temporary
        :style="{ zIndex: 10000 }"
      >
        <v-list nav dense>
          <v-list-item-group active-class="deep-purple--text text--accent-4">
            <v-list-item>
              <v-btn min-width="100%" to="/">Home</v-btn>
            </v-list-item>
            <v-list-item>
              <v-btn min-width="100%" to="/parcels">Parcels</v-btn>
            </v-list-item>
            <v-list-item>
              <v-btn min-width="100%" to="/election">Election</v-btn>
            </v-list-item>
            <v-list-item>
              <v-btn min-width="100%" to="/about">About</v-btn>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
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

interface State {
  drawer: boolean;
  selectStyle: any;
}

export default Vue.extend({
  name: "Home",
  data(): State {
    return {
      drawer: false,
      selectStyle: {
        paddingTop: "25px",
        marginRight: "10px",
      },
    };
  },
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
