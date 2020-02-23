<template>
  <el-card>
    <p>病例离汉后路径</p>
    <div id="cases-track" ref="chart" :style="style"></div>
  </el-card>
</template>

<script>
import echarts from "echarts";

export default {
  props: ["jsonData"],
  methods: {
    renderChart() {
      if (!this.$props.jsonData) {
        return;
      }
      this.$props.jsonData.nodes.forEach(node => {
        node.id = node.name;
        if(node.name == '武汉市'){
          node.value = NaN
          node.symbolSize = 60
          node.itemStyle = {
            "normal": { "color": "red" }
          }
        }else{
          node.itemStyle = {
            "normal": { "color": "#0a91a8" }
          }
          node.symbolSize = node.value * 2;
        }
        if(node.value > 10 || node.name == '武汉市'){
          node.label = {
            show: true
          }
        }
      });
      let echartObj = echarts.init(this.$refs.chart);
      echartObj.setOption({
        tooltip: {},
         animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            type: "graph",
            layout: "force",
            animation: true,
            focusNodeAdjacency: false,
            roam: true,
            draggable: false,
            data: this.$props.jsonData.nodes,
            force: {
              edgeLength: 40,
              repulsion: 60
            },
            lineStyle: {
              normal: {
                opacity: 0.7,
                width: 1
              }
            },
            edges: this.$props.jsonData.edges
          }
        ]
      });
    }
  },
  mounted() {
    this.renderChart();
  },
  watch: {
    jsonData(newVal, oldVal) {
      this.renderChart();
    }
  },
  data(){
    return{
      style:{
        height: window.innerWidth > 767 ? '500px' : '300px'
      }
    }
  }
};
</script>

<style>
</style>