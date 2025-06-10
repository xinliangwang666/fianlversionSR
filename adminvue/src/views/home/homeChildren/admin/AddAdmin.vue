<template>
  <el-form label-position="right" label-width="100px" :model="formData" style="max-width: 460px">
    <el-form-item label="账号">
      <el-input v-model="formData.account" />
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="formData.password" />
    </el-form-item>
    <el-form-item label="手机号">
      <el-input v-model="formData.phone" />
    </el-form-item>
    <el-form-item label="角色">
      <el-select v-model="formData.role" class="m-2" placeholder="Select" size="large">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">创建</el-button>
      <el-button type="warning" @click="reset">清空</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
// import { ElMessage } from 'element-plus'
import http from '@/utils/http'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
const router = useRouter()


const formData = reactive({
  account: '',
  password: '',
  role: 2,
  phone: ''
})
// const value = ref('')

const options = [
  {
    value: 2,
    label: '商家',
  },
  {
    value: 1,
    label: '管理员',
  },
]
const onSubmit = () => {
  const data = {
    account: formData.account,
    password: formData.password,
    phone: formData.phone,
    role: formData.role
  }
  http.post('/admin/adminInfo', data).then(res => {
    console.log(res)
    ElNotification({
      title: 'Success',
      message: `账户${data.account}创建成功!`,
      type: 'success'
    })
    // const router = useRouter()

    formData.account = ''
    formData.password = ''
    formData.phone = ''
    formData.role = 2
    router.push('/home/admin/list')
  }).catch(e => {
    console.log(e)
    ElNotification({
      title: 'Error',
      message: `权限不够,无法添加`,
      type: 'error'
    })
  })
  // console.log(data)
}
// 清空表单
const reset = () => {
  formData.account = ''
  formData.password = ''
  formData.role = 2
  formData.phone = ''
}
// const onSubmit = () => {
//   let formDatas = new FormData()
//   formDatas.append('title', formData.title)
//   formDatas.append('desc', formData.desc)
//   // formDatas.append('image', formData.image)
//   http.post('/admin/notice', formDatas, {
//     headers: {
//       'Content-Type': 'multipart/form-data'
//     }
//   }).then(() => {
//     ElMessage({
//       message: '添加成功',
//       type: 'success',
//     })
//     formData.title = ''
//     formData.desc = ''
//     formData.image = ''
//     router.push('/home/notice/list')
//   }).catch(() => {
//     ElMessage({
//       message: '添加失败',
//       type: 'error',
//     })
//   })

// }

</script>
