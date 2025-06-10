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
    <el-form-item label="已定次数">
      <el-input v-model="form.order_count" type="number" />
    </el-form-item>
    <el-form-item label="选择类别">
      <el-select v-model="form.type_id" class="m-2" placeholder="Select" size="large">
        <el-option v-for="item in selectOptions" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </el-form-item>
    <el-form-item label="菜品图片">
      <input type="file" @change="changeImg" id="inputImg">
    </el-form-item>
    <div v-if="imgs" style="margin-left:50px;" class="preImg">
      <img :src="imgs" alt="" width="200" height="200">
      <div class="cancelImg" @click="cancelImg">X</div>
    </div>
    <el-form-item>
      <el-button type="primary" @click="submitForm">
        更改
      </el-button>
      <el-button @click="resetForm">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue'
import http from '@/utils/http'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
interface SelectType {
  label: string
  value: number
}
const route = useRoute()
const router = useRouter()
let id = route.params.id
// 表单内容
const form = reactive({
  dish_name: '',
  dish_desc: '',
  price: 0,
  type_id: 1,
  image: '',
  order_count: 0
})
// 下拉框内容选择
let selectOptions = ref<SelectType[]>([])
// 预览图的url
let imgs = ref('')
// let formImg = ''
// 初始化请求下拉框可选项
onMounted(() => {
  DishInfo(id)
  getType()
})
const DishInfo = (id: any) => {
  http.get(`/admin/dish?id=${id}`).then((res: any) => {

    form.dish_name = res.DishInfo.name
    form.dish_desc = res.DishInfo.desc
    form.price = res.DishInfo.price
    form.image = res.DishInfo.cover
    imgs.value = res.DishInfo.cover
    form.type_id = res.DishInfo.type
    form.order_count = res.DishInfo.order_count
    // formImg = res.DishInfo.cover
    // console.log(res)
    // Object.assign(form, res.DishInfo)
  })
}
// 获取菜品分类
const getType = () => {
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
}
// 选择图片
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
// 点击x取消图片
const cancelImg = () => {
  form.image = ''
  imgs.value = ''
}
// 提交更改
const submitForm = () => {
  // console.log(form)
  let formData = new FormData()
  formData.append('id', id.toString())
  formData.append('dish_name', form.dish_name)
  formData.append('dish_desc', form.dish_desc)
  formData.append('order_count', form.order_count.toString())
  formData.append('dish_price', form.price.toString())
  formData.append('type_id', form.type_id.toString())
  // 判断图片是否替换过
  if (form.image != imgs.value) {
    console.log('当前图片更换了');
    formData.append('dish_img', form.image)
  }

  http.post('/admin/upDish', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then((res) => {
    console.log(res)
    ElMessage({
      message: '修改成功',
      type: 'success',
    })
    form.dish_name = ''
    form.dish_desc = ''
    form.image = ''
    form.price = 0
    form.order_count = 0
    form.type_id = 1
    imgs.value = ''


    router.push('/home/dish/list')
  }).catch(() => {
    ElMessage({
      message: '修改失败失败',
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
    form.order_count = 0,
    form.image = ''
}



</script>
<style lang="scss" >
.preImg {
  position: relative;
  width: 200px;
  height: 200px;
}

.cancelImg {
  position: absolute;
  // content: 'x';
  // display: block;
  width: 20px;
  height: 20px;
  text-align: center;
  line-height: 20px;
  right: -20px;
  top: -20px;
  border-radius: 50%;
  border: 1px solid #000;

}
</style>
