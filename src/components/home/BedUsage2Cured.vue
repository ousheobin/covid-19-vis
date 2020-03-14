<template>
  <el-card>
    <p>医院床位利用率与治愈率的关系（湖北以外地区）</p>
    <div id="home-bed-usage-chart"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("home-bed-usage-chart").innerHTML = "";
      let view = new View();
      view
        .source(this.$props.csvData, {
          type: "csv"
        })
        .transform({
          type: "filter",
          callback: row => {
            if (row.province === "湖北" || row.province === '香港' || row.province === '澳门' || row.province === '台湾') {
              return false;
            }
            return true;
          }
        })
        .transform({
          type: "map",
          callback: row => {
            let totalCured = Number(row.cured);
            let totalConfirm = Number(row.confirmed);
            row["curedRate"] =
              Math.round((totalCured / totalConfirm) * 1000) / 10;
            return row;
          }
        });
      let chart = new G2.Chart({
        container: "home-bed-usage-chart",
        forceFit: true,
        height: window.innerWidth > 767 ? 300 : 200,
        padding: [10, 20, 60, 60]
      });
      chart.source(view, {
        province: {
          type: "cat",
          alias: "省、市、自治区"
        },
        curedRate: {
          type: "linear",
          alias: "治愈率",
          formatter: val => {
            val = val + "%";
            return val;
          }
        },
        confirmed: {
          type: "linear",
          alias: "确诊数"
        },
        bedUsageRate: {
          type: "linear",
          alias: "医院病床使用率",
          formatter: val => {
            val = val + "%";
            return val;
          }
        },
      });
      // chart.legend('confirmed', false);
      chart.axis("curedRate", {
        title: {
          offset: 50
        },
        label: {
          autoRotate: false
        }
      });
      chart.axis("bedUsageRate", {
        title: true,
        label: {
          autoRotate: false
        }
      });
      chart.tooltip({
        showTitle: false
      });
       chart.legend('curedRate', false);
      chart
        .point()
        .position("bedUsageRate*curedRate")
        .shape("circle")
        .tooltip("province*bedUsageRate*curedRate")
        .color("curedRate", '#5eaec1-#269e2a')
        .style("continent", {
          lineWidth: 1,
          strokeOpacity: 1,
          fillOpacity: 0.6,
          opacity: 0.8
        });
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