<template>
  <div id="app" class="app">
    <el-row :gutter="10">
      <el-col :xs="16" :sm="12" :md="12" :lg="12" :xl="12">
        <Banner />
      </el-col>
      <el-col :xs="8" :sm="12" :md="12" :lg="12" :xl="12" class="menu-bar" v-if="this.$data.ready">
        <MobileMenu v-if="isMobile"/>
        <PCMenu v-if="!isMobile"/>
      </el-col>
    </el-row>
    <router-view />
    <div class="footer">
      <p>武汉加油！</p>
      <p>Designed by <a href="https://github.com/ousheobin/" target="_blank">Steve OU</a> with ❤ in China</p>
    </div>
  </div>
</template>

<script>
import Banner from "@/components/header/Banner";
import MobileMenu from "@/components/header/MobileMenu";
import PCMenu from "@/components/header/PCMenu";

export default {
  components: {
    Banner,
    PCMenu,
    MobileMenu
  },
  methods: {
    checkMobile(){
      if(window.innerWidth > 767){
        this.$data.isMobile = false
      }else{
        this.$data.isMobile = true
      }
    }
  },
  mounted() {
    this.checkMobile();
    this.$data.ready = true;
    window.onresize = () => {
      this.checkMobile();
      return true;
    };
  },
  data() {
    return {
      isMobile: false
    };
  }
};
</script>