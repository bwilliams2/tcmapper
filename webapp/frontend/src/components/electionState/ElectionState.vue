<template>
  <div :style="containerStyle">
    <div :style="buttonContainer">
      <v-card outlined elevation="3">
        <v-select
          :items="properties"
          :value="selectedColorProperty"
          label="Map Overlay"
          @input="updateSelectedColorProperty"
          :style="{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
      </v-card>
    </div>
    <div :style="mapContainer">
      <ElectionMap />
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { mapGetters } from "vuex";
import ElectionMap from "./ElectionMap.vue";

interface State {
  mapContainer: {
    position: "absolute";
    height: "100%";
    width: "100%";
  };
  buttonContainer: {
    position: string;
    top: string;
    left: string;
    width: string;
    zIndex: number;
  };
  containerStyle: {
    position: string;
    width: string;
    height: string;
  };
  parentStyle: {
    width: string;
    height: string;
  };
}

export default Vue.extend({
  name: "Home",
  components: {
    ElectionMap,
  },
  data(): State {
    return {
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
      mapContainer: {
        position: "absolute",
        height: "100%",
        width: "100%",
      },
    };
  },
  computed: {
    ...mapGetters("election", {
      properties: "properties",
      selectedYear: "selectedYear",
      selectedColorProperty: "selectedColorProperty",
    }),
  },
  methods: {
    updateSelectedColorProperty(newValue: string) {
      this.$store.dispatch("election/updateColorProperty", newValue);
    },
    updateSelectedYear(newValue: string) {
      this.$store.dispatch("election/updateYear", parseInt(newValue));
    },
  },
});
</script>
