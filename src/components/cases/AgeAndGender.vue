<template>
  <el-card>
    <p>病例年龄与性别分布</p>
    <div id="cases-bed-usage-chart"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      document.getElementById("cases-bed-usage-chart").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type: 'rename',
        map: {
          '年龄': 'age',
          '性别': 'gender'
        }
      }).transform({
        type:'filter',
        callback: (row)=>{
          return row.gender != '不明' && row.age != '不明'
        }
      }).transform({
        type:'pick',
        fields:['age','gender']
      }).transform({
        type:'map',
        callback: (row)=>{
          if(row.age < 10){
            row.ageName = '10岁以下'
          }else if(row.age > 70){
            row.ageName = '70岁以上'
          }else{
            let low = Math.floor(row.age / 5) * 5
            let high = low + 4
            row.ageName = low + '-' + high + '岁'
          }
          row.age = Number(row.age)
          return row
        }
      }).transform({
        type: 'aggregate',
        fields: ['ageName','gender'],
        operations: ['count'],
        as: ['cnt'],
        groupBy: ['ageName','gender']
      }).transform({
        type: 'sort-by',
        fields: [ 'age' ],
        order: 'ASC'
      })
      let chart = new G2.Chart({
        container: "cases-bed-usage-chart",
        forceFit: true,
        height: window.innerWidth > 767 ? 500 : 400,
        padding: window.innerWidth > 767 ? [20, 20, 60, 60] :  [20, 0, 60, 0]
      });
      chart.source(view,{
        age:{
          type:'linear',
          alias:'年龄'
        },
        gender:{
          type:'cat',
          alias:'性别'
        },
        cnt:{
          type:'linear',
          alias:'病例数'
        }
      });
      chart.facet('mirror',{
        fields:['gender'],
        transpose: true,
        padding: [ 0, 40, 0, 30 ],
        //[ '#1890ff', '#f04864' ]
        eachView(view) {
          view.interval()
          .position('ageName*cnt')
          .color('gender',(value)=>{
            if(value == '男'){
              return '#1890ff';
            }else{
              return '#f04864'
            }
          });
        }
      })
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