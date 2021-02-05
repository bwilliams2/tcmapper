<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col cols="6">
        <div class="fill" :style="{ height: '50vh' }">
          <img
            :src="mill"
            :style="{ objectPosition: '100% 0', width: '100%', height: '100%' }"
          />
        </div>
      </v-col>
      <v-col cols="6">
        <v-row no-gutters>
          <v-col cols="6">
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
                <span>Election</span>
              </div>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card outlined elevation="3">
              <div class="navButton">
                <div
                  class="bg"
                  :style="{
                    height: '30vh',
                    width: '100%',
                    backgroundImage: 'url(' + paperMap + ')',
                    backgroundPosition: '50% 0',
                  }"
                  v-on:click="parcelsNav"
                ></div>
                <span>Parcels</span>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
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
