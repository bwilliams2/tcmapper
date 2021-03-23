<template>
  <div :style="mapContainer">
    <ParcelMap />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import ParcelMap from "./ParcelMap.vue";

interface State {
  mapContainer: {
    position: "absolute";
    height: "100%";
    width: "100%";
  };
}

export default Vue.extend({
  name: "Home",
  components: {
    ParcelMap,
  },
  data(): State {
    return {
      mapContainer: {
        position: "absolute",
        height: "100%",
        width: "100%",
      },
    };
  },
});
</script>
