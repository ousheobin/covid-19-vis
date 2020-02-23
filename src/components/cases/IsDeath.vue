<template>
  <el-card>
    <p>是否死亡</p>
    <div id="cases-death"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("cases-death").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type: 'rename',
        map: {
          '是否死亡': 'isDeath'
        }
      }).transform({
        type: 'aggregate',
        fields: ['isDeath'],
        operations: ['count'],
        as: ['isDeathCnt'],
        groupBy: ['isDeath']
      }).transform({
        type:'pick',
        fields: ['isDeath','isDeathCnt']
      }).transform({
        type:'map',
        callback:(row)=>{
          if( row.isDeath == ''){
            row.isDeath = '未知'
          }
          return row
        }
      }).transform({
        type: 'percent',
        field: 'isDeathCnt',
        dimension:'isDeath',
        as: 'percent'
      });

      let chart = new G2.Chart({
        container: "cases-death",
        forceFit: true,
        height: window.innerWidth > 767 ? 300 : 200,
        padding: [0, 0, 40, 0]
      });
      chart.source(view,{
        isDeathCnt:{
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
        isDeath:{
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
      .color('isDeath', [ '#8C9EAC', '#918383', '#E3E3CD' ])
      .tooltip('isDeath*percent')
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