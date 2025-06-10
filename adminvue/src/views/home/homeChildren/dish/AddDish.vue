<template>
  <!-- <el-radio-group v-model="labelPosition" label="label position">
    <el-radio-button label="left">Left</el-radio-button>
    <el-radio-button label="right">Right</el-radio-button>
    <el-radio-button label="top">Top</el-radio-button>
  </el-radio-group> -->
  <div style="margin: 20px" />
  <el-form label-position="right" label-width="100px" :model="form" style="max-width: 460px">
    <el-form-item label="菜品名称">
      <el-input v-model="form.dish_name" />
    </el-form-item>
    <el-form-item label="价格">
      <el-input v-model="form.price" type="number" />
    </el-form-item>
    <el-form-item label="菜品描述">
      <el-input v-model="form.dish_desc" type="textarea" />
    </el-form-item>
    <el-form-item label="选择类别">
      <el-select v-model="form.type_id" class="m-2" placeholder="Select" size="large">
        <el-option v-for="item in selectOptions" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </el-form-item>
    <el-form-item label="菜品图片">
      <input type="file" @change="changeImg" id="inputImg">
    </el-form-item>
    <div v-if="form.image !== ''"><img :src="imgs" alt="">
      <div class="cancelImg" @click="cancelImg">X</div>
    </div>
    <!-- <img src="" alt="preview" width="100px" height="100px"> -->
    <el-form-item>
      <el-button type="primary" @click="submitForm">
        添加
      </el-button>
      <el-button @click="resetForm">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue'
import http from '@/utils/http'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
interface SelectType {
  label: string
  value: number
}
const router = useRouter()
// 表单内容
const form = reactive({
  dish_name: '',
  dish_desc: '',
  price: 0,
  type_id: 1,
  image: '',
})
// 点击x取消推按
const cancelImg = () => {
  form.image = ''
  imgs.value = ''
}
// 下拉框内容选择
let selectOptions = ref<SelectType[]>([])
// 初始化请求下拉框可选项
onMounted(() => {
  http.get('/type').then((res: any) => {
    // console.log(res)
    selectOptions.value = res.typeList.map((item: any) => {
      const obj = {
        label: item.name,
        value: item.id
      }
      return obj
    })
  })
  // console.log('初始化加载')
})
let imgs = ref('')
const changeImg = (e: any) => {
  form.image = e.target.files[0]
  // imgs.value = e.target.value
  // console.log(e)

  // 图片预览
  let file = e.target.files[0]
  let reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function (result) {
    console.log('result')
    console.log(result)
    if (result.target?.result) {
      imgs.value = typeof (result.target.result) == 'string' ? result.target.result : ''
    }
  }


  // form.image = e.target.value
}
// 提交
const submitForm = () => {
  // console.log(form)
  let formData = new FormData()
  formData.append('dish_name', form.dish_name)
  formData.append('dish_desc', form.dish_desc)
  formData.append('dish_img', form.image)
  formData.append('dish_price', form.price.toString())
  formData.append('type_id', form.type_id.toString())
  http.post('/admin/dish', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then((res) => {
    console.log(res)
    ElMessage({
      message: '添加成功',
      type: 'success',
    })
    form.dish_name = ''
    form.dish_desc = ''
    form.image = ''
    form.price = 0
    form.type_id = 1


    router.push('/home/dish/list')
  }).catch(() => {
    ElMessage({
      message: '添加失败',
      type: 'error',
    })
  })

}
// 重置
const resetForm = () => {
  form.dish_name = '',
    form.dish_desc = '',
    form.price = 100,
    form.type_id = 1,
    form.image = ''
}



</script>
<style lang="scss" scoped>
.preImg {
  position: relative;
  width: 200px;
  height: 200px;
}
</style>
