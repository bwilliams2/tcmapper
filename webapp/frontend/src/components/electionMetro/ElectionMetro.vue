<template>
  <div :style="containerStyle">
    <!-- <div :style="buttonContainer">
      <v-card outlined elevation="3">
        <v-select
          :items="years"
          :value="selectedYear"
          label="Election Year"
          @input="updateSelectedYear"
          :style="{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
        <v-select
          :items="categories"
          :value="selectedCategory"
          label="Category"
          @input="updateSelectedCategory"
          :style="{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
        <v-select
          :items="properties"
          :value="selectedProperty"
          label="Property"
          @input="updateSelectedProperty"
          :style="    <div :style="buttonContainer">
      <v-card outlined elevation="3">
        <v-select
          :items="years"
          :value="selectedYear"
          label="Election Year"
          @input="updateSelectedYear"
          :style="{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
        <v-select
          :items="categories"
          :value="selectedCategory"
          label="Category"
          @input="updateSelectedCategory"
          :style="{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
        <v-select
          :items="properties"
          :value="selectedProperty"
          label="Property"
          @input="updateSelectedProperty"
          :style="{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
      </v-card>
    </div>{
            marginLeft: '10px',
            marginRight: '10px',
            marginBottom: '-10px',
          }"
        ></v-select>
      </v-card>
    </div> -->
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
  availableProperties: string[];
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
      availableProperties: [],
    };
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
  },
});
</script>
