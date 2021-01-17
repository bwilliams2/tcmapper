<template>
  <!-- <v-card outlined elevation="7" :style="cardStyle"> -->
  <div :style="containerStyle">
    <div :style="buttonContainer">
      <v-container fluid>
        <v-row justify="end">
          <v-col cols="3">
            <v-btn
              class="mr-5"
              @click.native="submitLatLng"
              :disabled="!latLng[0]"
              :style="{ float: 'right' }"
              >Calculate Stats</v-btn
            >
          </v-col>
        </v-row>
      </v-container>
    </div>
    <div :style="mapContainer">
      <search-map />
    </div>
  </div>
  <!-- </v-card> -->
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";
import { mapState } from "vuex";
import SearchMap from "./SearchMap.vue";
import BarPlot from "./barplot/BarPlotContainer.vue";
import {
  MapTypes,
  RootStateType,
  FeatureItem,
  HistDataItem,
} from "@/store/state";

interface State {
  buttonContainer: any;
  parentStyle: any;
  cardStyle: any;
  containerStyle: any;
  mapContainer: any;
}

export default Vue.extend({
  name: "Home",
  components: {
    SearchMap,
  },
  data(): State {
    return {
      cardStyle: {
        // padding: "10px",
        margin: "15px",
      },
      mapContainer: {
        position: "absolute",
        height: "100%",
        width: "100%",
      },
      buttonContainer: {
        position: "absolute",
        top: "10px",
        width: "100%",
        zIndex: 1000,
        float: "right",
      },
      containerStyle: {
        position: "relative",
        width: "100%",
        height: "90%",
      },
      parentStyle: {
        width: "100%",
        height: "90%",
      },
    };
  },
  computed: {
    ...mapState({
      mapType: function (state: RootStateType) {
        return state.plotControls.mapType;
      },
      latLng: (state: RootStateType) => state.plotControls.latLng,
    }),
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
    this.$store.dispatch("resetAnalysis");
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    handleResize() {
      this.containerStyle.height = window.innerHeight - 64 + "px";
    },
    submitLatLng() {
      this.$store
        .dispatch("updatePlotData")
        .then(() => this.$router.push({ path: "map" }));
    },
  },
});
</script>
