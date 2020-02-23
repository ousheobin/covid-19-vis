<template>
  <el-card>
    <p>每10万人平均卫生人员数与治愈率的关系（湖北以外地区）</p>
    <div id="home-medical-person-chart"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("home-medical-person-chart").innerHTML = "";
      let view = new View();
      view
        .source(this.$props.csvData, {
          type: "csv"
        })
        .transform({
          type: "filter",
          callback: row => {
            if (row.province === "湖北" || row.province === "香港" || row.province === "澳门" || row.province === "台湾") {
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
            row["healthStaffPer10w"] = Math.round(
              Number(row.healthStaffPer10w)
            );
            row["curedRate"] =
              Math.round((totalCured / totalConfirm) * 1000) / 10;
            return row;
          }
        });
      let chart = new G2.Chart({
        container: "home-medical-person-chart",
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
        healthStaffPer10w: {
          type: "linear",
          alias: "每10万人平均卫生人员数"
        }
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
      chart.axis("healthStaffPer10w", {
        title: true,
        label: {
          autoRotate: false
        }
      });
      chart.tooltip({
        showTitle: false
      });
      chart.legend("curedRate", false);
      chart
        .point()
        .position("healthStaffPer10w*curedRate")
        .shape("circle")
        .tooltip("province*healthStaffPer10w*curedRate")
        .color("curedRate", val => {
          if (val > 60) {
            return "#269e2a";
          } else if (val > 30) {
            return "#5eaec1";
          } else {
            return "#c15e74";
          }
        })
        .style("continent", {
          lineWidth: 1,
          strokeOpacity: 1,
          fillOpacity: 0.5,
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