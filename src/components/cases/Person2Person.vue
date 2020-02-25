<template>
  <el-card>
    <p>是否存在人传人（疑似）</p>
    <div id="cases-person-infect"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("cases-person-infect").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type: 'rename',
        map: {
          '人传人（疑似）': 'willPerson2Person'
        }
      }).transform({
        type: 'aggregate',
        fields: ['willPerson2Person'],
        operations: ['count'],
        as: ['willPerson2PersonCnt'],
        groupBy: ['willPerson2Person']
      }).transform({
        type:'pick',
        fields: ['willPerson2Person','willPerson2PersonCnt']
      }).transform({
        type:'map',
        callback:(row)=>{
          if( row.willPerson2Person == ''){
            row.willPerson2Person = '未知'
          }
          return row
        }
      }).transform({
        type: 'percent',
        field: 'willPerson2PersonCnt',
        dimension:'willPerson2Person',
        as: 'percent'
      });

      let chart = new G2.Chart({
        container: "cases-person-infect",
        forceFit: true,
        height: window.innerWidth > 767 ? 300 : 200,
        padding: [0, 0, 40, 0]
      });
      chart.source(view,{
        willPerson2PersonCnt:{
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
        willPerson2Person:{
          type:'cat',
          alias:'是否人传人'
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
      .color('willPerson2Person', [ '#F5AA84', '#DE826D', '#FA807B'])
      .tooltip('willPerson2Person*percent')
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