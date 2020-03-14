<template>
  <el-card>
    <p>现有确诊病例与重症比例</p>
    <div id="home-confirmed-chart"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("home-confirmed-chart").innerHTML = "";
      let view = new View();
      view
        .source(this.$props.csvData, {
          type: "csv"
        })
        .transform({
          type: "map",
          callback(row) {
            row.normalConfirmed = Number(row.currentConfrim) - Number(row.currentSerious)
            row.currentSerious = Number(row.currentSerious)
            return row;
          }
        })
        .transform({
          type: "fold",
          fields: ["normalConfirmed", "currentSerious"],
          key: "type",
          value: "value"
        })
        .transform({
          type: "map",
          callback(row) {
            row.type = (row.type === "normalConfirmed") ? "一般确诊病例" : "重症病例";
            return row;
          }
        })
        .transform({
          type: "pick",
          fields: ["date", "value", "type"]
        });
      let chart = new G2.Chart({
        container: "home-confirmed-chart",
        forceFit: true,
        height: window.innerWidth > 767 ? 300 : 200,
        padding: [10, 20, 60, 50]
      });
      chart.source(view, {
        date: {
          type: "time",
          mask: "MM-DD"
        },
        value: {
          type: "linear",
          tickCount: 5
        }
      });

      chart.axis("value", {
        label: {
          formatter: val => {
            val = Number(val) / 1000 + "k";
            return val;
          }
        }
      });

      chart.intervalStack().position('date*value').color("type", value => {
          if (value === "一般确诊病例") {
            return "#ff877a";
          } else {
            return "#800f03";
          }
        }).opacity(0.6);

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