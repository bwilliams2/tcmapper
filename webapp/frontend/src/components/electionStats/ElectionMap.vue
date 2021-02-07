<template>
  <div id="map" style="width: 100%; height: 100%"></div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import L, { LatLngTuple, TileLayer, LatLngBounds, Circle } from "leaflet";
//@ts-ignore
import geojsonvt from "geojson-vt";
// import { LMap, LTileLayer, LMarker, LCircle } from "vue2-leaflet";
import { mapGetters, mapState } from "vuex";
import * as d3 from "d3";
import { ScaleSequential } from "d3";
import { GeoProjection } from "d3-geo";
import { FeatureCollection } from "geojson";
import "leaflet.heat";
import "leaflet.vectorgrid";
import { RootStateType, FeatureItem } from "@/store/state";
const apiKey = process.env.VUE_APP_HERE_API_KEY as string;

function colorIsSequential(color: unknown): color is ScaleSequential<"string"> {
  return color !== null;
}

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
  circleLayer: Circle | null;
}

type DataPoints = [number, number];

export default Vue.extend({
  name: "ElectionMap",
  mounted() {
    // this.initLayers();
    this.getPrecincts();
  },
  beforeDestroy() {
    this.map.off();
    this.map.remove();
  },
  props: {
    selectedFeatures: {
      type: Array as PropType<FeatureItem[]>,
    },
    selectedLocations: {
      type: Array as PropType<[number, number, number][]>,
    },
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
      currentLayer: null,
      circleLayer: null,
    };
  },
  computed: {
    ...mapGetters("election", {
      features: "features",
      properties: "properties",
      selectedProperty: "selectedProperty",
    }),
  },
  watch: {
    mapType: function () {
      this.initLayers();
    },
    selectedProperty: function () {
      this.initLayers();
    },
  },
  methods: {
    async getPrecincts() {
      await this.$store.dispatch("election/updateParcels");
      this.initMap();
    },
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
      const centerLatLng = new L.LatLng(
        this.center[0] as number,
        this.center[1] as number
      );
      const centerPoint = this.map.latLngToContainerPoint(centerLatLng);
      const offset = this.map.getSize().x * 0.2;
      centerPoint.x += offset;

      // Set center to latLng
      this.map.panTo(this.map.layerPointToLatLng(centerPoint));
      // Calculate the offset
      // Then move the map
      // this.map.panBy(new L.Point(-offset, 0), { animate: false });
      this.initLayers();
    },
    initLayers() {
      const self = this;

      //@ts-ignore

      // Define popup for parcel map
      function popup(e: any) {
        L.popup()
          .setContent(
            // `<span>USECLASS: ${e.layer.properties.USECLASS1}</span><br><span>YEAR_BUILT: ${e.layer.properties.YEAR_BUILT}</span>`
            "<span>Test item</span>"
          )
          .setLatLng(e.latlng)
          .openOn(self.map);
      }

      // Remove current overlay layer if it exists already
      if (this.currentLayer) {
        this.map.removeLayer(this.currentLayer);
      }

      if (this.selectedProperty !== null) {
        const selectedProperty = this.selectedProperty;
        const propertyVals = this.features.map(
          (el: Record<string, number | string>) => el[selectedProperty]
        );
        const propertyType = this.features[0][this.selectedProperty];
        let color = null as ScaleSequential<"string"> | null;
        if (propertyType === "string") {
          // Set color scheme for parcel map
          propertyVals.sort();
          color = d3
            .scaleSequential(d3.interpolateRdYlBu)
            .domain(propertyVals) as ScaleSequential<"string">;
        } else {
          propertyVals.sort(d3.ascending);
          const domain = d3.extent(propertyVals as number[]);
          if (domain) {
            color = d3
              .scaleSequential(d3.interpolateViridis)
              .domain(domain as number[]) as ScaleSequential<"string">;
          }
        }
        if (colorIsSequential(color)) {
          // Construct GEOJson FeatureCollection
          const geoJsonConstruct = {
            type: "FeatureCollection",
            features: this.features,
          };
          //@ts-ignore
          this.currentLayer = L.vectorGrid.slicer(geoJsonConstruct, {
            vectorTileLayerStyles: {
              sliced: function (properties: any) {
                //@ts-ignore
                const parcelColor = d3
                  .color(
                    (color as ScaleSequential<"string">)(
                      properties[selectedProperty]
                    )
                  )
                  .formatHex();
                return {
                  //@ts-ignore
                  fill: true,
                  fillColor: parcelColor,
                  fillOpacity: 0.8,
                  color: "black",
                  opacity: 0.9,
                  weight: 0.5,
                };
              },
            },
            maxZoom: 15,
            // indexMaxZoom: 5, // max zoom in the initial tile index
            interactive: true,
            // getFeatureId: function(feature) {
            //     return feature.properties["cartodb_id"]
            // }
          });
          this.tileLayer?.setOpacity(0.7);
          this.currentLayer?.addTo(this.map);
          this.currentLayer?.on("click", popup);
        }
      }
    },
  },
});
</script>
