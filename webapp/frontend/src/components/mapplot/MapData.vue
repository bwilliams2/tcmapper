<template>
  <div :style="containerStyle">
    <div :style="buttonContainer">
      <v-container fluid>
        <v-row justify="end">
          <v-col cols="3">
            <v-select
              :items="mapTypes"
              :value="mapType"
              label="Overlay"
              @input="updateMapType"
              solo
            ></v-select>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <div :style="mapContainer">
      <overlay-map
        :selectedFeatures="selectedFeatures"
        :selectedLocations="selectedLocations"
      />
    </div>
    <div :style="plotContainer">
      <v-container fluid>
        <v-row>
          <v-col md="12" lg="6" v-if="histData.length > 0">
            <bar-plot
              :limitedData="limitedData"
              :limitedGrowthData="limitedGrowthData"
            ></bar-plot>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
  <!-- <v-card outlined elevation="7" :style="cardStyle">
    <v-container fluid>
      <v-row>
        <v-col sm="12" md="6">
          <div :style="containerStyle">
            <div :style="buttonContainer">
              <v-container fluid>
                <v-row justify="end">
                  <v-col cols="3">
                    <v-select
                      :items="mapTypes"
                      :value="mapType"
                      label="Overlay"
                      @input="updateMapType"
                      solo
                    ></v-select>
                  </v-col>
                </v-row>
              </v-container>
            </div>
            <div :style="{ height: '80vh' }">
              <overlay-map
                :selectedFeatures="selectedFeatures"
                :selectedLocations="selectedLocations"
              />
            </div>
          </div>
        </v-col>
        <v-col md="12" lg="6" v-if="histData.length > 0">
          <bar-plot
            :limitedData="limitedData"
            :limitedGrowthData="limitedGrowthData"
          ></bar-plot>
        </v-col>
      </v-row>
    </v-container>
  </v-card> -->
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
        top: "15px",
        left: "15px",
        width: "100%",
        zIndex: 1000,
        float: "right",
      },
      parentStyle: {
        width: "100%",
        height: "90%",
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
    containerStyle() {
      return {
        position: "relative",
        width: "100%",
        height: window.innerHeight - 64 + "px",
      };
    },
    plotContainer() {
      return {
        position: "absolute",
        top: "20px",
        left: window.innerWidth * 0.55 + "px",
        width: window.innerWidth * 0.45,
        height: window.innerHeight - 64 + "px",
        padding: "20px",
      };
    },
  },
  mounted() {
    this.filterData(this.yearRange, this.selectedUseClasses);
    this.filterFeatures(this.yearRange, this.selectedUseClasses);
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
      const limitedGrowthData = this.growthData.map((el) => {
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
  },
});
</script>