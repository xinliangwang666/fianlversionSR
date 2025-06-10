<template>
  <div class="head-box">
    <div class="my-bread">
      <el-breadcrumb separator="/" :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ name: 'dish' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'dish' }">菜品</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'notice' }">公告</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'admin' }">商家</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'user' }">用户</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'order' }">订单</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'flavor' }">口味</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'type' }">分类</el-breadcrumb-item>
        <el-breadcrumb></el-breadcrumb>
      </el-breadcrumb>
    </div>

    <div class="user_info" @click="logout">
      <div class="username">{{ loginUser.data.username }}</div>
      <div class="role">{{ loginUser.data.role }}</div>
      <button class="logout">退出登录</button>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { onMounted, reactive } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
const router = useRouter()

const store = useStore()
const loginUser = reactive({
  data: {
    username: '游客',
    role: '商家'
  }
})
onMounted(() => {
  // localStorage.get()
  const data = localStorage.getItem('loginUser')
  if (data) {
    const userInfo = JSON.parse(data)
    loginUser.data.role = userInfo.role
    loginUser.data.username = userInfo.username
  }
})
// 清除当前登录信息
const clearState = () => {

  store.commit('logout')
  router.push('/')
}
const logout = () => {
  ElMessageBox.confirm('你确定要退出吗?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      clearState()
      console.log('点击了退出');
    })
    .catch(() => {
      console.log('退出失败')
    })
}

// 1.引用图标
</script>
<style lang="scss" scoped>
.head-box {
  position: relative;
  width: 100%;
}

.my-bread {
  position: absolute;
  top: 20px;
  left: 0
}

.user_info {
  position: absolute;
  top: 0;
  right: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
  margin-right: 30px;

  button {
    padding: 12.5px 30px;
    border: 0;
    border-radius: 100px;
    background-color: #2ba8fb;
    color: #ffffff;
    font-weight: Bold;
    transition: all 0.5s;
    -webkit-transition: all 0.5s;
  }

  button:hover {
    background-color: #6fc5ff;
    box-shadow: 0 0 20px #6fc5ff50;
    transform: scale(1.1);
  }

  button:active {
    background-color: #3d94cf;
    transition: all 0.25s;
    -webkit-transition: all 0.25s;
    box-shadow: none;
    transform: scale(0.98);
  }
}

.user-info:hover {
  // cursor: pointer;
  background-color: #f2f2f2;
}

.username {
  font-size: 16px;
  color: #333;
  margin-right: 10px;
}

.role {
  font-size: 14px;
  color: #666;
  border-left: 1px solid #ccc;
  padding-left: 10px;
  margin-left: 10px;
}

.logout {
  cursor: pointer;
  margin-left: 10px;


}


.el-header {
  line-height: 60px; //设置图标垂直居中

  .el-icon {
    font-size: 20px; //设置图标大小
  }
}
</style>