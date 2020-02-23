<template>
  <el-card>
      <p>确诊病例增长趋势</p>
      <div id="home-confirmed-incr-chart"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from '@antv/g2';

export default {
    props:['csvData'],
    methods:{
        renderChart(){
            document.getElementById('home-confirmed-incr-chart').innerHTML = ''
            let view = new View();
            view.source(this.$props.csvData,{
                type:'csv'
            }).transform({
                type:'map',
                callback: (row) => {
                    row.nonHubeiConfirmedIncr = Number(row.confirmIncr) - Number(row.hubeiConfirmedIncr)
                    return row
                }
            }).transform({
                type: 'fold',
                fields: [ 'confirmIncr','hubeiConfirmedIncr', 'nonHubeiConfirmedIncr' ],
                key: 'type',
                value: 'value'
            }).transform({
                type:'map',
                callback(row){
                    if(row.type == 'confirmIncr'){
                        row.type = '全国'
                    }else if ( row.type == 'hubeiConfirmedIncr'){
                        row.type = '湖北地区'
                    }else{
                        row.type = '非湖北地区'
                    }
                    return row
                }
            }).transform({
                type: 'pick',
                fields: [ 'date', 'value' , 'type' ]
            });
            let currentConfrimMax = 0;
            view.rows.forEach((row)=>{
                if( Number(row.value) > currentConfrimMax ){
                    currentConfrimMax = row.value;
                }
            })
            let chart = new G2.Chart({
                container:'home-confirmed-incr-chart',
                forceFit: true,
                height: (window.innerWidth > 767)?300:200,
                padding:[30,30,60,40]
            });
            chart.source(view,{
                date:{
                    type:'timeCat',
                    mask:'MM-DD'
                },
                value:{
                    tickCount: 5,
                    type:'linear',
                    alias:'确诊病例数'
                },
            });

            chart.axis('value',{
                position:'left',
                label: {
                    autoRotate:false,
                    formatter(text){
                        let originNum =  Number(text);
                        if( originNum >= 1000 ){
                            let num = Number(text) / 1000;
                            return num + 'k'
                        }else{
                            return originNum
                        }
                    }
                }
            })
            
            chart.line().position('date*value').color('type', (value) => {
                if (value === '全国') {
                    return '#E82040';
                }else if (value === '湖北地区') {
                    return '#FA9835';
                }else{
                    return '#5BAFE3';
                } 
            }).size(2).shape('smooth');
            
            chart.render();
        }
    },
    mounted(){
        this.renderChart();
    },
    watch:{
        csvData(newVal,oldVal){
            this.renderChart();
        }
    }
}
</script>

<style>

</style>