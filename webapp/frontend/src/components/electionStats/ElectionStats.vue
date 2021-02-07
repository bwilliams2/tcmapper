<template>
  <div :style="mapContainer">
    <ElectionMap />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import ElectionMap from "./ElectionMap.vue";

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
    ElectionMap,
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
