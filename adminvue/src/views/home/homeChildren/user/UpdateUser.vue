<template>
  <el-form :model="form" label-width="120px">
    <el-form-item label="用户名">
      <el-input v-model="form.name" disabled />
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

    <el-form-item>
      <el-button type="primary" @click="onSubmit">确认</el-button>
      <el-button @click="reset">重置</el-button>
    </el-form-item>
  </el-form>
  <!-- <el-text class="mx-1" type="success">当前页面得到的参数是{{ id }}</el-text> -->
</template>

<script lang="ts" setup>
import http from '@/utils/http'
import { reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
// do not use same name with ref
const route = useRoute()
const router = useRouter()
let user_id = 0
onMounted(() => {
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
  avatar_img: ''
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
  http.put('/admin/user', {
    user_id: user_id,
    password: form.password,
    gender: form.gender,
    integral: form.integral,
    phone: form.phone,
    email: form.email,
  }).then(() => {
    ElNotification({
      title: '成功',
      message: '用户信息更新成功',
      type: 'success',
    })
    router.push('/home/user/list')
  })
}
// 重置
const reset = () => {
  Object.assign(form, userData)
}
</script>
