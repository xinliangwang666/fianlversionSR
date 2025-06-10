<template>
  <el-radio-group v-model="isCollapse" style="max-height: 1000px;">
    <el-radio-button :label="true">《</el-radio-button>

    <el-radio-button :label="false">》</el-radio-button>
  </el-radio-group>
  <el-menu active-text-color="#ffd04b" background-color="#545c64" :default-active="activeMenu"
    class="el-menu-vertical-demo" text-color="#fff" @open="handleOpen" @close="handleClose" :collapse="isCollapse" router
    :unique-opened="true">
    <el-sub-menu index="/home/notice">
      <template #title>
        <el-icon>
          <Tickets />
        </el-icon>
        <span>公告管理</span>
      </template>
      <el-menu-item-group>
        <el-menu-item index="/home/notice/list">
          <el-icon>
            <Dish />
          </el-icon>
          <span>公告列表</span>
        </el-menu-item>
        <el-menu-item index="/home/notice/add">
          <el-icon>
            <Dish />
          </el-icon>
          <span>添加公告</span>
        </el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>




    <el-sub-menu index="/home/admin/list" v-if="role != '商家'">
      <template #title>
        <el-icon>
          <UserFilled />
        </el-icon>
        <span>商家管理</span>
      </template>
      <el-menu-item-group>
        <el-menu-item-group>
          <el-menu-item index="/home/admin/list">
            <el-icon>
              <User />
            </el-icon>
            <span>商家列表</span>
          </el-menu-item>

        </el-menu-item-group>
        <el-menu-item-group>
          <el-menu-item index="/home/admin/add">
            <el-icon>
              <EditPen />
            </el-icon>
            <span>添加商家</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-menu-item-group>

    </el-sub-menu>
    <el-sub-menu index="/home/dish">
      <template #title>
        <el-icon>
          <Food />
        </el-icon>
        <span>菜品管理</span>
      </template>


      <el-menu-item-group>
        <el-menu-item-group>
          <el-menu-item index="/home/dish/list" :default-active="true">
            <el-icon>
              <Iphone />
            </el-icon>
            <span>菜品列表</span>
          </el-menu-item>

        </el-menu-item-group>
        <el-menu-item-group>
          <el-menu-item index="/home/dish/add">
            <el-icon>
              <Dish />
            </el-icon>
            <span>添加菜品</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-menu-item-group>

    </el-sub-menu>
    <el-menu-item index="/home/user/list">
      <el-icon>
        <User />
      </el-icon>
      <span>用户管理</span>
    </el-menu-item>
    <el-menu-item index="/home/order/list">
      <el-icon>
        <Tickets />
      </el-icon>
      <span>订单管理</span>
    </el-menu-item>

    <el-menu-item index="/home/flavor">
      <el-icon>
        <Bowl />
      </el-icon>
      <span>口味管理</span>
    </el-menu-item>
    <el-menu-item index="/home/type">
      <el-icon>
        <Dish />
      </el-icon>
      <span>菜品类别</span>
    </el-menu-item>



  </el-menu>
</template>
<script lang="ts" setup>
import {
  Dish,
  Food,
  UserFilled,
  // Menu as IconMenu,
  Iphone,
  EditPen,
  Tickets,
  User,
  Bowl,
} from '@element-plus/icons-vue'
import { ref } from 'vue';
import { useRoute } from 'vue-router'
// import { useStore } from 'vuex'
interface Users {
  username: string,
  password: string,
  role: string
}
const route = useRoute()
const activeMenu = route.path

// 当前用户身份
const userInfo = JSON.parse(localStorage.getItem('loginUser')!) as Users
const role = userInfo.role

// 左侧展开
const isCollapse = ref(false)
const handleOpen = (key: string, keyPath: string[]) => {
  localStorage.setItem('nav', key)
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>
<style lang="scss" scoped>
/* 自定义滚动条样式（兼容各种浏览器） */
/* 隐藏系统默认的滚动条 */
::-webkit-scrollbar {
  display: none;
}

/* 自定义滚动条样式 */
.el-menu__wrapper::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.el-menu__wrapper::-webkit-scrollbar-thumb {
  background-color: #c0c4cc;
  border-radius: 4px;
}

.el-menu__wrapper::-webkit-scrollbar-track {
  background-color: #f5f5f5;
  border-radius: 4px;
}
</style>