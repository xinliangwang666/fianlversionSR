<template>
  <el-form label-position="right" label-width="100px" :model="formData" style="max-width: 460px">
    <el-form-item label="标题">
      <el-input v-model="formData.title" />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="formData.desc" />
    </el-form-item>
    <el-form-item label="图片">
      <input type="file" v-on:change="onFileChange" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Create</el-button>
      <el-button type="warning">Cancel</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import http from '@/utils/http'
import { useRouter } from 'vue-router'
const router = useRouter()
const onFileChange = (e: any) => {
  // console.log(e);
  formData.image = e.target.files[0]
}

const formData = reactive({
  title: '',
  desc: '',
  image: '',
})

const onSubmit = () => {
  let formDatas = new FormData()
  formDatas.append('title', formData.title)
  formDatas.append('desc', formData.desc)
  formDatas.append('image', formData.image)
  http.post('/admin/notice', formDatas, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(() => {
    ElMessage({
      message: '添加成功',
      type: 'success',
    })
    formData.title = ''
    formData.desc = ''
    formData.image = ''
    router.push('/home/notice/list')
  }).catch(() => {
    ElMessage({
      message: '添加失败',
      type: 'error',
    })
  })

}

</script>
