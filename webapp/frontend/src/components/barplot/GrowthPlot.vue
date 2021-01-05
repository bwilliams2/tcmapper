<template>
  <svg
    :width="width + margins.left + margins.right"
    :height="height + margins.top + margins.bottom"
    class="growthplot"
  >
    <g class="container" :transform="`translate(${margins.left + 3}, ${10})`">
      <!-- Axes -->
      <g class="x-axis" :transform="`translate(0, ${height})`"></g>
      <g class="y-axis"></g>
      <g class="tooltip"></g>
      <g class="clippingmask">
        <g class="brush"></g>
        <g class="ylines"></g>
        <g class="ypoints"></g>
      </g>

      <!-- Grids -->
      <!-- <g>
          <g class="gf-x-grid grid" :transform="`translate(0, ${height})`"></g>
          <g class="gf-y-grid grid"></g>
        </g> -->

      <!-- Tooltip -->
      <!-- <rect :width="width" :height="height" class="overlay"></rect>
        <g class="focus">
          <rect
            width="100"
            height="30"
            class="tooltip"
            y="0"
            rx="4"
            ry="4"
          ></rect>
        </g> -->
    </g>
  </svg>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
//@ts-ignore
import { tip as d3tip } from "d3-v6-tip";
import "./barplot.css";
import { GrowthItem, RootStateType, GrowthItemPoint } from "@/store/state";
import { mapState } from "vuex";
import * as d3 from "d3";
import { SeriesPoint, stack } from "d3-shape";
import { D3BrushEvent } from "d3";

export interface Margins {
  left: number;
  right: number;
  top: number;
  bottom: number;
}

interface State {
  fullWidth: number;
  width: number;
  height: number;
  margins: Margins;
  aspectRatio: number;
  barGroup: any;
  color: any;
  tip: any;
  brush: any;
  clippingMask: any;
  hasMounted: boolean;
  minMax: {
    xMin: number;
    xMax: number;
    yMin: number;
    yMax: number;
  };
  scales: {
    x: d3.ScaleLinear<number, number, never> | null;
    y: d3.ScaleLinear<number, number, never> | null;
  };
}

interface AreaItem {
  [index: number]: number;
  key: string;
}

export default Vue.extend({
  name: "GrowthPlot",
  data(): State {
    return {
      margins: {
        left: 50,
        right: 20,
        top: 10,
        bottom: 20,
      },
      minMax: {
        xMin: 0,
        xMax: 10,
        yMin: 0,
        yMax: 10,
      },
      color: null,
      tip: null,
      brush: null,
      clippingMask: null,
      hasMounted: false,
      aspectRatio: 1.4,
      fullWidth: 0,
      width: 0,
      height: 0,
      barGroup: null,
      scales: {
        x: null,
        y: null,
      },
    };
  },
  props: {
    // histData: {
    //   type: Array as PropType<HistDataItem[]>,
    // },
    limitedData: {
      type: Array as PropType<GrowthItem[]>,
    },
    yearRange: {
      type: Array as PropType<number[]>,
    },
  },
  computed: {
    ...mapState({
      selectedUseClasses: (state) =>
        (state as RootStateType).plotControls.selectedUseClasses,
      histData: (state) => (state as RootStateType).plotData.histData,
      subgroups: function (state) {
        return Object.keys(
          (state as RootStateType).plotData.histData[0]
        ).filter((el) => el !== "YEAR_BUILT");
      },
      yearSums: (state) => (state as RootStateType).plotData.yearData,
    }),
  },
  mounted() {
    this.setMount();
  },
  watch: {
    limitedGrowthData: function () {
      if (this.hasMounted) {
        this.initGrowthPlot();
      } else {
        this.setMount();
      }
    },
  },
  methods: {
    setMount() {
      if (this.limitedData.length > 0) {
        this.initGrowthPlot();
        this.hasMounted = true;
      }
    },
    setSize() {
      const width = document.getElementById(`growthplotparent`)?.clientWidth;
      // const height = document.getElementById(`barplotparent`)?.clientHeight;
      if (typeof width !== "number") {
        throw "parentDiv undefined";
      }
      const height = width / this.aspectRatio;
      if (typeof height !== "number") {
        throw "parentDiv undefined";
      }
      this.fullWidth = width;
      this.width = this.fullWidth - this.margins.left - this.margins.right;
      this.height = height - this.margins.top - this.margins.bottom;
    },
    setScales() {
      this.minMax.xMin = Math.min(
        ...this.limitedData.map((el: GrowthItem) =>
          Math.min(...el.points.map((point) => point.YEAR_BUILT))
        )
      );
      this.minMax.xMax = Math.max(
        ...this.limitedData.map((el: GrowthItem) =>
          Math.max(...el.points.map((point) => point.YEAR_BUILT))
        )
      );
      this.minMax.yMin =
        Math.min(
          ...this.limitedData.map((el: GrowthItem) =>
            Math.min(...el.points.map((point) => point.YEAR_BUILT))
          )
        ) * 0.9;
      this.minMax.yMax =
        Math.max(
          ...this.limitedData.map((el: GrowthItem) =>
            Math.max(...el.points.map((point) => point.Rates))
          )
        ) * 1.2;
      const self = this;
      this.scales.x = d3
        .scaleLinear()
        .domain([self.minMax.xMin, self.minMax.xMax])
        .range([0, this.width]);
      this.scales.y = d3
        .scaleLinear()
        .domain([0, self.minMax.yMax])
        .range([this.height, 0]);
    },
    setAxes() {
      if (this.scales.x !== null && this.scales.y !== null) {
        d3.select(".x-axis")
          //@ts-ignore
          .call(d3.axisBottom(this.scales.x).tickSizeOuter(0))
          .selectAll(".tick line")
          .attr("stroke", "#000")
          .attr("stroke-opacity", "0.1");

        d3.select(".y-axis")
          //@ts-ignore
          .call(d3.axisLeft(this.scales.y))
          .selectAll(".tick line")
          .attr("stroke", "#000")
          .attr("stroke-opacity", "0.1");
        // Change text color
        d3.selectAll(".y-axis text").attr("color", "#999");
        d3.selectAll(".x-axis text").attr("color", "#999");

        // Change path color
        d3.selectAll(".y-axis path")
          .attr("stroke", "#000")
          .attr("stroke-opacity", "0");
        d3.selectAll(".x-axis path")
          .attr("stroke", "#999")
          .attr("stroke-opacity", "0.1");
      }
    },
    initColors() {
      const self = this;
      // color palette = one color per subgroup
      const colorRange = d3.range(0, self.subgroups.length + 1).map((el) => {
        return d3.interpolateTurbo(el / self.subgroups.length);
      });
      this.color = d3
        .scaleOrdinal(d3.schemeRdYlBu)
        .domain(self.subgroups)
        //@ts-ignore
        .range(colorRange as string[]);
    },
    initTip() {
      //@ts-ignore
      this.tip = d3tip().attr("class", "d3-tip").attr("z-index", 10000);
      d3.select(".growthplot").select(".tooltip").call(this.tip);
    },
    initBrush() {
      // Add brushing
      const self = this;
      let idleTimeout = null as null | number;
      function idled() {
        idleTimeout = null;
      }
      function updateChart(event: D3BrushEvent<GrowthItem>) {
        const extent = event.selection as [[number, number], [number, number]];
        // If no selection, back to initial coordinate. Otherwise, update X axis domain
        if (!extent) {
          if (!idleTimeout) {
            return (idleTimeout = setTimeout(idled, 350)); // This allows to wait a little bit
          }
          self.setScales();
        } else {
          self.scales.x?.domain([
            self.scales.x.invert(extent[0][0]),
            self.scales.x.invert(extent[1][0]),
          ]);
          self.scales.y?.domain([
            self.scales.y.invert(extent[1][1]),
            self.scales.y.invert(extent[0][1]),
          ]);
        }
        // Update axis and circle position
        self.updateZoom();
        d3.select(".brush").call(self.brush.move, null);
      }
      this.brush = d3
        .brush()
        .extent([
          [0, 0],
          [this.width, this.height],
        ])
        .on("end", updateChart); // Each time the brush selection changes, trigger the 'updateChart' function
      //@ts-ignore
      d3.select(".brush").call(this.brush);
    },
    initLines(delay = 750) {
      const self = this;

      const t = d3.transition().duration(delay).ease(d3.easeLinear) as any;
      const xScale = self.scales.x;
      const yScale = self.scales.y;

      if (xScale && yScale) {
        const lineFunc = (d: GrowthItem) => {
          return d3
            .line<GrowthItemPoint>()
            .x(function (d): number {
              return xScale(d.YEAR_BUILT);
            })
            .y(function (d): number {
              return yScale(d.Rates);
            })(d.points);
        };

        const zeroLineFunc = (d: GrowthItem) => {
          return d3
            .line<GrowthItemPoint>()
            .x(xScale(self.minMax.xMin))
            .y(yScale(self.minMax.yMin))(d.points);
        };

        const lines = d3
          .select(".ylines")
          .selectAll("path")
          .data<GrowthItem>(this.limitedData, function (d) {
            return (d as GrowthItem).id;
          });
        lines
          .exit()
          .transition(t)
          //@ts-ignore
          .attr("d", zeroLineFunc)
          .remove();

        lines
          .enter()
          .append("path")
          //@ts-ignore
          .attr("fill", "none")
          .attr("stroke", function (d) {
            return self.color(d.id);
          })
          .attr("stroke-width", 1.5)
          .attr("d", zeroLineFunc)
          //@ts-ignore
          // .on("mouseover", mouseAction)
          // .on("mouseout", self.tip.hide)
          .transition(t)
          //@ts-ignore
          .attr("d", lineFunc);

        lines.attr("d", lineFunc);
        //@ts-ignore
        // .on("mouseover", mouseAction);
      }
    },
    initPoints(delay = 750) {
      const self = this;

      const t = d3.transition().duration(delay).ease(d3.easeLinear) as any;
      const xScale = self.scales.x;
      const yScale = self.scales.y;

      function mouseAction(this: SVGCircleElement, event: any, d: unknown) {
        if (xScale && yScale) {
          const data = d as GrowthItemPoint;
          self.tip.html(
            "<span>" +
              `Use Class: ${data.USECLASS1}<br>` +
              `Year Built: ${data.YEAR_BUILT}<br>` +
              `New: ${data.New}<br>` +
              `Rate: ${Math.round(data.Rates * 1000) / 10}%` +
              "</span>"
          );
          self.tip.show(d, this);
        }
      }

      if (xScale && yScale) {
        let parents = d3
          .select(".ypoints")
          .selectAll(".circlegroup")
          .data<GrowthItem>(this.limitedData, function (d) {
            return (d as GrowthItem).id;
          });

        parents
          .exit()
          .selectAll("circle")
          .transition(t)
          .attr("cx", 0)
          .attr("cy", self.height)
          .attr("r", 0);

        const parentsEnter = parents
          .enter()
          .append("g")
          .attr("class", "circlegroup")
          .style("fill", function (d) {
            return self.color(d.id);
          });

        parents = parentsEnter.merge(parents as any) as any;
        const points = parents.selectAll("circle").data(function (d) {
          return d.points;
        });

        points
          .exit()
          .transition(t)
          .attr("cx", 0)
          .attr("cy", this.height)
          .attr("r", 0)
          .remove();

        points
          .enter()
          .append("circle")
          .attr("cx", 0)
          .attr("cy", this.height)
          .attr("r", 0)
          .on("mouseover", mouseAction)
          .on("mouseout", self.tip.hide)
          .transition(t)
          .attr("cx", function (d) {
            return xScale(d.YEAR_BUILT);
          })
          .attr("cy", function (d) {
            return yScale(d.Rates);
          })
          .attr("r", 8);

        points
          .transition(t)
          .attr("cx", function (d) {
            return xScale(d.YEAR_BUILT);
          })
          .attr("cy", function (d) {
            return yScale(d.Rates);
          });
      }
    },
    updateZoom() {
      this.setAxes();
      this.initLines(50);
      this.initPoints(50);
    },
    initGrowthPlot() {
      this.setSize();
      this.setScales();
      this.setAxes();
      this.initTip();

      this.initBrush();
      this.initColors();
      this.initLines();
      this.initPoints();
    },
  },
});
</script>
