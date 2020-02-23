<template>
  <el-dropdown class="mobile-menu"  @command="onCommand">
    <el-button type="primary" size="mini" plain>
        菜单
    </el-button>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item 
        v-for="item in this.$data.menuList" 
        v-bind:key="item.index"
        :command="item.index">{{item.name}}</el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
import menu from './menuList'

export default {

  methods:{
    onCommand(name){
      if(name != this.$route.name){
        this.$router.push({
          name: name
        })
      }
    }
  },
  mounted(){
    console.log(this.$route.name)
  },
  data(){
    return {
      menuList: menu.list,
      activeIndex: menu.list[0].url
    }
  }

};
</script>