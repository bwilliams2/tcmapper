<template>
  <div id="map" style="width: 100%; height: 100%"></div>
</template>

<script lang="ts">
import Vue from "vue";
import L, { LatLngTuple, TileLayer, LatLngBounds } from "leaflet";
//@ts-ignore
import geojsonvt from "geojson-vt";
// import { LMap, LTileLayer, LMarker, LCircle } from "vue2-leaflet";
import { mapState } from "vuex";
import * as d3 from "d3";
import { GeoProjection } from "d3-geo";
import { FeatureCollection } from "geojson";
import "leaflet.heat";
import "leaflet.vectorgrid";
import { RootStateType } from "@/store/state";
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
  currentLayer: TileLayer | null;
}

type DataPoints = [number, number];

export default Vue.extend({
  name: "DensityMap",
  mounted() {
    // this.initLayers();
    const { lat, lng } = this.addressInfo.position;
    if (lat && lng) {
      this.center = [lat, lng];
    }
    this.initMap();
  },
  data(): MapData {
    return {
      url: `https://2.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest/normal.day/{z}/{x}/{y}/512/png8?apiKey=${apiKey}&ppi=320`,
      zoom: { start: 12, end: 12 },
      center: [47.41322, -1.219482],
      bounds: null,
      map: null,
      svg: null,
      svgGroup: null,
      layers: [],
      tileLayer: null,
      currentLayer: null,
    };
  },
  computed: {
    ...mapState({
      addressInfo: function (state: RootStateType) {
        return state.addressInfo;
      },
      mapType: (state: RootStateType) => state.plotControls.mapType,
      features: (state: RootStateType) => state.plotData.features,
      locationData: (state: RootStateType) => state.plotData.locationData,
    }),
  },
  watch: {
    mapType: function () {
      this.initLayers();
    },
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
      if (this.currentLayer) {
        this.map.removeLayer(this.currentLayer);
      }
      if (this.mapType == "points") {
        // @ts-ignore
        this.currentLayer = L.heatLayer(this.locationData, { max: 2020 });
        this.currentLayer?.addTo(this.map);
        // console.log("in")
      } else {
        const geoJsonConstruct = {
          type: "FeatureCollection",
          features: this.features,
        };
        //@ts-ignore
        this.currentLayer = L.vectorGrid.slicer(geoJsonConstruct, {
          vectorTileLayerStyles: {
            sliced: {
              fillColor: "transparent",
              color: "blue",
              weight: 0.5,
            },
          },
          maxZoom: 15,
          // indexMaxZoom: 5, // max zoom in the initial tile index
          // interactive: true,
          // getFeatureId: function(feature) {
          //     return feature.properties["cartodb_id"]
          // }
        });
        this.currentLayer?.addTo(this.map);
        // tileLayer.on('click', function(e) {
        //   console.log(e);
        //   if (e.layer.feature) {
        //     var prop = e.layer.feature.properties;
        //     //var latlng = [e.latlng.lat,e.latlng.lng];
        //   } else {
        //     var prop = e.layer.properties;
        //     //var latlng = [Number(parcel.y),Number(parcel.x)];
        //   }
        //   //settimeout otherwise when map click fires it will override this color change
        //   if (id != 0) {
        //     tileLayer.setFeatureStyle(id, {
        //       color: "blue",
        //       weight: 0.5,
        //     });
        //   }
        //   id = prop["cartodb_id"];
        //   setTimeout(function () {
        //     tileLayer.setFeatureStyle(id, { color: "red" }, 100);
        //   });
        // });
      }
    },
  },
});
</script>
