<template>
  <div class="backContainer">
    <div
      class="largeBG"
      :style="{ backgroundImage: 'url(' + city + ')' }"
    ></div>
    <v-container fluid>
      <v-row>
        <v-col cols="3">
          <v-card outlined elevation="3">
            <div class="navButton">
              <div
                class="bg"
                :style="{
                  height: '30vh',
                  width: '100%',
                  backgroundImage: 'url(' + electionMap + ')',
                  backgroundSize: '100% 100%',
                }"
                v-on:click="electionNav"
              ></div>
              <span class="hoverAntiDisplay">Elections</span>
              <v-container class="hoverDisplay">
                <v-row>
                  <v-col cols="12">
                    <span>State Map</span>
                  </v-col>
                  <v-col cols="12">
                    <span>Metro Precinct Statistics</span>
                  </v-col>
                  <v-col cols="12">
                    <span>Metro Precinct Model</span>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </v-card>
        </v-col>
        <v-col cols="3">
          <v-card outlined elevation="3">
            <div class="navButton">
              <div
                class="bg"
                :style="{
                  height: '30vh',
                  width: '100%',
                  backgroundImage: 'url(' + paperMap + ')',
                  backgroundPosition: '50% 10%',
                }"
                v-on:click="parcelsNav"
              ></div>
              <span class="hoverAntiDisplay">Parcels</span>
              <v-container class="hoverDisplay">
                <v-row>
                  <v-col cols="12">
                    <span>Parcel Map</span>
                  </v-col>
                  <v-col cols="12">
                    <span>Density Stats</span>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import "./Base.css";
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
    // ...mapState({
    //   years: function (state: RootStateType) {
    //     const years = state.plotData.histData.map((el) => el.YEAR_BUILT);
    //     const sortYears = _.range(
    //       Math.min(...years),
    //       Math.max(...years) + 1
    //     ).reverse();
    //     return sortYears;
    //   }
    // }),
    bridge() {
      return require("./gallery/nicole-geri-9mYqvUo5XxM-unsplash.jpg");
    },
    city() {
      return require("./gallery/weston-mackinnon-ZmZP3oVReZY-unsplash.jpg");
    },
    snow() {
      return require("./gallery/weston-mackinnon-xafjfcTz1d4-unsplash.jpg");
    },
    mill() {
      return require("./gallery/weston-mackinnon-6IkhvzeHJn4-unsplash.jpg");
    },
    paperMap() {
      return require("./gallery/nico-smit-Q1tAFjL34C4-unsplash.jpg");
    },
    electionMap() {
      return require("./gallery/clay-banks-BY-R0UNRE7w-unsplash.jpg");
    },
  },
  methods: {
    electionNav() {
      this.$router.push({ path: "/elections" });
    },
    parcelsNav() {
      this.$router.push({ path: "/parcels" });
    },
  },
});
</script>
