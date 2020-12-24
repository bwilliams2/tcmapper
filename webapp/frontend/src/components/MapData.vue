<template>
  <v-card outlined elevation="7" :style="cardStyle">
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
              <new-map />
            </div>
          </div>
        </v-col>
        <v-col md="12" lg="6">
          <bar-plot></bar-plot>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState } from "vuex";
import NewMap from "./NewMap.vue";
import BarPlot from "./barplot/BarPlotContainer.vue";
import { MapTypes, RootStateType } from "@/store/state";

interface State {
  yearRange: number[];
  buttonContainer: any;
  parentStyle: any;
  containerStyle: any;
  cardStyle: any;
  mapTypes: { text: string; value: string }[];
}

export default Vue.extend({
  name: "Home",
  components: {
    NewMap,
    BarPlot,
  },
  computed: {
    ...mapState({
      mapType: function (state: RootStateType) {
        return state.plotControls.mapType;
      },
    }),
  },
  data(): State {
    return {
      yearRange: [2010, 2020],
      cardStyle: {
        // padding: "10px",
        margin: "15px",
      },
      mapTypes: [
        { text: "Heatmap", value: "points" },
        { text: "Parcels", value: "parcel" },
      ],
      buttonContainer: {
        position: "absolute",
        top: "15px",
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
  methods: {
    updateMapType(newValue: MapTypes) {
      this.$store.dispatch("updateMapType", newValue);
    },
  },
});
</script>
