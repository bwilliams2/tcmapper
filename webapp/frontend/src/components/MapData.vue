<template>
  <v-row :style="{ height: '100%' }">
    <v-col sm="12" md="6">
      <new-map />
    </v-col>
    <v-col sm="12" md="6">
      <div id="barplotparent" v-bind:style="parentStyle">
        <bar-plot :yearRange="yearRange"></bar-plot>
      </div>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import { mapState } from "vuex";
import NewMap from "./NewMap.vue";
import BarPlot from "./charts/BarPlot.vue";

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
