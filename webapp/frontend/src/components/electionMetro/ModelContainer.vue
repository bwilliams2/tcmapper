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
            label="Mean EMV"
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
            label="Mean Age"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          ></v-slider>
          <v-slider
            :value="cityDis"
            @change="updateCityDis"
            :min="cityDisLimits[0]"
            :max="cityDisLimits[1]"
            label="City Dis"
            thumb-label="always"
            thumb-size="35"
            :style="{ margin: '20px' }"
          >
            <template v-slot:thumb-label="item"> {{ item.value }} mi </template>
          </v-slider>
        </v-col>
      </v-row>
      <v-row class="fill-height">
        <v-col cols="12">
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
  },
  mounted() {
    this.$store.dispatch("model/updateControlLimits");
  },
  computed: {
    ...mapGetters("model", {
      meanEMV: "meanEMV",
      meanAge: "meanAge",
      cityDis: "cityDis",
      meanEMVLimits: "meanEMVLimits",
      meanAgeLimits: "meanAgeLimits",
      cityDisLimits: "cityDisLimits",
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
    resetAnalysis() {
      this.$store.dispatch("resetAnalysis");
    },
  },
});
</script>
