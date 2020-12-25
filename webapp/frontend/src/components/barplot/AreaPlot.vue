<template>
  <svg
    :width="width + margins.left + margins.right"
    :height="height + margins.top + margins.bottom"
    class="barplot"
  >
    <g class="container" :transform="`translate(${margins.left + 3}, ${10})`">
      <!-- Axes -->
      <g class="x-axis" :transform="`translate(0, ${height})`"></g>
      <g class="y-axis"></g>
      <g class="stacks"></g>
      <g class="tooltip"></g>

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
import { HistDataItem, RootStateType } from "../../store/state";
import { mapState } from "vuex";
import * as d3 from "d3";
import { SeriesPoint, stack } from "d3-shape";

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
  limitedData: HistDataItem[];
  barGroup: any;
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
  name: "BarPlot",
  data(): State {
    return {
      margins: {
        left: 50,
        right: 20,
        top: 10,
        bottom: 20,
      },
      aspectRatio: 1.4,
      fullWidth: 0,
      width: 0,
      height: 0,
      limitedData: [],
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
    yearRange: {
      type: Array as PropType<number[]>,
      default: function () {
        return [2010, 2020];
      },
    },
  },
  computed: {
    ...mapState({
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
    this.limitedData = this.histData.filter(
      (el: HistDataItem) =>
        // typescript not parsing this correctly
        el.YEAR_BUILT <= this.$props.yearRange[1] &&
        el.YEAR_BUILT >= this.$props.yearRange[0]
    );
    d3.select(".barplot")
      .append("g")
      .append("circle")
      .attr("id", "tipcircle")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("fille", "rgb(255,255,255)")
      .attr("r", 5);
    this.initBarplot();
  },
  watch: {
    yearRange: function (newValue, oldValue) {
      this.limitedData = this.histData.filter(
        (el: HistDataItem) =>
          // typescript not parsing this correctly
          el.YEAR_BUILT <= newValue[1] && el.YEAR_BUILT >= newValue[0]
      );
      this.initBarplot();
    },
  },
  methods: {
    setSize() {
      const width = document.getElementById(`areaplotparent`)?.clientWidth;
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
      const self = this;
      const yMax =
        Math.max(
          ...this.limitedData.map((el): number => {
            return this.yearSums[el.YEAR_BUILT];
          })
        ) * 1.2;
      this.scales.x = d3
        .scaleLinear()
        .domain(
          d3.extent(this.limitedData, function (d) {
            return d.YEAR_BUILT;
          }) as [number, number]
        )
        .range([0, this.width]);
      this.scales.y = d3
        .scaleLinear()
        .domain([0, yMax])
        .range([this.height, 0]);
    },
    setAxes() {
      function tickFilter(d: any, i: number) {
        return i % 2 === 0;
      }
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
    initBars() {
      const self = this;
      const tipCircle = d3.select(".barplot").select("#tipcircle");
      // color palette = one color per subgroup
      const colorRange = d3.range(0, self.subgroups.length + 1).map((el) => {
        return d3.interpolateTurbo(el / self.subgroups.length);
      });

      //@ts-ignore
      const tip = d3tip().attr("class", "d3-tip").attr("z-index", 10000);
      d3.select(".barplot").select(".tooltip").call(tip);

      const color = d3
        .scaleOrdinal(d3.schemeRdYlBu)
        .domain(self.subgroups)
        //@ts-ignore
        .range(colorRange as string[]);
      //stack the data? --> stack per subgroup
      const stackedData = d3.stack<HistDataItem>().keys(self.subgroups)(
        this.limitedData
      );
      const t = d3.transition().duration(750).ease(d3.easeLinear) as any;
      const xScale = self.scales.x;
      const yScale = self.scales.y;

      function mouseAction(event: any, d: unknown) {
        if (xScale && yScale) {
          const data = d as d3.Series<HistDataItem, string>;
          const mouse = d3.pointer(event);
          const ind = d3.bisectLeft(
            data.map((el) => el.data.YEAR_BUILT),
            xScale.invert(mouse[0])
          );
          const x0 = xScale.invert(mouse[0]);
          const d0 = data[ind - 1];
          const d1 = data[ind];
          const point =
            x0 - d0.data.YEAR_BUILT > d1.data.YEAR_BUILT - x0 ? d1 : d0;
          //@ts-ignore
          const parentNode = d3.select(this).node().parentNode;
          const year = point.data.YEAR_BUILT;
          const target = tipCircle
            .attr("cx", xScale(year) + self.margins.left)
            .attr("cy", yScale(point[1]) + self.margins.top)
            .node();
          tip.html(
            "<span>" +
              `Year: ${year}<br>` +
              `${data.key}: ${point[1] - point[0]}<br>` +
              `Total: ${self.yearSums[year]}` +
              "</span>"
          );
          tip.show(d, target);
        }
      }

      if (xScale && yScale) {
        // // Remove elements
        const area = d3
          .area<d3.SeriesPoint<HistDataItem>>()
          .x(function (d) {
            return xScale(d.data.YEAR_BUILT);
          })
          .y0(function (d) {
            return yScale(d[0]);
          })
          //@ts-ignore
          .y1(function (d) {
            return yScale(d[1]);
          });

        const zeroArea = d3
          .area<d3.SeriesPoint<HistDataItem>>()
          .x(function (d) {
            return 0;
          })
          .y0(function (d) {
            return self.height;
          })
          //@ts-ignore
          .y1(function (d) {
            return self.height;
          });

        const areas = d3.select(".stacks").selectAll("path").data(stackedData);
        areas
          .exit()
          .transition(t)
          //@ts-ignore
          .attr("d", zeroArea)
          .remove();

        areas
          .enter()
          .append("path")
          //@ts-ignore
          .style("fill", function (d: d3.Series<HistDataItem>) {
            return color(d.key);
          })
          //@ts-ignore
          .attr("d", zeroArea)
          // .on("mouseenter", mouseAction)
          .on("mousemove", mouseAction)
          .on("mouseout", tip.hide)
          .transition(t)
          //@ts-ignore
          .attr("d", area);

        areas
          //@ts-ignore
          .attr("d", area)
          .on("mousemove", mouseAction);
      }
    },
    initBarplot() {
      this.setSize();
      this.setScales();
      this.setAxes();
      this.initBars();
    },
  },
});
</script>
