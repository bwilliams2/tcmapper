<template>
  <div :style="containerStyle">
    <div :style="buttonContainer">
      <v-card outlined elevation="3">
        <v-select
          :items="mapTypes"
          :value="mapType"
          label="Map Overlay"
          @input="updateMapType"
          :style="{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
      </v-card>
    </div>
    <div :style="plotContainer">
      <v-card outlined elevation="3">
        <bar-plot
          :limitedData="limitedData"
          :limitedGrowthData="limitedGrowthData"
        ></bar-plot>
      </v-card>
    </div>
    <div :style="mapContainer">
      <overlay-map
        :selectedFeatures="selectedFeatures"
        :selectedLocations="selectedLocations"
      />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";
import { mapState } from "vuex";
import OverlayMap from "./OverlayMap.vue";
import BarPlot from "./BarPlotContainer.vue";
import {
  MapTypes,
  RootStateType,
  FeatureItem,
  HistDataItem,
  GrowthItem,
} from "@/store/state";

interface State {
  buttonContainer: any;
  mapContainer: any;
  parentStyle: any;
  cardStyle: any;
  mapTypes: { text: string; value: string }[];
  selectedFeatures: FeatureItem[];
  selectedLocations: [number, number, number][];
  limitedData: HistDataItem[];
  limitedGrowthData: GrowthItem[];
  containerStyle: any;
  plotContainer: any;
}

export default Vue.extend({
  name: "Home",
  components: {
    OverlayMap,
    BarPlot,
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
      mapTypes: [
        { text: "Heatmap", value: "points" },
        { text: "Parcels", value: "parcel" },
      ],
      buttonContainer: {
        position: "absolute",
        top: "10px",
        left: "60px",
        width: "250px",
        zIndex: 1000,
        // float: "right",
      },
      parentStyle: {
        width: "100%",
        height: "90%",
      },
      containerStyle: {
        position: "relative",
        width: "100%",
        height: "100%",
      },
      plotContainer: {
        position: "absolute",
        top: "20px",
        zIndex: 1000,
        // backgroundColor: "rgb(255,255,255, 0.8)",
        right: "20px",
        left: "200px",
        // width: window.innerWidth * 0.35,
        height: "200px",
        padding: "20px",
      },
      selectedFeatures: [],
      selectedLocations: [],
      limitedData: [],
      limitedGrowthData: [],
    };
  },
  computed: {
    ...mapState({
      mapType: function (state: RootStateType) {
        return state.plotControls.mapType;
      },
      latLng: (state: RootStateType) => state.plotControls.latLng,
      selectedUseClasses: (state: RootStateType) =>
        state.plotControls.selectedUseClasses,
      features: (state: RootStateType) => state.plotData.features,
      histData: (state: RootStateType) => state.plotData.histData,
      growthData: (state: RootStateType) => state.plotData.growthData,
      locationData: (state: RootStateType) => state.plotData.locationData,
      yearData: (state: RootStateType) => state.plotData.yearData,
      yearRange: (state: RootStateType) => [
        state.plotControls.startYear,
        state.plotControls.endYear,
      ],
    }),
  },
  mounted() {
    this.filterData(this.yearRange, this.selectedUseClasses);
    this.filterFeatures(this.yearRange, this.selectedUseClasses);
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
  },
  watch: {
    yearRange: function (newValue) {
      this.filterData(newValue, this.selectedUseClasses);
      this.filterFeatures(newValue, this.selectedUseClasses);
    },
    selectedUseClasses: function (newValue) {
      this.filterData(this.yearRange, newValue);
      this.filterFeatures(this.yearRange, newValue);
    },
  },
  methods: {
    filterData(years: number[], classes: string[]) {
      const limitedData = this.histData
        .filter(
          (el: HistDataItem) =>
            el.YEAR_BUILT <= years[1] && el.YEAR_BUILT >= years[0]
        )
        .map((el) => {
          return _.pick(el, ["YEAR_BUILT", ...classes]);
        });
      this.limitedData = limitedData as HistDataItem[];
      const limitedGrowthData = this.growthData
        .filter((el) => classes.includes(el.id))
        .map((el) => {
          return {
            id: el.id,
            points: el.points.filter(
              (point) =>
                point.YEAR_BUILT <= years[1] && point.YEAR_BUILT >= years[0]
            ),
          };
        });
      this.limitedGrowthData = limitedGrowthData;
    },
    filterFeatures(years: number[], classes: string[]) {
      this.selectedFeatures = this.features.filter(
        (el) =>
          classes.includes(el.properties.USECLASS1) &&
          el.properties.YEAR_BUILT <= years[1] &&
          el.properties.YEAR_BUILT >= years[0]
      );
      this.selectedLocations = this.locationData.filter(
        (el) => el[2] <= this.yearRange[1] && el[2] >= this.yearRange[0]
      );
    },
    updateMapType(newValue: MapTypes) {
      this.$store.dispatch("updateMapType", newValue);
    },
    handleResize() {
      this.containerStyle.height = window.innerHeight - 64 + "px";
      this.plotContainer.left = window.innerWidth * 0.55 + "px";
      this.plotContainer.height = window.innerHeight - 64 - 60 + "px";
    },
    resetAnalysis() {
      this.$store.dispatch("resetAnalysis");
    },
  },
});
</script>
