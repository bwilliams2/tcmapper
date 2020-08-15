<template>
  <l-map
    style="height: 100%; width: 100%;"
    :zoom="zoom"
    :center="center"
    @update:zoom="zoomUpdated"
    @update:center="centerUpdated"
    @update:bounds="boundsUpdated"
  >
    <l-tile-layer :url="url"></l-tile-layer>
    <l-circle
      :lat-lng="circle.center"
      :radius="circle.radius"
      :color="circle.color"
    ></l-circle>
  </l-map>
</template>

<script lang="ts">
import Vue from "vue";
import L from "leaflet";
import { LMap, LTileLayer, LMarker, LCircle } from "vue2-leaflet";
import { mapState } from "vuex";
const apiKey = process.env.VUE_APP_HERE_API_KEY as string;

export default Vue.extend({
  name: "DensityMap",
  components: {
    LMap,
    LTileLayer,
    LCircle,
  },
  mounted() {
    this.center = [
      this.addressInfo.position.lat,
      this.addressInfo.position.lng,
    ];
    this.circle.center = [
      this.addressInfo.position.lat,
      this.addressInfo.position.lng,
    ];
  },
  data() {
    return {
      url: `https://2.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest/normal.day/{z}/{x}/{y}/512/png8?apiKey=${apiKey}&ppi=320`,
      zoom: 12,
      center: [47.41322, -1.219482],
      bounds: null,
      circle: {
        center: [47.41322, -1.0482],
        radius: 4500,
        color: "red",
      },
    };
  },
  computed: {
    ...mapState(["addressInfo"]),
  },
  methods: {
    zoomUpdated(zoom: number) {
      this.zoom = zoom;
    },
    centerUpdated(center: [number, number]) {
      this.center = center;
    },
    boundsUpdated(bounds: any) {
      this.bounds = bounds;
    },
  },
});
</script>
