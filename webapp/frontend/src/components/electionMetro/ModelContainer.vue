<template>
  <div>
    <v-container fluid>
      <v-row no-gutters>
        <v-col cols="12">
          <v-row no-gutters align="start" justify="start">
            <v-col cols="8">
              <div class="text-h6" :style="{ marginBottom: '15px' }">
                Metro Margin Change Model
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-slider
            :value="meanEMV"
            @change="updateMeanEMV"
            :min="meanEMVLimits[0]"
            :max="meanEMVLimits[1]"
            label="Mean Estimated House Value"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item">
              ${{ parseInt(item.value / 1000) }}k
            </template>
          </v-slider>
          <v-slider
            :value="meanAge"
            @change="updateMeanAge"
            :min="meanAgeLimits[0]"
            :max="meanAgeLimits[1]"
            label="Mean House Age"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          ></v-slider>
          <v-slider
            :value="cityDis"
            @change="updateCityDis"
            :min="cityDisLimits[0]"
            :max="cityDisLimits[1]"
            label="Distance to City Center"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item"> {{ item.value }} mi </template>
          </v-slider>
          <v-slider
            :value="voteDensity"
            @change="updateVoteDensity"
            :min="voteDensityLimits[0]"
            :max="voteDensityLimits[1]"
            label="Vote Density"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item">
              {{ parseInt(item.value / 1000) }}
            </template>
          </v-slider>
          <v-slider
            :value="growth * 1000"
            @change="updateGrowth"
            :min="growthLimits[0] * 1000"
            :max="growthLimits[1] * 1000"
            label="5-year SFH Growth"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item">
              {{ item.value / 10 }}%
            </template>
          </v-slider>
          <v-slider
            :value="medianAge"
            @change="updateMedianAge"
            :min="medianAgeLimits[0]"
            :max="medianAgeLimits[1]"
            label="Median Age"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item">
              {{ item.value / 10 }}%
            </template>
          </v-slider>
          <v-slider
            :value="medianInc"
            @change="updateMedianInc"
            :min="medianIncLimits[0]"
            :max="medianIncLimits[1]"
            label="Median Income"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item">
              {{ item.value / 1000 }}k
            </template>
          </v-slider>
          <v-slider
            :value="ratioOneHouse"
            @change="updateRatioOneHouse"
            :min="ratioOneHouseLimits[0]"
            :max="ratioOneHouseLimits[1]"
            label="Ratio in House for < 4 years"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item">
              {{ item.value / 1000 }}k
            </template>
          </v-slider>
        </v-col>
      </v-row>
      <v-row class="fill-height">
        <v-col cols="12">
          <div class="text-h5">Prediction: {{ predictedMargin.toFixed() }}</div>
          <!-- <div
            id="barplotparent"
            v-bind:style="parentStyle"
            v-if="chart == 'bar'"
          >
            <bar-plot
              :limitedData="limitedData"
              :yearRange="yearRange"
            ></bar-plot>
          </div>
          <div
            id="areaplotparent"
            v-bind:style="parentStyle"
            v-if="chart == 'area'"
          >
            <area-plot
              :limitedData="limitedData"
              :yearRange="yearRange"
            ></area-plot>
          </div>
          <div
            id="growthplotparent"
            v-bind:style="parentStyle"
            v-if="chart == 'growth'"
          >
            <growth-plot
              :limitedData="limitedGrowthData"
              :yearRange="yearRange"
            ></growth-plot>
          </div> -->
        </v-col>
      </v-row>
    </v-container>
    <!-- <v-dialog
    v-model="dialog"
    width="500"
  >
    <v-card :style="{ position: 'absolute', left: '20px', top: '100px'}">
      
    </v-card>
  </v-dialog> -->
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { mapGetters, mapState } from "vuex";
import { HistDataItem, RootStateType, GrowthItem } from "@/store/state";
import _ from "lodash";
import { select } from "d3";

interface State {
  parentStyle: any;
  chart: string;
  charts: { text: string; value: string }[];
  ranges: { text: string; value: number }[];
}

export default Vue.extend({
  name: "ModelContainer",
  // components: {
  //   BarPlot,
  //   AreaPlot,
  //   GrowthPlot,
  // },
  data(): State {
    return {
      parentStyle: {
        width: "100%",
      },
      chart: "bar",
      charts: [
        { text: "Bar Chart", value: "bar" },
        { text: "Area Chart", value: "area" },
        { text: "Growth Chart", value: "growth" },
      ],
      ranges: [
        { text: "1 km", value: 1000 },
        { text: "5 km", value: 5000 },
        { text: "10 km", value: 10000 },
      ],
    };
  },
  props: {
    limitedData: {
      type: Array as PropType<HistDataItem[]>,
    },
    limitedGrowthData: {
      type: Array as PropType<GrowthItem[]>,
    },
  },
  created() {
    this.updateClosestIDs = _.debounce(this.updateClosestIDs, 500);
  },
  watch: {
    cityDis: function () {
      this.updateClosestIDs();
    },
    meanEMV: function () {
      this.updateClosestIDs();
    },
    meanAge: function () {
      this.updateClosestIDs();
    },
    voteDensity: function () {
      this.updateClosestIDs();
    },
    growth: function () {
      this.updateClosestIDs();
    },
  },
  mounted() {
    this.$store.dispatch("model/updateControlLimits");
  },
  computed: {
    ...mapGetters("model", {
      meanEMV: "meanEMV",
      meanAge: "meanAge",
      cityDis: "cityDis",
      growth: "growth",
      voteDensity: "voteDensity",
      medianAge: "medianAge",
      medianInc: "medianInc",
      ratioOneHouse: "ratioOneHouse",
      predictedMargin: "predictedMargin",
      meanEMVLimits: "meanEMVLimits",
      meanAgeLimits: "meanAgeLimits",
      cityDisLimits: "cityDisLimits",
      growthLimits: "growthLimits",
      medianAgeLimits: "medianAgeLimits",
      medianIncLimits: "medianIncLimits",
      ratioOneHouseLimits: "ratioOneHouseLimits",
      voteDensityLimits: "voteDensityLimits",
      closestIDs: "closetIDs",
      metroData: "metroData",
    }),
  },
  methods: {
    updateClosestIDs() {
      this.$store.dispatch("model/updateClosestIDs");
    },
    updateCityDis(newDis: number) {
      this.$store.dispatch("model/updateCityDis", newDis);
    },
    updateMeanEMV(newEMV: number) {
      this.$store.dispatch("model/updateMeanEMV", newEMV);
    },
    updateMeanAge(newAge: number) {
      this.$store.dispatch("model/updateMeanAge", newAge);
    },
    updateGrowth(newGrowth: number) {
      this.$store.dispatch("model/updateGrowth", newGrowth / 1000);
    },
    updateVoteDensity(newVoteDensity: number) {
      this.$store.dispatch("model/updateVoteDensity", newVoteDensity);
    },
    updateMedianAge(newMedianAge: number) {
      this.$store.dispatch("model/updateMedianAge", newMedianAge);
    },
    updateMedianInc(newMedianInc: number) {
      this.$store.dispatch("model/updateMedianInc", newMedianInc);
    },
    updateRatioOneHouse(newRatioOneHouse: number) {
      this.$store.dispatch("model/updateRatioOneHouse", newRatioOneHouse);
    },
    resetAnalysis() {
      this.$store.dispatch("resetAnalysis");
    },
  },
});
</script>
