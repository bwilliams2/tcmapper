<template>
  <v-card outlined elevation="7" :style="cardStyle">
    <v-container fluid>
      <v-row>
        <v-col xs="12">
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
            <div :style="{ height: '80vh' }">
              <search-map />
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
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
  containerStyle: any;
  cardStyle: any;
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
        height: "80vh",
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
  methods: {
    submitLatLng() {
      this.$store
        .dispatch("updatePlotData")
        .then(() => this.$router.push({ path: "map" }));
    },
  },
});
</script>
