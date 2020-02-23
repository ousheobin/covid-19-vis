<template>
  <el-card>
    <p>确诊病例合计</p>
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
          type: "fold",
          fields: ["currentConfrim", "currentSerious"],
          key: "type",
          value: "value"
        })
        .transform({
          type: "map",
          callback(row) {
            row.type =
              row.type === "currentConfrim" ? "当前确诊病例" : "重症病例";
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
        padding: [10, 20, 60, 30]
      });
      chart.source(view, {
        date: {
          type: "timeCat",
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

      chart
        .area()
        .position("date*value")
        .color("type", value => {
          if (value === "当前确诊病例") {
            return "#FF564D";
          } else {
            return "#850B03";
          }
        })
        .size(1)
        .shape("smooth");

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