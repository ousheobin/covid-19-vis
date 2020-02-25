<template>
  <el-card>
      <p>治愈率与死亡率趋势</p>
      <div id="home-cured-death-rate"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from '@antv/g2';

export default {
    props:['csvData'],
    methods:{
        renderChart(){
            document.getElementById('home-cured-death-rate').innerHTML = ''
            let view = new View();
            view.source(this.$props.csvData,{
                type:'csv'
            }).transform({
                type:'map',
                callback(row){
                    let totalDeath = Number(row.totalDeath);
                    let totalCured = Number(row.totalCured);
                    let totalConfirm = Number(row.totalConfirm);
                    row['deathRate'] = Math.round((totalDeath / totalConfirm) * 1000) / 10;
                    row['curedRate'] = Math.round((totalCured / totalConfirm) * 1000) / 10;
                    return row
                }
            }).transform({
                type: 'fold',
                fields: [ 'deathRate', 'curedRate' ],
                key: 'type',
                value: 'rate'
            }).transform({
                type:'map',
                callback(row){
                    row.type = (row.type === 'deathRate')?'死亡率':'治愈率'
                    return row
                }
            }).transform({
                type: 'pick',
                fields: [ 'date', 'rate' , 'type' ]
            });
            let max = 0;
            view.rows.forEach(row => {
                if( row.rate > max){
                    max = row.rate;
                }
            });
            let chart = new G2.Chart({
                container:'home-cured-death-rate',
                forceFit: true,
                height: (window.innerWidth > 767)?300:200,
                padding:[10,20,60,50]
            });
            
            chart.source(view,{
                date:{
                    type:'time',
                    mask:'MM-DD'
                },
                rate:{
                    max: (max * 1.2) > 100 ? 100 : max * 1.2,
                    formatter: val => {
                        val = val + '%';
                        return val;
                    },
                    tickCount:5
                },
                
            });

            chart.line()
            .position('date*rate')
            .color('type', (value) => {
                if (value === '死亡率') {
                    return '#969696';
                }else{
                    return '#15B342';
                } 
            })
            .size(2)
            .shape('smooth');
            
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