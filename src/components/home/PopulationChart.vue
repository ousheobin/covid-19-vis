<template>
  <el-card>
    <p>人口、运输与确诊数的关系（湖北以外地区）</p>
    <div id="home-population-transport-chart"></div>
    <p class="remark">备注：点的大小表示累计确诊的数量。</p>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("home-population-transport-chart").innerHTML = "";
      let isPCView = (window.innerWidth > 767);
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type:'filter',
        callback:(row)=>{
          if (row.province === "湖北" || row.province === '香港' || row.province === '澳门' || row.province === '台湾') {
              return false;
            }
          return true;
        }
      })
      let chart = new G2.Chart({
        container: "home-population-transport-chart",
        forceFit: true,
        height: isPCView ? 300 : 200,
        padding: [10, 20, 60, 80]
      });
      chart.source(view, {
        province: {
          type: "cat",
          alias: "省、市、自治区"
        },
        population: {
          type: "linear",
          alias: "年末常住人口(万人)"
        },
        transportTotal:{
          type: "linear",
          alias: "客运量(万人)"
        },
        confirmed: {
          type: "linear",
          alias: "确诊数"
        }
      });
    chart.legend('confirmed', false);
    chart.axis('population',{
      title: true,
      label:{
        autoRotate:false
      }
    });
    chart.axis('transportTotal',{
      title: {
        offset: 65
      },
      label:{
        autoRotate:false
      }
    });
    chart.tooltip({
      showTitle: false 
    });
    chart.point().position('population*transportTotal')
    .size('confirmed', isPCView ? [ 4, 30 ] : [4 , 10]).shape('circle')
    .tooltip('province*population*transportTotal*confirmed')
    .color('confirmed',(val)=>{
      if(val < 200){
          return '#5eb6c5'
        }else if( val < 600 ){
          return '#d49a83'
        }else{
          return '#710600'
      }
    })
    .style('continent', {
      lineWidth: 1,
      strokeOpacity: 1,
      fillOpacity: 0.5,
      opacity: 0.8,
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