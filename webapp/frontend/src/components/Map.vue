<template>
  <div>
    <l-map
      style="height: 80%; width: 100%"
      :zoom="zoom"
      :center="[addressInfo.position.lat, addressInfo.position.lon]"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
    >
      <l-tile-layer :url="url"></l-tile-layer>
    </l-map>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import { mapState } from "vuex";
const apiKey = process.env.VUE_APP_HERE_API_KEY as string;

export default Vue.extend({
  name: "DensityMap",
  components: {
    LMap,
    LTileLayer
  },
  data() {
    return {
      url: `https://2.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest/normal.day/{z}/{x}/{y}/512/png8?apiKey=${apiKey}&ppi=320`,
      zoom: 3,
      // center: [47.413220, -1.219482],
      bounds: null
    };
  },
  computed: {
    ...mapState(["addressInfo"])
  },
  methods: {
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    centerUpdated(center) {
      this.center = center;
    },
    boundsUpdated(bounds) {
      this.bounds = bounds;
    }
  }
});
</script>
