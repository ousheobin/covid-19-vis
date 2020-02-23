<template>
  <el-menu
    :default-active="activeIndex"
    class="pc-menu"
    mode="horizontal"
    background="#e2eef7"
    @select="handleSelect"
  >
    <el-menu-item 
      v-for="item in this.$data.menuList" 
      v-bind:key="item.index" 
      :index="item.index">{{item.name}}</el-menu-item>
  </el-menu>
</template>

<script>
import menu from './menuList'
export default {
  methods:{
    handleSelect(name){
      if(name != this.$route.name){
        this.$router.push({
          name: name
        })
      }
    }
  },
  mounted(){
    let name = this.$route.name;
    let menuList = menu.list;
    for(let i = 0 ; i < menuList.length ; i ++ ){
      if(menuList[i].index == name){
        this.$data.activeIndex = menuList[i].index;
        break;
      }
    }
  },
  data(){
    return {
      menuList: menu.list,
      activeIndex: null
    }
  }
};
</script>

<style>
</style>