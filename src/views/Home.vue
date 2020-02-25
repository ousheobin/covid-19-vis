<template>
  <div class="home">
    <p class="source">全国数据来源于国家卫健委官方网站，数据截止至 {{currentData.date}} 晚上24时</p>
    <el-row :gutter="20" class="row">
      <el-col :xs="12" :sm="12" :md="8" :lg="8" :xl="8">
        <NumberPanel name="现有确诊" :currentNumber="currentData.currentConfrim" color="#c54242" />
      </el-col>
      <el-col :xs="12" :sm="12" :md="8" :lg="8" :xl="8">
        <NumberPanel name="现有疑似" :currentNumber="currentData.currentSupect" color="#e6af2f" />
      </el-col>
      <el-col :xs="12" :sm="12" :md="8" :lg="8" :xl="8">
        <NumberPanel name="累计治愈" :currentNumber="currentData.totalCured" color="#169200" />
      </el-col>
      <el-col :xs="12" :sm="12" :md="8" :lg="8" :xl="8">
        <NumberPanel name="累计确诊" :currentNumber="currentData.totalConfirm" color="#860000" />
      </el-col>
      <el-col :xs="12" :sm="12" :md="8" :lg="8" :xl="8">
        <NumberPanel name="现有重症" :currentNumber="currentData.currentSerious" color="#5d2929" />
      </el-col>
      <el-col :xs="12" :sm="12" :md="8" :lg="8" :xl="8">
        <NumberPanel name="累计死亡" :currentNumber="currentData.totalDeath" color="#636363" />
      </el-col>
    </el-row>
    <p class="section-title">全国总体趋势</p>
    <p class="source">以下图表数据来源于国家卫健委与湖北省卫健委</p>
    <el-row :gutter="20" style="margin-top:30px;">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <ConfirmedAndSerChart v-bind:csvData="csvData" />
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <ConfirmedIncrChart v-bind:csvData="csvData" />
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <SupectedChart v-bind:csvData="csvData" />
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <CuredAndDeathRate v-bind:csvData="csvData" />
      </el-col>
    </el-row>
    <p class="section-title">国内各省趋势</p>
    <p class="source">
      各省趋势数据由
      <a href="https://github.com/BlankerL/DXY-COVID-19-Data">Isaac Lin</a> 采集自网络
    </p>
    <el-row :gutter="20" style="margin-top:30px; padding: 0px 10px;">
      <ByProvince v-bind:csvData="timeseriesCsv" />
    </el-row>
    <p class="section-title">相关分析</p>
    <p class="source">疫情数据来源于澎湃新闻数美课（截止至 {{thePaperData}}），宏观数据来源于国家统计局（截止至 {{theOverallData}} 年末）</p>
    <el-row :gutter="20" style="margin-top:30px;">
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="chart-cards">
        <PopulationChart v-bind:csvData="corrCsv" />
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <BedUsage2Cured v-bind:csvData="corrCsv" />
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <MedicalPerson2Cured v-bind:csvData="corrCsv" />
      </el-col>
    </el-row>
    <p class="section-title" v-if="jsonReady && timeReady">社会关注度</p>
    <p class="source" v-if="jsonReady && timeReady">以下数据基于对新浪微博指数和百度指数相关关键词时序数据进行计算获得。(截止至{{timeData.time}})</p>
    <el-row :gutter="20" style="margin-top:30px;" v-if="jsonReady && timeReady">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <WHFocus v-bind:jsonData="focus" />
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" class="chart-cards">
        <MaskFocus v-bind:jsonData="mask" />
      </el-col>
    </el-row>
    <p class="section-title" v-if="jsonReady && timeReady">谣言喜欢用什么词</p>
    <p class="source" v-if="jsonReady && timeReady">基于丁香园辟谣信息</p>
    <el-row :gutter="20" style="margin-top:30px;" v-if="jsonReady && timeReady">
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="chart-cards">
        <WordCloud v-bind:jsonData="wordCloud" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import NumberPanel from "@/components/home/NumberPanel";
import ConfirmedIncrChart from "@/components/home/ConfirmedIncrChart";
import ConfirmedAndSerChart from "@/components/home/ConfirmedAndSerChart";
import CuredAndDeathRate from "@/components/home/CuredAndDeathRate";
import SupectedChart from "@/components/home/SupectedChart";
import PopulationChart from "@/components/home/PopulationChart";
import BedUsage2Cured from "@/components/home/BedUsage2Cured";
import MedicalPerson2Cured from "@/components/home/MedicalPerson2Cured";
import ByProvince from "@/components/home/ByProvince";

import MaskFocus from "@/components/focus/MaskFocus";
import WHFocus from "@/components/focus/WHFocus";
import WordCloud from "@/components/focus/WordCloud";

import { View } from "@antv/data-set";
import Axios from "axios";

export default {
  name: "Home",
  components: {
    NumberPanel,
    SupectedChart,
    ConfirmedIncrChart,
    ConfirmedAndSerChart,
    CuredAndDeathRate,
    PopulationChart,
    BedUsage2Cured,
    MedicalPerson2Cured,
    ByProvince,
    WHFocus,
    MaskFocus,
    WordCloud
  },
  methods: {
    renderCurrentData() {
      let view = new View();
      view.source(this.$data.csvData, {
        type: "csv"
      });
      this.$data.currentData = view.rows[view.rows.length - 1];
    },
    checkLoadingFinish() {
      if (
        this.$data.csvReady &&
        this.$data.corrReady &&
        this.$data.timeseriesReady
      ) {
        let loading = this.$data.loading;
        if (loading) {
          loading.close();
        }
      }
    },
    loadData() {
      Axios.get("./data/nhc.data.csv", {
        headers: {
          "Cache-Control": "no-cache"
        }
      })
        .then(response => {
          this.$data.csvData = response.data;
          this.renderCurrentData();
          this.$data.csvReady = true;
          this.checkLoadingFinish();
        })
        .catch(() => {
          this.$data.csvReady = true;
          this.checkLoadingFinish();
        });

      Axios.get("./data/overall.stat.csv", {
        headers: {
          "Cache-Control": "no-cache"
        }
      })
        .then(response => {
          this.$data.corrCsv = response.data;
          this.$data.corrReady = true;
          this.checkLoadingFinish();
        })
        .catch(() => {
          this.$data.corrReady = true;
          this.checkLoadingFinish();
        });

      Axios.get("./data/timeseries.data.csv", {
        headers: {
          "Cache-Control": "no-cache"
        }
      })
        .then(response => {
          this.$data.timeseriesCsv = response.data;
          this.$data.timeseriesReady = true;
          this.checkLoadingFinish();
        })
        .catch(() => {
          this.$data.timeseriesReady = true;
          this.checkLoadingFinish();
        });

      Axios.get("./data/overall.stat.date.json", {
        headers: {
          "Cache-Control": "no-cache"
        }
      }).then(response => {
        this.$data.thePaperData = response.data.thePaperData;
        this.$data.theOverallData = response.data.theOverallData;
      });

      Axios.get("./data/media.json", {
        headers: {
          "Cache-Control": "no-cache"
        }
      })
        .then(response => {
          this.$data.focus = response.data.focus;
          this.$data.wordCloud = response.data.wordCloud;
          this.$data.mask = response.data.mask;
          this.$data.newsChannel = response.data.newsChannel;
          this.$data.jsonReady = true;
        })
        .catch(() => {
          this.$data.jsonReady = true;
        });
      Axios.get("./media.updateTime.json", {
        headers: {
          "Cache-Control": "no-cache"
        }
      })
        .then(response => {
          this.$data.timeData = response.data;
          this.$data.timeReady = true;
        })
        .catch(() => {
          this.$data.timeReady = true;
        });
    }
  },
  mounted() {
    this.$data.loading = this.$loading({
      lock: true,
      text: "数据加载中，稍等下哈",
      background: "rgba(226, 238, 247, 0.9)"
    });
    this.loadData();
  },

  data() {
    return {
      csvData: "",
      csvReady: false,

      corrCsv: "",
      corrReady: false,

      timeseriesCsv: "",
      timeseriesReady: false,

      currentData: {},
      loading: null,

      thePaperData: "",
      theOverallData: "",

      focus: null,
      wordCloud: null,
      mask: null,
      newsChannel: null,

      timeData: null,

      jsonReady: false,
      timeReady:false,

    };
  }
};
</script>
