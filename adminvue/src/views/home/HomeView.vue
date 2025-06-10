<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">
        <div class="logo">
          <h1>未来领鲜</h1>
        </div>
        <LeftMenu></LeftMenu>
      </el-aside>
      <el-container>
        <el-header>
          <TopMenu></TopMenu>
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style lang="scss" scoped>
.common-layout {
  .el-aside {
    background-color: rgb(84, 92, 100);
  }

  .el-header {
    background-color: rgb(225, 225, 224);
  }

  .el-main {
    background-color: #fff;
  }
}

.logo {
  width: 100%;
  height: 120px; /* 增加高度 */
  background: linear-gradient(45deg, #2a80b3, #1a4d6b); /* 渐变背景 */
  box-shadow: 0 0 20px rgba(26, 77, 107, 0.3); /* 投影效果 */
  display: flex; /* 弹性布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  position: relative; /* 定位基准 */
  overflow: hidden; /* 隐藏溢出 */

  h1 {
    margin: 0;
    font-size: 28px; /* 加大字体 */
    font-family: 'Courier New', monospace; /* 等宽字体 */
    color: #fff;
    text-transform: uppercase; /* 大写字母 */
    letter-spacing: 2px; /* 字母间距 */
    z-index: 1; /* 层级置顶 */
    
    /* 文字描边效果 */
    -webkit-text-stroke: 1px rgba(255, 255, 255, 0.1);
    text-shadow: 
      0 0 10px rgba(255, 255, 255, 0.3),
      0 0 20px rgba(255, 255, 255, 0.2),
      0 0 40px rgba(255, 255, 255, 0.1); /* 多层阴影 */
    
    /* 动态发光动画 */
    &:after {
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at center, rgba(255,255,255,0.3) 0%, transparent 70%);
      filter: blur(15px);
      opacity: 0;
      animation: glowAnimation 3s infinite; /* 应用动画 */
    }
  }
}

// 高度100%
.el-aside,
.el-container,
.common-layout,
#app,
body,
html {
  height: 100%;
}

/* 定义发光动画 */
@keyframes glowAnimation {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(1.2);
  }
}
</style>