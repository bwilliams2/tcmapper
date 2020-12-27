<template>
  <div id="map" style="width: 100%; height: 100%"></div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import L, { LatLngTuple, TileLayer, LatLngBounds, Circle } from "leaflet";
//@ts-ignore
import geojsonvt from "geojson-vt";
// import { LMap, LTileLayer, LMarker, LCircle } from "vue2-leaflet";
import { mapState } from "vuex";
import * as d3 from "d3";
import { GeoProjection } from "d3-geo";
import { FeatureCollection } from "geojson";
import "leaflet.heat";
import "leaflet.vectorgrid";
import { RootStateType, FeatureItem } from "@/store/state";
const apiKey = process.env.VUE_APP_HERE_API_KEY as string;

interface Feature {
  type: string;
  properties: { name: string }[];
  geometry: {
    type: string;
    coordinates: LatLngTuple;
  };
}

interface Features {
  type: string;
  features: Feature[];
}

interface MapData {
  url: string;
  zoom: { start: number; end: number };
  center: LatLngTuple;
  bounds: LatLngBounds | null;
  map: any;
  svg: any;
  svgGroup: any;
  layers: any[];
  tileLayer: TileLayer | null;
  circleLayer: Circle | null;
}

type DataPoints = [number, number];

export default Vue.extend({
  name: "SearchMap",
  mounted() {
    // this.initLayers();
    this.initMap();
  },
  beforeDestroy() {
    this.map.off();
    this.map.remove();
  },
  data(): MapData {
    return {
      url: `https://2.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest/normal.day/{z}/{x}/{y}/512/png8?apiKey=${apiKey}&ppi=320`,
      zoom: { start: 12, end: 12 },
      center: [44.98752, -93.248841],
      bounds: null,
      map: null,
      svg: null,
      svgGroup: null,
      layers: [],
      tileLayer: null,
      circleLayer: null,
    };
  },
  computed: {
    ...mapState({
      latLng: function (state: RootStateType) {
        return state.plotControls.latLng;
      },
      analysisRange: (state: RootStateType) => state.plotControls.analysisRange,
    }),
  },
  methods: {
    initMap() {
      this.map = L.map("map", {
        center: this.center,
        zoom: this.zoom.start,
      });
      this.tileLayer = L.tileLayer(this.url, {
        maxZoom: 15,
        attribution:
          "Map Tiles &copy; " +
          new Date().getFullYear() +
          " " +
          '<a href="http://developer.here.com">HERE</a>',
      });
      this.tileLayer.addTo(this.map);
      this.initLayers();
    },
    initLayers() {
      const self = this;
      function getLatLng(e: any) {
        const latLng = [e.latlng.lat, e.latlng.lng] as [number, number];
        if (self.circleLayer) {
          self.map.removeLayer(self.circleLayer);
        }
        self.circleLayer = L.circle(latLng, {
          color: "red",
          fillColor: "#f03",
          fillOpacity: 0.5,
          radius: self.analysisRange,
        });
        self.circleLayer.addTo(self.map);
        self.$store.dispatch("updateLatLng", latLng);
        console.log("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng);
      }
      this.map.on("click", getLatLng);
    },
  },
});
</script>
