<template>
  <div id="app">
    <el-config-provider :locale="locale">
      <router-view />
    </el-config-provider>
  </div>
</template>

<script lang="ts" setup>
import locale from "element-plus/lib/locale/lang/zh-cn"
</script>
<style lang="scss" >
@import '@/styles/style.scss';

html,
body,
#app {
  //设置页面100%高
  height: 100vh;
}

/* 隐藏系统默认的滚动条 */
::-webkit-scrollbar {
  width: 1px;

}
</style>
