<template>
  <el-card>
    <p>出现症状到首次入院/就诊时间间隔</p>
    <div id="cases-to-hospital"></div>
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
      document.getElementById("cases-to-hospital").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type: 'rename',
        map: {
          '入院间隔': 'toHospitalInterval'
        }
      }).transform({
        type:'filter',
        callback: (row) =>{
          return row.toHospitalInterval != '';
        }
      }).transform({
        type:'map',
        callback: (row) =>{
          row.toHospitalInterval = Number(row.toHospitalInterval)
          if(row.toHospitalInterval < 2){
            row.intervalName = '1天内'
          }else if(row.toHospitalInterval <= 3){
            row.intervalName = '2-3天'
          }else if(row.toHospitalInterval <= 5){
            row.intervalName = '4-5天'
          }else if(row.toHospitalInterval <= 7){
            row.intervalName = '6-7天'
          }else if(row.toHospitalInterval <= 9){
            row.intervalName = '8-9天'
          }else{
            row.intervalName = '10天以上'
          }
          return row;
        }
      }).transform({
        type: 'sort-by',
        fields: [ 'toHospitalInterval' ],
        order: 'ASC'
      }).transform({
        type:'pick',
        fields:['toHospitalInterval','intervalName']
      }).transform({
        type: 'aggregate',
        fields: ['toHospitalInterval'],
        operations: ['count'],
        as: ['toHospitalIntervalCnt'],
        groupBy: ['intervalName']
      })
      let chart = new G2.Chart({
        container: "cases-to-hospital",
        forceFit: true,
        height: isPCView ? 300 : 200,
        padding: [10, 20, 60, 40]
      });
      chart.source(view,{
        toHospitalInterval:{
          alias:'在武汉逗留时间',
          type:'linear',
          formatter: (value)=>{
            return Number(value) + '天'
          }
        },
        intervalName:{
          type:'cat',
          alias:'间隔时间',
        },
        toHospitalIntervalCnt:{
          type:'linear',
          alias:'病例数'
        }
      })
      chart.axis('intervalName',{
        title:true,
      })
      chart.axis('toHospitalIntervalCnt',{
        label:{
          offset:20
        }
      })
      chart.tooltip({
        showTitle:false
      })
      chart.line().position('intervalName*toHospitalIntervalCnt').tooltip('intervalName*toHospitalIntervalCnt').shape('smooth')
      chart.interval().position('intervalName*toHospitalIntervalCnt').tooltip(false).opacity(0.6)
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