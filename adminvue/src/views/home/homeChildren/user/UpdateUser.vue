<template>
  <el-form :model="form" label-width="120px">
    <el-form-item label="用户名">
      <el-input v-model="form.name" :disabled="userRole === '商家'" />
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="form.password" />
    </el-form-item>
    <el-form-item label="性别">
      <el-select v-model="form.gender" placeholder="请选择性别">
        <el-option label="男" :value="1" />
        <el-option label="女" :value="0" />
      </el-select>
    </el-form-item>
    <el-form-item label="积分">
      <el-input v-model="form.integral" />
    </el-form-item>
    <el-form-item label="电话">
      <el-input v-model="form.phone" />
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="form.email" />
    </el-form-item>
    <el-form-item label="收货地址" v-if="userRole === '管理员' || userRole === '超级管理员'">
      <el-input v-model="form.addr" type="textarea" :rows="3" placeholder="请输入收货地址" />
    </el-form-item>
    <el-form-item label="收货地址" v-else>
      <el-input v-model="form.addr" type="textarea" :rows="3" disabled />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">确认</el-button>
      <el-button @click="reset">重置</el-button>
    </el-form-item>
  </el-form>
  <!-- <el-text class="mx-1" type="success">当前页面得到的参数是{{ id }}</el-text> -->
</template>

<script lang="ts" setup>
import http from '@/utils/http'
import { reactive, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'

interface UpdateUserData {
  user_id: number;
  name: string;
  password: string;
  gender: number;
  integral: number;
  phone: string;
  email: string;
  addr?: string;
}

const route = useRoute()
const router = useRouter()
let user_id = 0

// 获取用户角色
const userRole = ref('')

onMounted(() => {
  // 获取用户信息
  const userInfo = JSON.parse(localStorage.getItem('loginUser') || '{}')
  userRole.value = userInfo.role || '商家'

  const params = route.params
  console.log(params, typeof (params), Object.keys(params));

  let id = params.id
  if (!Array.isArray(id)) {
    user_id = parseInt(id)
    getInfo(parseInt(id))
  }
})

let form = reactive({
  name: '',
  password: '',
  gender: 1,
  integral: 0,
  phone: '134545848',
  email: '',
  avatar_img: '',
  addr: ''
})

// 做缓存
let userData = {}

// 根据id获取用户信息
const getInfo = (id: number) => {
  http.get(`/admin/user?id=${id}`).then(res => {
    console.log(res);
    userData = res.data
    Object.assign(form, res.data)
  })
}

const onSubmit = () => {
  const updateData: UpdateUserData = {
    user_id: user_id,
    name: form.name,
    password: form.password,
    gender: form.gender,
    integral: form.integral,
    phone: form.phone,
    email: form.email,
  }

  // 管理员和超级管理员可以修改地址
  if (userRole.value === '管理员' || userRole.value === '超级管理员') {
    updateData.addr = form.addr
  }

  http.put('/admin/user', updateData).then(() => {
    ElNotification({
      title: '成功',
      message: '用户信息更新成功',
      type: 'success',
    })
    router.push('/home/user/list')
  }).catch(error => {
    console.error('更新失败:', error);
    ElNotification({
      title: '错误',
      message: error.response?.data?.msg || '更新失败',
      type: 'error',
    })
  })
}

// 重置
const reset = () => {
  Object.assign(form, userData)
}
</script>

<style>
.el-form {
  max-width: 600px;
  margin: 20px auto;
}
</style>
