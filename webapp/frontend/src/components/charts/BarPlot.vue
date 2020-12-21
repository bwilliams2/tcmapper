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
      aspectRatio: 1.5,
      fullWidth: 0,
      width: 0,
      height: 0,
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
      limitedData: function (state) {
        const { yearRange } = this.$props;
        return (state as RootStateType).plotData.histData.filter(
          (el: HistDataItem) =>
            // typescript not parsing this correctly
            el.YEAR_BUILT <= yearRange[1] && el.YEAR_BUILT >= yearRange[0]
        );
      },
      subgroups: function (state) {
        return Object.keys(
          (state as RootStateType).plotData.histData[0]
        ).filter((el) => el !== "YEAR_BUILT");
      },
    }),
  },
  mounted() {
    this.initBarplot();
  },
  methods: {
    setSize() {
      const width = document.getElementById(`barplotparent`)?.clientWidth;
      const height = document.getElementById(`barplotparent`)?.clientHeight;
      if (typeof width !== "number") {
        throw "parentDiv undefined";
      }
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
          ...this.limitedData.map((el) =>
            Math.max(
              ...Object.entries(el)
                .filter((item) => item[0] !== "YEAR_BUILT")
                .map((el) => el[1])
            )
          )
        ) * 1.1;
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
      d3.select(".x-axis")
        //@ts-ignore
        .call(d3.axisBottom(this.scales.x).tickSizeOuter(0))
        .selectAll(".tick line")
        .attr("stroke", "#000")
        .attr("stroke-opacity", "0.1");

      d3.select(".y-axis")
        //@ts-ignore
        .call(d3.axisLeft(this.scales.y).ticks(5))
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
    },
    initBars() {
      const self = this;
      // color palette = one color per subgroup
      const colorRange = d3.range(0, self.subgroups.length + 1).map((el) => {
        return d3.interpolateTurbo(el / self.subgroups.length);
      });
      const color = d3
        .scaleOrdinal(d3.schemeSpectral)
        .domain(self.subgroups)
        //@ts-ignore
        .range(colorRange as string[]);
      //stack the data? --> stack per subgroup
      const stackedData = d3.stack().keys(self.subgroups)(this.limitedData);

      if (self.scales.x !== null && self.scales.y !== null) {
        d3.select(".container")
          .append("g")
          .selectAll("g")
          .data(stackedData)
          .enter()
          .append("g")
          .attr("fill", function (d): string {
            //@ts-ignore
            return color(d.key) as string;
          })
          .selectAll("rect")
          .data(function (d) {
            return d;
          })
          .enter()
          .append("rect")
          .attr("x", function (d): number {
            //@ts-ignore
            return self.scales.x(d.data.YEAR_BUILT);
          })
          .attr("y", function (d) {
            //@ts-ignore
            return self.scales.y(d[1]);
          })
          .attr("height", function (d) {
            //@ts-ignore
            return self.scales.y(d[0]) - self.scales.y(d[1]);
          })
          .attr("width", self.scales.x.bandwidth());
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
