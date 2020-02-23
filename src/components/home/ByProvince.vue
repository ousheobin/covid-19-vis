<template>
  <el-card>
    <div id="home-by-province"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from "@antv/g2";

import Axios from "axios";

export default {
  props: ["csvData"],
  methods: {
    renderChart() {
      let isPCView = (window.innerWidth > 767);
      document.getElementById("home-by-province").innerHTML = "";
      let view = new View();
      view.source(this.$props.csvData, {
          type: "csv"
      }).transform({
        type:'filter',
        callback(row){
          return row.provinceName != '澳门'
        }
      }).transform({
        type:'map',
        callback(row){
          row['currentConfirmed'] = Number(row['province_confirmedCount']) - Number(row['province_curedCount']) - Number(row['province_deadCount'])
          return row
        }
      }).transform({
        type:'fold',
        fields: [ 'currentConfirmed', 'province_curedCount','province_deadCount' ],
        key:'type',
        value: 'value',
        retains: [ 'provinceName','updateTime' ]
      }).transform({
        type:'map',
        callback(row){
          let type = row.type;
          if(type == 'currentConfirmed'){
            row.type = '现有确诊'
          }else if(type == 'province_curedCount'){
            row.type = '治愈出院'
          }else{
            row.type = '死亡'
          } 
          return row
        }
      })
      console.log(view)
      let chart = new G2.Chart({
        container: "home-by-province",
        forceFit: true,
        height: isPCView ? 600 : 450,
        padding: [20, 0, 40, 20]
      });

      chart.source(view,{
        provinceName:{
          type: "cat",
          alias: "省、市、自治区"
        },
        type:{
          type: "cat",
          alias: "分类",
        },
        value:{
          type: "linear",
          alias: "值",
        },
        updateTime:{
          type: "timeCat",
          alias: '时间',
        }
      })
      chart.axis(false)
      chart.facet('list', {
        fields:['provinceName'],
        cols: isPCView ? 8: 4,
        padding: isPCView ? 20 : 5,
        eachView(view) {
        view.line()
          .position('updateTime*value')
          .color('type', value => {
              if (value == "现有确诊") {
                return "#FF564D";
              } else if (value == '死亡'){
                return "#969696";
              } else {
                return "#15B342"
              }
          })
          .shape('smooth')
          .opacity(0.3)
          .size(3);
        },
        colTitle: {
          offsetY: isPCView ? -10 : -3,
          style:{
            textAlign:'center',
            fontSize: (isPCView)?12:10
          }
        }
      })
      chart.render();
    }
  },
  mounted() {
    this.renderChart()
  },
  data(){
    return {
    }
  },
  watch: {
    csvData(newVal, oldVal) {
      this.renderChart()
    }
  }
};
</script>

<style>
</style>