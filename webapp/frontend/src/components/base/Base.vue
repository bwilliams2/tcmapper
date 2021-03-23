<template>
  <div class="backContainer">
    <div
      class="largeBG"
      :style="{ backgroundImage: 'url(' + city + ')' }"
    ></div>
    <v-container fluid>
      <v-row align="center" justify="center">
        <v-col cols="10">
          <div class="text-h3 text-center font-weight-medium mb-16">
            Twin Cities Metro Statistics
          </div>
          <div class="text-h6 text-center font-weight-medium mt-16">
            Welcome to my site for presentation and analysis of geographic and
            election data in the Twin Cities metro and Greater Minnesota.
          </div>
          <div class="text-h6 text-center font-weight-medium mb-16">
            For more information on site development and additional analysis
            visit my main blog at
            <a href="https://bwilliams.dev">bwilliams.dev</a>.
          </div>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="6" md="4" lg="3" :style="{ height: '30vh' }">
          <v-card outlined elevation="3" :style="{ height: '100%' }">
            <div class="navButton">
              <div
                class="bg"
                :style="{
                  height: '100%',
                  width: '100%',
                  backgroundImage: 'url(' + paperMap + ')',
                  backgroundPosition: '50% 10%',
                }"
                id="parcelButton"
                v-on:click="parcelsNav"
              ></div>
              <!-- <span class="hoverAntiDisplay">Parcels</span> -->
              <!-- <v-container class="hoverDisplay" ma-0 pa-0> -->
              <v-container ma-0 pa-0>
                <v-row no-gutters>
                  <v-col
                    cols="12"
                    class="text-xs-center"
                    :style="parcelButtonStyle"
                  >
                    <v-btn
                      absolute
                      :style="{
                        left: '50%',
                        transform: 'translateX(-50%) translateY(100%)',
                      }"
                      :class="btnStyle"
                      to="parcels"
                      disabled
                      >Metro Parcel Map</v-btn
                    >
                  </v-col>
                  <v-col
                    cols="12"
                    class="text-xs-center"
                    :style="parcelButtonStyle"
                  >
                    <v-btn
                      absolute
                      :style="{
                        left: '50%',
                        transform: 'translateX(-50%) translateY(100%)',
                      }"
                      to="parcels"
                      >Parcel Density Stats</v-btn
                    >
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </v-card>
        </v-col>
        <v-col
          cols="12"
          sm="6"
          md="4"
          lg="3"
          :style="{ height: '30vh' }"
          offset-md="1"
        >
          <v-card outlined elevation="3" :style="{ height: '100%' }">
            <div class="navButton">
              <div
                class="bg"
                :style="{
                  height: '100%',
                  width: '100%',
                  backgroundImage: 'url(' + electionMap + ')',
                  backgroundSize: '100% 100%',
                }"
                v-on:click="electionNav"
                id="electionButton"
              ></div>
              <!-- <span class="hoverAntiDisplay">Elections</span> -->
              <!-- <v-container class="hoverDisplay" pa-0 ma-0> -->
              <v-container pa-0 ma-0>
                <v-row no-gutters>
                  <v-col
                    cols="12"
                    class="text-xs-center"
                    :style="electionButtonStyle"
                  >
                    <v-btn
                      absolute
                      :style="{
                        left: '50%',
                        transform: 'translateX(-50%) translateY(50%)',
                      }"
                      to="election/stateprecincts"
                      >State Map</v-btn
                    >
                  </v-col>
                  <v-col
                    cols="12"
                    class="text-xs-center"
                    :style="electionButtonStyle"
                  >
                    <v-btn
                      absolute
                      :style="{
                        left: '50%',
                        transform: 'translateX(-50%) translateY(50%)',
                      }"
                      disabled
                      to="election/metroprecincts"
                      >Metro Precinct Statistics</v-btn
                    >
                  </v-col>
                  <v-col
                    cols="12"
                    class="text-xs-center"
                    :style="electionButtonStyle"
                  >
                    <v-btn
                      absolute
                      :style="{
                        left: '50%',
                        transform: 'translateX(-50%) translateY(50%)',
                      }"
                      to="election/metromodel"
                      >Metro Precinct Model</v-btn
                    >
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
  btnStyle: {
    left: string;
    transform: string;
  };
  electionButtonStyle: {
    height: string | number;
  };
  parcelButtonStyle: {
    height: string | number;
  };
}

export default Vue.extend({
  name: "Home",
  data(): State {
    return {
      btnStyle: {
        left: "50%",
        transform: "translateX(-50%) translateY(50%)",
      },
      electionButtonStyle: {
        height: 0,
      },
      parcelButtonStyle: {
        height: 0,
      },
    };
  },
  mounted() {
    this.handleResize();
    window.addEventListener("resize", this.onResize);
  },
  destroyed() {
    window.removeEventListener("resize", this.onResize);
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
    onResize() {
      const handleResize = this.handleResize;
      return _.debounce(function () {
        handleResize;
      }, 100);
    },
    handleResize() {
      const buttonHeight = document.getElementById("parcelButton")
        ?.offsetHeight;
      if (buttonHeight) {
        this.electionButtonStyle.height = buttonHeight / 3 + "px";
        this.parcelButtonStyle.height = buttonHeight / 2 + "px";
      }
    },
    electionNav() {
      this.$router.push({ path: "/elections" });
    },
    parcelsNav() {
      this.$router.push({ path: "/parcels" });
    },
  },
});
</script>
