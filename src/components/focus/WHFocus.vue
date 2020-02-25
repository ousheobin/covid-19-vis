<template>
  <el-card>
    <p>武汉肺炎搜索与微博讨论综合关注指数</p>
    <div id="focus-overall-index"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["jsonData"],
  methods: {
    renderChart() {
      if (!this.$props.jsonData) {
        return;
      }
      let isPCView = window.innerWidth > 767;
      document.getElementById("focus-overall-index").innerHTML = "";
      let view = new View();
      view.source(this.$props.jsonData);
      let chart = new G2.Chart({
        container: "focus-overall-index",
        forceFit: true,
        height: isPCView ? 300 : 200,
        padding: [10, 30, 60, 30]
      });

      chart.source(view, {
        date: {
          type: "time",
          mask: "YYYY-MM-DD"
        },
        focus: {
          alias: "综合关注度"
        }
      });

      chart
        .line()
        .position("date*focus")
        .size(2)
        .shape("smooth");
      if (isPCView) {
        chart.guide().dataMarker({
          position: ["2019-12-31", 9.33],
          content: "武汉市卫健委发布“不明原因肺炎”通报",
          lineLength: 30,
          autoAdjust: true
        });
        chart.guide().dataMarker({
          position: ["2020-01-20", 45.85],
          content: "钟南山明确表示新型冠状病毒“人传人”",
          lineLength: 10,
          autoAdjust: false,
          direction:'downward'
        });
      }

      chart.guide().dataMarker({
        position: ["2020-01-23", 94.168],
        content: "关闭离汉通道",
        lineLength: 30,
        autoAdjust: true
      });

      chart.render();
    }
  },
  mounted() {
    this.renderChart();
  },
  watch: {
    jsonData(newVal, oldVal) {
      this.renderChart();
    }
  }
};
</script>

<style>
</style>