<template>
  <!-- <el-button type="primary" class="addNotice" @click="changeTag">添加口味</el-button> -->
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
    <el-form-item label="菜品类型">
      <el-input v-model="formInline.DishType" placeholder="请输入类型名称" />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="formInline.desc" placeholder="请进行描述" />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">添加</el-button>
    </el-form-item>
  </el-form>
  <el-table :data="DishTypeList">
    <el-table-column prop="index" label="序号"></el-table-column>
    <el-table-column prop="name" label="标题"></el-table-column>
    <el-table-column prop="desc" label="描述"></el-table-column>
    <el-table-column label="操作">
      <template v-slot="{ row }">
        <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script lang="ts" setup>
import { ref, onMounted, reactive } from 'vue';
import { ElTable, ElTableColumn, ElButton, ElMessageBox, ElMessage } from 'element-plus';
import { DishTypes } from '@/utils/types'
import http from '@/utils/http'

// 添加按钮const formInline = reactive({


const formInline = reactive({
  DishType: '',
  desc: '',
})
// // 添加事件
const onSubmit = () => {
  console.log(formInline.DishType, formInline.desc);
  http.post('admin/type', {
    name: formInline.DishType,
    desc: formInline.desc
  }).then(res => {
    console.log(res);
    getDishType()
    formInline.DishType = ''
    formInline.desc = ''
  }).catch(() => {
    console.log('添加失败');
  })
  console.log('submit!')
}

// 获取数据
const getDishType = () => {
  http.get('admin/type').then(res => {
    const data = res.data.dishType.map((item: any, index: number) => {
      item['index'] = index + 1
      return item
    })
    DishTypeList.value = data
  }).catch(() => {
    console.log('请求发送失败');
  })

}
onMounted(() => {
  getDishType()
})


let DishTypeList = ref<DishTypes[]>([
  {
    id: 1,
    name: '炒菜',
    desc: 'fdsfsfsfdf'
  },
  {
    id: 2,
    name: '冒菜',
    desc: 'fdsfsfsfdf'
  }
])
// // 删除按钮
const handleDelete = (id: number) => {
  const name = DishTypeList.value.filter(item => item.id === id)[0].name
  ElMessageBox.confirm(
    `确定要删除${name}吗`,
    'Warning',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      const res = await http.delete('/admin/type', {
        data: {
          id: id
        }
      })
      console.log(res);
      ElMessage({
        type: 'success',
        message: `${name} 删除成功`,
      })
      getDishType()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      })
    })
};


</script>
<style lang="scss" scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>