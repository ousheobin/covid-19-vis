<template>
  <el-card>
    <p>逗留、途径武汉后到出现症状时间间隔</p>
    <div id="cases-infected-interval"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      let isPCView = window.innerWidth > 767;
      document.getElementById("cases-infected-interval").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type: 'rename',
        map: {
          '症状间隔': 'infectInterval'
        }
      }).transform({
        type:'filter',
        callback: (row) =>{
          return row.infectInterval != '';
        }
      }).transform({
        type:'map',
        callback: (row) =>{
          row.infectInterval = Number(row.infectInterval)
          if(row.infectInterval < 14){
            row.intervalName = row.infectInterval+'天'
          }else{
            row.intervalName = '14天以上'
          }
          return row;
        }
      }).transform({
        type: 'sort-by',
        fields: [ 'infectInterval' ],
        order: 'ASC'
      }).transform({
        type:'pick',
        fields:['infectInterval','intervalName']
      }).transform({
        type: 'aggregate',
        fields: ['infectInterval'],
        operations: ['count'],
        as: ['infectIntervalCnt'],
        groupBy: ['intervalName']
      })
      let chart = new G2.Chart({
        container: "cases-infected-interval",
        forceFit: true,
        height: isPCView ? 300 : 200,
        padding: [20, 20, 60, 40]
      });
      chart.source(view,{
        infectInterval:{
          alias:'间隔时间',
          type:'linear',
          formatter: (value)=>{
            return Number(value) + '天'
          }
        },
        intervalName:{
          type:'cat',
          alias:'间隔时间',
        },
        infectIntervalCnt:{
          type:'linear',
          alias:'病例数'
        }
      })
      chart.axis('intervalName',{
        title:true
      })
      chart.axis('infectIntervalCnt',{
        label:{
          offset:20
        }
      })
      chart.tooltip({
        showTitle:false
      })
      chart.interval().position('intervalName*infectIntervalCnt').opacity(0.6)
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