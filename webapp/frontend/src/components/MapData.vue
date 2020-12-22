<template>
  <v-row :style="{ height: '100%' }">
    <v-col sm="12" md="6">
      <new-map />
    </v-col>
    <v-col md="12" lg="6">
      <bar-plot></bar-plot>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState } from "vuex";
import NewMap from "./NewMap.vue";
import BarPlot from "./barplot/BarPlotContainer.vue";

interface State {
  yearRange: number[];
  parentStyle: any;
}

export default Vue.extend({
  name: "Home",
  components: {
    NewMap,
    BarPlot,
  },
  data(): State {
    return {
      yearRange: [2010, 2020],
      parentStyle: {
        width: "100%",
        height: "90%",
      },
    };
  },
});
</script>
