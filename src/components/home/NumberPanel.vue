<template>
  <el-card class="numberPanel" :style="{borderLeftColor: this.$props.color}">
    <div class="name">{{name}}</div>
    <div class="number" :style="{color:this.$props.color}">{{numberFormatted}} 例</div>
  </el-card>
</template>

<script>
export default {
  props: ["name", "currentNumber", "color"],
  methods: {
    toThousands(num) {
      let numStr = "0";
      if (num instanceof Number) {
        numStr = num.toString();
      } else {
        numStr = num ? num : "-";
      }
      let result = "";

      while (numStr.length > 3) {
        result = "," + numStr.slice(-3) + result;
        numStr = numStr.slice(0, numStr.length - 3);
      }

      if (numStr) {
        result = numStr + result;
      }

      return result;
    }
  },
  watch: {
    currentNumber(newV) {
      this.$data.numberFormatted = this.toThousands(this.$props.currentNumber);
    }
  },
  mounted() {
    this.$data.numberFormatted = this.toThousands(this.$props.currentNumber);
  },
  data() {
    return {
      numberFormatted: ""
    };
  }
};
</script>

<style>
</style>