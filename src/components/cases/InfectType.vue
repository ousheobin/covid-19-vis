<template>
  <el-card>
    <p>传播途径</p>
    <div id="cases-infect-type"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("cases-infect-type").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type: 'rename',
        map: {
          '类型（人传人）': 'infectType'
        }
      }).transform({
        type: 'aggregate',
        fields: ['infectType'],
        operations: ['count'],
        as: ['infectTypeCnt'],
        groupBy: ['infectType']
      }).transform({
        type:'pick',
        fields: ['infectType','infectTypeCnt']
      }).transform({
        type:'map',
        callback:(row)=>{
          if( row.infectType == ''){
            row.infectType = '未知'
          }
          return row
        }
      }).transform({
        type: 'percent',
        field: 'infectTypeCnt',
        dimension:'infectType',
        as: 'percent'
      });

      let chart = new G2.Chart({
        container: "cases-infect-type",
        forceFit: true,
        height: window.innerWidth > 767 ? 300 : 200,
        padding: [0, 0, 40, 0]
      });
      chart.source(view,{
        infectTypeCnt:{
          type:'linear',
          alias:'个案数'
        },
        percent:{
          type:'linear',
          alias:'比例',
          formatter: (value) =>{
             return Math.round(value * 10000) / 100  + '%';
          }
        },
        infectType:{
          type:'cat',
          alias:'人传人类型'
        },
      });
      chart.tooltip({
        showTitle: false 
      });
      chart.coord('theta', {
        radius: 0.75,
        innerRadius: 0.6
      });
      chart.intervalStack()
      .position('percent')
      .color('infectType', [ '#6B9DF8', '#5DAAD9', '#73E1F0', '#5DD9C5','#6BF8BA' ])
      .tooltip('infectType*percent')
      .opacity(1)
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