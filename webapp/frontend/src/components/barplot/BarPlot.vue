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
      <g class="bars"></g>

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
  yearSums: Record<string, number>;
  barGroup: any;
  scales: {
    x: d3.ScaleBand<string> | null;
    y: d3.ScaleLinear<number, number, never> | null;
  };
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
      yearSums: {},
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
    chartType: {
      type: String,
      default: "bar",
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
    }),
  },
  mounted() {
    this.limitedData = this.histData.filter(
      (el: HistDataItem) =>
        // typescript not parsing this correctly
        el.YEAR_BUILT <= this.$props.yearRange[1] &&
        el.YEAR_BUILT >= this.$props.yearRange[0]
    );
    this.setYearSums(this.histData);
    d3.select(".barplot")
      .append("g")
      .append("circle")
      .attr("id", "tipcircle")
      .attr("cx", 0)
      .attr("cy", 0)
      .attr("r", 0);
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
    histData: function (newValue) {
      this.setYearSums(newValue);
    },
  },
  methods: {
    setYearSums(newValue: HistDataItem[]) {
      newValue.forEach((el: HistDataItem) => {
        this.yearSums[el.YEAR_BUILT] = Object.entries(el)
          .filter((val) => val[0] !== "YEAR_BUILT")
          .map((val) => val[1])
          .reduce((a, b) => a + b, 0);
      });
    },
    setSize() {
      const width = document.getElementById(`barplotparent`)?.clientWidth;
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
        .scaleBand()
        .domain(
          d3
            .range(self.$props.yearRange[0], self.$props.yearRange[1] + 1)
            .map((el) => `${el}`)
        )
        .range([0, this.width])
        .padding(0.2);
      this.scales.y = d3
        .scaleLinear()
        .domain([0, yMax])
        .range([this.height, 0]);
    },
    setAxes() {
      function tickFilter(d: any, i: number) {
        return i % 2 === 0;
      }
      const xScale = this.scales.x;
      const yScale = this.scales.y;
      if (xScale && yScale) {
        const xDomain = xScale.domain();
        const xTicks =
          xDomain.length > 15 ? xDomain.filter(tickFilter) : xDomain;
        d3.select(".x-axis")
          //@ts-ignore
          .call(d3.axisBottom(xScale).tickSizeOuter(0).tickValues(xTicks))
          .selectAll(".tick line")
          .attr("stroke", "#000")
          .attr("stroke-opacity", "0.1");

        d3.select(".y-axis")
          //@ts-ignore
          .call(d3.axisLeft(this.scales.y).ticks(8))
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
        return d3.interpolateRdYlBu(el / self.subgroups.length);
      });

      //@ts-ignore
      const tip = d3tip().attr("class", "d3-tip").attr("z-index", 10000);
      d3.select(".barplot").call(tip);

      const color = d3
        .scaleOrdinal()
        .domain(self.subgroups)
        //@ts-ignore
        .range(colorRange as string[]);
      //stack the data? --> stack per subgroup
      const stackedData = d3.stack().keys(self.subgroups)(this.limitedData);
      const t = d3.transition().duration(750).ease(d3.easeLinear) as any;

      function mouseAction(event: any, d: any) {
        const mouse = d3.pointer(event);
        const target = tipCircle
          .attr("cx", mouse[0] + self.margins.left)
          .attr("cy", mouse[1] + self.margins.bottom - 40)
          .node();
        //@ts-ignore
        const parentNode = d3.select(this).node().parentNode;
        //@ts-ignore
        const key = d3.select(parentNode).datum().key;
        tip.html(
          "<span>" +
            `Year: ${d.data.YEAR_BUILT}<br>` +
            `${key}: ${d[1] - d[0]}<br>` +
            `Total: ${self.yearSums[d.data.YEAR_BUILT]}` +
            "</span>"
        );
        tip.show(d, target);
      }
      if (self.scales.x !== null && self.scales.y !== null) {
        // // Remove elements
        let parents = d3.select(".bars").selectAll(".stacks").data(stackedData);

        parents
          .exit()
          .selectAll(".stacks")
          .selectAll("rect")
          .transition(t)
          .attr("x", 0)
          .attr("y", this.height)
          .attr("width", 0)
          .attr("height", 0)
          .remove();

        parents.exit().transition(t).style("opacity", 0).remove();

        const parentsEnter = parents
          .enter()
          .append("g")
          .attr("class", "stacks")
          .attr("fill", function (d: any): string {
            //@ts-ignore
            return color(d.key) as string;
          });

        // parentsEnter
        //   .selectAll("rect")
        //   .data(function (d: any) {
        //     return d;
        //   })
        //   .enter()
        //   .append("rect")
        //   .attr("x", 0)
        //   .attr("y", this.height)
        //   .attr("width", 0)
        //   .attr("height", 0)
        //   .transition(t)
        //   .attr("x", function (d: any): number {
        //     //@ts-ignore
        //     return self.scales.x(d.data.YEAR_BUILT);
        //   })
        //   .attr("y", function (d: any) {
        //     //@ts-ignore
        //     return self.scales.y(d[1]);
        //   })
        //   .attr("height", function (d: any) {
        //     //@ts-ignore
        //     return self.scales.y(d[0]) - self.scales.y(d[1]);
        //   })
        //   .attr("width", self.scales.x.bandwidth());

        parents = parentsEnter.merge(parents as any) as any;

        // const children = parents.select(".stacks");
        const childRects = parents.selectAll("rect").data(function (d) {
          return d;
        });

        childRects
          .exit()
          .transition(t)
          .attr("x", 0)
          .attr("y", this.height)
          .attr("width", 0)
          .attr("height", 0)
          .remove();

        const childRectsEnter = childRects
          .enter()
          .append("rect")
          .attr("x", 0)
          .attr("y", this.height)
          .attr("width", 0)
          .attr("height", 0)
          .on("mouseenter", mouseAction)
          .on("mousemove", mouseAction)
          .on("mouseout", tip.hide)
          .transition(t)
          .attr("x", function (d: any): number {
            //@ts-ignore
            return self.scales.x(d.data.YEAR_BUILT);
          })
          .attr("y", function (d: any) {
            //@ts-ignore
            return self.scales.y(d[1]);
          })
          .attr("height", function (d: any) {
            //@ts-ignore
            return self.scales.y(d[0]) - self.scales.y(d[1]);
          })
          .attr("width", self.scales.x.bandwidth());

        childRects
          .transition(t)
          .attr("x", function (d: any): number {
            //@ts-ignore
            return self.scales.x(d.data.YEAR_BUILT);
          })
          .attr("y", function (d: any) {
            //@ts-ignore
            return self.scales.y(d[1]);
          })
          .attr("height", function (d: any) {
            //@ts-ignore
            return self.scales.y(d[0]) - self.scales.y(d[1]);
          })
          .attr("width", self.scales.x.bandwidth());

        // Add new bars
        // parents
        //   .enter()
        //   .append("g")
        //   .attr("fill", function (d: any): string {
        //     //@ts-ignore
        //     return color(d.key) as string;
        //   })
        //   .selectAll("rect")
        //   .data(function (d: any) {
        //     return d;
        //   })
        //   .enter()
        //   .append("rect")
        //   .attr("x", 0)
        //   .attr("y", this.height)
        //   .attr("width", 0)
        //   .attr("height", 0)
        //   .transition(t)
        //   .attr("x", function (d: any): number {
        //     //@ts-ignore
        //     return self.scales.x(d.data.YEAR_BUILT);
        //   })
        //   .attr("y", function (d: any) {
        //     //@ts-ignore
        //     return self.scales.y(d[1]);
        //   })
        //   .attr("height", function (d: any) {
        //     //@ts-ignore
        //     return self.scales.y(d[0]) - self.scales.y(d[1]);
        //   })
        //   .attr("width", self.scales.x.bandwidth());

        // Update curent bars
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
