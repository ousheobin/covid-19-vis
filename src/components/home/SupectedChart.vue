<template>
  <el-card>
    <p>现有疑似病例</p>
    <div id="home-supected-chart"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("home-supected-chart").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
        type: "csv"
      });

      let chart = new G2.Chart({
        container: "home-supected-chart",
        forceFit: true,
        height: window.innerWidth > 767 ? 300 : 200,
        padding: [10, 20, 60, 50]
      });

      chart.source(view, {
        date: {
          type: "time",
          mask: "MM-DD"
        },
        currentSupect: {
          type: "linear",
          alias: "现有疑似病例数"
        }
      });

      chart.axis("currentSupect", {
        label: {
          formatter: val => {
            val = Number(val) / 1000 + "k";
            return val;
          }
        }
      });

      chart
        .interval()
        .position("date*currentSupect")
        .color("#f9cd67")
        .opacity(0.6);

      chart.render();
    }
  },
  mounted() {
    this.renderChart();
  },
  watch: {
    csvData(newVal, oldVal) {
      this.renderChart();
    }
  }
};
</script>

<style>
</style>