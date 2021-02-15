<template>
  <div :style="containerStyle">
    <div :style="plotContainer">
      <v-card outlined elevation="3">
        <model-container></model-container>
      </v-card>
    </div>
    <div :style="mapContainer">
      <ElectionMap />
    </div>
  </div>
</template>

<script lang="ts">
import { RootStateType } from "@/store/state";
import Vue, { PropType } from "vue";
import { mapGetters, mapState } from "vuex";
import ElectionMap from "./ElectionMap.vue";
import ModelContainer from "./ModelContainer.vue";

interface State {
  plotContainer: {
    position: string;
    top: string;
    zIndex: number;
    // backgroundColor: string;
    right: string;
    left: string;
    // width: window.innerWidth * 0.35,
    height: string;
    padding: string;
  };
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
  availableProperties: string[];
}

export default Vue.extend({
  name: "Home",
  components: {
    ElectionMap,
    ModelContainer,
  },
  data(): State {
    return {
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
      availableProperties: [],
    };
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  },
  computed: {
    ...mapGetters("election", {
      properties: "properties",
      categories: "categories",
      years: "years",
      selectedYear: "selectedYear",
      selectedProperty: "selectedProperty",
      selectedCategory: "selectedCategory",
    }),
    ...mapGetters("model", {
      closestIDs: "closestIDs",
    }),
  },
  methods: {
    updateSelectedProperty(newValue: string) {
      this.$store.dispatch("election/updateSelectedProperty", newValue);
    },
    updateSelectedCategory(newValue: string) {
      this.$store.dispatch("election/updateSelectedCategory", newValue);
    },
    updateSelectedYear(newValue: string) {
      this.$store.dispatch("election/updateYear", parseInt(newValue));
    },
    handleResize() {
      this.containerStyle.height = window.innerHeight - 64 + "px";
      this.plotContainer.left = window.innerWidth * 0.55 + "px";
      this.plotContainer.height = window.innerHeight - 64 - 60 + "px";
    },
  },
});
</script>
