<template>
  <v-container fluid>
    <v-row justify="end">
      <v-col cols="4">
        <v-select
          @input="updateRange"
          :value="analysisRange"
          :items="ranges"
          label="Analysis Distance"
        ></v-select>
      </v-col>
      <v-col cols="4">
        <v-autocomplete
          v-on:input="updateStartYear"
          :value="startYear"
          :items="years"
          label="Start Year"
        ></v-autocomplete>
      </v-col>
      <v-col cols="4">
        <v-autocomplete
          v-on:input="updateStartYear"
          :value="endYear"
          :items="endYears"
          label="End Year"
        ></v-autocomplete>
      </v-col>
    </v-row>
    <v-row class="fill-height">
      <v-col cols="12">
        <div id="barplotparent" v-bind:style="parentStyle">
          <bar-plot :yearRange="yearRange"></bar-plot>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { RootStateType } from "@/store/state";
import Vue from "vue";
import { mapState } from "vuex";
import BarPlot from "./BarPlot.vue";
import _ from "lodash";

interface State {
  parentStyle: any;
  ranges: { text: string; value: number }[];
}

export default Vue.extend({
  name: "BarPlotContainer",
  components: {
    BarPlot,
  },
  data(): State {
    return {
      parentStyle: {
        width: "100%",
      },
      ranges: [
        { text: "1 km", value: 1000 },
        { text: "5 km", value: 5000 },
        { text: "10 km", value: 10000 },
      ],
    };
  },
  computed: {
    ...mapState({
      years: function (state: RootStateType) {
        const years = state.plotData.histData.map((el) => el.YEAR_BUILT);
        return _.range(Math.min(...years), Math.max(...years)).reverse();
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
      analysisRange: (state: RootStateType) => state.plotControls.analysisRange,
      startYear: (state: RootStateType) => state.plotControls.startYear,
      endYear: (state: RootStateType) => state.plotControls.endYear,
      yearRange: (state: RootStateType) => [
        state.plotControls.startYear,
        state.plotControls.endYear,
      ],
    }),
  },
  methods: {
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
