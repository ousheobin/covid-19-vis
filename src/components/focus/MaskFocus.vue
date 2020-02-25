<template>
  <el-card>
      <p>公众对口罩的关注指数</p>
      <div id="focus-mask"></div>
  </el-card>
</template>

<script>
import { View } from "@antv/data-set";
import G2 from '@antv/g2';

export default {
    props:['jsonData'],
    methods:{
        renderChart(){
            if(!this.$props.jsonData){
                return;
            }
            document.getElementById('focus-mask').innerHTML = ''
            let view = new View();
            view.source(this.$props.jsonData)

            let chart = new G2.Chart({
                container:'focus-mask',
                forceFit: true,
                height: (window.innerWidth > 767)?300:200,
                padding:[10,30,60,50]
            });
            
            chart.source(view,{
                date:{
                    type:'time',
                    mask:'YYYY-MM-DD',
                },
                focus:{
                    alias:'综合关注度',
                }
            });

            chart.guide().dataMarker({
                position: ["2020-01-20", 4.338],
                content: "钟南山在接受央视连线时明确表示新型冠状病毒“人传人”",
                lineLength: 10,
                autoAdjust: true,
            });

             chart.guide().dataMarker({
                position: ["2020-01-23", 19.848],
                content: "工信部:30多家企业已复产",
                lineLength: 30,
                autoAdjust: true,
            });

            chart.line()
            .position('date*focus')
            .size(2)
            .shape('smooth');
            
            chart.render();
        }
    },
    mounted(){
        this.renderChart();
    },
    watch:{
        jsonData(newVal,oldVal){
            this.renderChart();
        }
    }
}
</script>

<style>

</style>