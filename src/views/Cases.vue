<template>
  <div class="cases">
    <p class="source">本页面数据来自<a href="https://github.com/839-Studio/Noval-Coronavirus-763-Cases">澎湃新闻美数课</a>团队整理自各地卫健委公开信息。</p>
    <el-row :gutter="20" style="margin-top:30px;">
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8" class="chart-cards">
        <Person2Person v-bind:csvData="csvData"/>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8" class="chart-cards">
        <InfectType v-bind:csvData="csvData"/>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8" class="chart-cards">
        <IsDeath v-bind:csvData="csvData"/>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <InfectedInterval v-bind:csvData="csvData"/>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <ToHospitalInterval v-bind:csvData="csvData"/>
      </el-col>
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="chart-cards">
        <AgeAndGender v-bind:csvData="csvData"/>
      </el-col>
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="chart-cards">
        <Track v-bind:jsonData="routeData"/>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import AgeAndGender from "@/components/cases/AgeAndGender";
import InfectedInterval from "@/components/cases/InfectedInterval";
import Person2Person from "@/components/cases/Person2Person";
import Track from "@/components/cases/Track";
import InfectType from "@/components/cases/InfectType";
import IsDeath from "@/components/cases/IsDeath";
import ToHospitalInterval from "@/components/cases/ToHospitalInterval";

import Axios from "axios";

export default {
  components:{
    AgeAndGender,
    InfectedInterval,
    Person2Person,
    Track,
    InfectType,
    IsDeath,
    ToHospitalInterval
  },
  methods: {
    checkLoading(){
      if(this.$data.csvReady && this.$data.routeReady){
        // this.$data.loading.close();
      }
    }
  },
  mounted() {
    // this.$data.loading = this.$loading({
    //       lock: true,
    //       text: '数据加载中，稍等下哈',
    //       background: 'rgba(226, 238, 247, 0.9)'
    // })
    Axios.get("./data/cases.data.csv", {
      headers: {
        "Cache-Control": "no-cache"
      }
    }).then(response => {
      this.$data.csvData = response.data;
      this.$data.csvReady = true;
      this.checkLoading();
    }).catch(()=>{
      this.$data.csvReady = true;
      this.checkLoading();
    });
    Axios.get("./data/cases.routes.json", {
      headers: {
        "Cache-Control": "no-cache"
      }
    }).then(response => {
      this.$data.routeData = response.data;
      this.$data.routeReady = true;
      this.checkLoading();
    }).catch(()=>{
      this.$data.routeReady = true;
      this.checkLoading();
    });
  },
  data() {
    return {
      csvData: "",
      routeData: null,
      csvReady: false,
      routeReady:false,
      loading: null
    };
  }
}
</script>