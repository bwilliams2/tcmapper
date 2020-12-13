<template>
  <div id="map" style="width: 100%; height: 100%"></div>
</template>

<script lang="ts">
import Vue from "vue";
import L, { LatLngTuple, TileLayer, LatLngBounds } from "leaflet";
// import { LMap, LTileLayer, LMarker, LCircle } from "vue2-leaflet";
import { mapState } from "vuex";
import * as d3 from "d3";
import { GeoProjection } from "d3-geo";
import { FeatureCollection } from "geojson";
import "leaflet.heat";
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
  circle: {
    center: LatLngTuple;
    radius: number;
    color: string;
  };
  features: FeatureCollection;
}

type DataPoints = [number, number];

export default Vue.extend({
  name: "DensityMap",
  mounted() {
    // this.initLayers();
    this.center = [
      this.addressInfo.position.lat,
      this.addressInfo.position.lng,
    ];
    this.circle.center = [
      this.addressInfo.position.lat,
      this.addressInfo.position.lng,
    ];
    this.features.features = [
      {
        type: "Feature",
        properties: [
          {
            name: "Address",
          },
        ],
        geometry: {
          type: "Point",
          coordinates: this.center,
        },
      },
    ];
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
      circle: {
        center: [47.41322, -1.0482],
        radius: 14,
        color: "red",
      },
      features: {
        type: "FeatureCollection",
        features: [],
      },
    };
  },
  computed: {
    ...mapState(["addressInfo"]),
  },
  methods: {
    initMap() {
      this.map = L.map("map", {
        center: this.center,
        zoom: this.zoom.start,
      });
      this.tileLayer = L.tileLayer(this.url, {
        maxZoom: 18,
        attribution:
          "Map Tiles &copy; " +
          new Date().getFullYear() +
          " " +
          '<a href="http://developer.here.com">HERE</a>',
      });
      this.tileLayer.addTo(this.map);
      // @ts-ignore
      L.heatLayer(this.$state.plotData.locationData).addTo(this.map);
      const parentDiv = document.getElementById("map");
      if (parentDiv !== null) {
        this.svg = d3
          .select(this.map.getPanes().overlayPane)
          .append("svg")
          .attr("height", parentDiv.clientHeight)
          .attr("width", parentDiv.clientWidth);
      }
      this.svgGroup = this.svg.append("g").attr("class", "leaflet-zoom-hide");
      this.updateLayers();
    },
    updateLayers() {
      const map = this.map;
      function projectPoint(this: any, x: number, y: number) {
        const point = map.latLngToLayerPoint(new L.LatLng(y, x));
        this.stream.point(point.x, point.y);
      }
      const transform = d3.geoTransform({ point: projectPoint });
      const path = d3.geoPath().projection(transform);

      const collection = this.features;

      // const feature = this.svgGroup
      //   .selectAll("path")
      //   .data(collection.features)
      //   .enter()
      //   .append("path")
      // feature.attr("d", path);
      const circleCoords = this.circle.center;
      // let circleRadius = this.circle.radius;
      const feature = this.svgGroup
        .selectAll("circle")
        .data([circleCoords])
        .enter()
        .append("circle")
        .attr("cx", function (d: DataPoints) {
          return map.latLngToLayerPoint(d).x;
        })
        .attr("cy", function (d: DataPoints) {
          return map.latLngToLayerPoint(d).y;
        })
        .attr("r", this.circle.radius)
        .style("fill", "red")
        .attr("stroke", "red")
        .attr("stroke-width", 3)
        .attr("fill-opacity", 0.4);

      const svg = this.svg;
      const svgGroup = this.svgGroup;
      const self = this;

      const currentZoom = {
        start: map.getZoom(),
        end: map.getZoom(),
      };
      function update() {
        self.svgGroup
          .selectAll("circle")
          .attr("cx", function (d: DataPoints) {
            return map.latLngToLayerPoint(d).x;
          })
          .attr("cy", function (d: DataPoints) {
            return map.latLngToLayerPoint(d).y;
          });
        const bounds = path.bounds(collection);
        // let topLeft = bounds[0];
        // let bottomRight = bounds[1];
        currentZoom.end = map.getZoom();
        const diff = currentZoom.start - currentZoom.end;
        if (diff > 0) {
          self.circle.radius = self.circle.radius / 2;
        } else if (diff < 0) {
          self.circle.radius = self.circle.radius * 2;
        }
        self.drawCircles([circleCoords]);
        // If there is only one circle the bounds are defined by a single point
        // Need to adjust for that here
        // if (topLeft[0] === bottomRight[0]) {
        //   topLeft = [topLeft[0] - 2 * circleRadius, topLeft[1] - 2 * circleRadius];
        //   bottomRight = [bottomRight[0] + 2 * circleRadius, bottomRight[1] + 2 * circleRadius];
        // }
        // svg
        //   .attr("height", bottomRight[0] - topLeft[0])
        //   .attr("width", bottomRight[1] - topLeft[1])
        //   .style("left", topLeft[0] + "px")
        //   .style("top", topLeft[1] + "px");
        // svgGroup.attr(
        //   "transform",
        //   "translate(" + -topLeft[0] + "," + -topLeft[1] + ")"
        // );
      }
      map.on("zoomstart", function () {
        currentZoom.start = map.getZoom();
      });
      // if (diff > 0) { circle.setRadius(circle.getRadius() * 2); } else if (diff < 0) { circle.setRadius(circle.getRadius() / 2); }
      map.on("viewreset", update);
      map.on("moveend", update);
      update();
    },
    drawCircles(circleCoords: [number, number][]) {
      const map = this.map;
      const self = this;
      this.svgGroup
        .selectAll("circle")
        .data(circleCoords)
        .enter()
        .append("circle")
        .attr("cx", function (d: DataPoints) {
          return map.latLngToLayerPoint(d).x;
        })
        .attr("cy", function (d: DataPoints) {
          return map.latLngToLayerPoint(d).y;
        })
        .attr("r", self.circle.radius)
        .style("fill", "red")
        .attr("stroke", "red")
        .attr("stroke-width", 3)
        .attr("fill-opacity", 0.4);
      this.svgGroup
        .selectAll("circle")
        .data(circleCoords)
        .attr("r", self.circle.radius);
    },
    // initLayers() {},
    zoomUpdated(zoom: { start: number; end: number }) {
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
