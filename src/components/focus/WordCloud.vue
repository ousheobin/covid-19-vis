<template>
  <el-card>
    <div id="focus-word-cloud"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";
function getTextAttrs(cfg) {
  return {
    ...cfg.style,

    fillOpacity: cfg.opacity,
    fontSize: cfg.origin._origin.size,
    rotate: cfg.origin._origin.rotate,
    text: cfg.origin._origin.text,
    textAlign: "center",
    fontFamily: cfg.origin._origin.font,
    fill: cfg.color,
    textBaseline: "Alphabetic"
  };
}
G2.Shape.registerShape("point", "cloud", {
  drawShape(cfg, container) {
    const attrs = getTextAttrs(cfg);
    return container.addShape("text", {
      attrs: {
        ...attrs,
        x: cfg.x,
        y: cfg.y
      }
    });
  }
});
export default {
  props: ["jsonData"],
  methods: {
    renderChart() {
      if (!this.$props.jsonData) {
        return;
      }
      document.getElementById("focus-word-cloud").innerHTML = "";
      let isPCView = window.innerWidth > 767;
      let view = new View();
      view.source(this.$props.jsonData);
      let range = view.range("cnt");
      let min = range[0];
      let max = range[1];
      view.transform({
        type: "tag-cloud",
        fields: ["keyword", "cnt"],
        size: (isPCView)?[600, 300]:[300, 300],
        font: "Microsoft Yahei",
        padding: 0,
        spiral: 'archimedean', 
        rotate() {
          return 0;
        },
        fontSize(d) {
          if (d.value) {
            if(isPCView){
              return ((d.value - min) / (max - min)) * (60 - 15) + 15;
            }else{
              return ((d.value - min) / (max - min)) * (20 - 10) + 10;
            }
            
          }
          return 0;
        }
      });
      let chart = new G2.Chart({
        container: "focus-word-cloud",
        forceFit: true,
        height: 300,
        padding: [10, 10, 10, 10]
      });
      chart.source(view, {
        x: { nice: false },
        y: { nice: false },
        keyword: {
          alias: "关键词"
        },
        value: {
          type: "linear",
          alias: "出现的谣言条数"
        }
      });
      chart.legend(false);
      chart.axis(false);
      chart.tooltip({
        showTitle: false
      });
      chart.coord().reflect();
      chart
        .point()
        .position("x*y")
        .color("value", "#F3C2BF-#B33D30")
        .shape("cloud")
        .tooltip("keyword*value");
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