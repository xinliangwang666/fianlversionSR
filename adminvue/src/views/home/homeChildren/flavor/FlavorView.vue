<template>
  <!-- <el-button type="primary" class="addNotice" @click="changeTag">添加口味</el-button> -->
  <el-form :inline="true" :model="formInline" class="demo-form-inline" border>
    <el-form-item label="口味">
      <el-input v-model="formInline.flavor" placeholder="请输入口味名称" />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="formInline.desc" placeholder="请进行描述" />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit">添加</el-button>
    </el-form-item>
  </el-form>
  <el-table :data="flavorList">
    <el-table-column prop="index" label="序号"></el-table-column>
    <el-table-column prop="name" label="标题"></el-table-column>
    <el-table-column prop="desc" label="描述"></el-table-column>
    <!-- <el-table-column label="图片">
      <template v-slot="{ row }">
        <el-image style="width: 100px; height: 100px" :src="row.img_url" :preview-src-list="[row.img_url]"></el-image>
      </template>
    </el-table-column> -->
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
import { FlavorType } from '@/utils/types'
import http from '@/utils/http'

// 添加按钮const formInline = reactive({


const formInline = reactive({
  flavor: '',
  desc: '',
})
// 添加事件
const onSubmit = () => {
  console.log(formInline.flavor, formInline.desc);
  http.post('admin/flavor', {
    name: formInline.flavor,
    desc: formInline.desc
  }).then(res => {
    console.log(res);
    getFlavor()
    formInline.flavor = ''
    formInline.desc = ''
  }).catch(() => {
    console.log('添加失败');
  })
  console.log('submit!')
}

// 获取数据
const getFlavor = () => {
  http.get('admin/flavor').then(res => {
    const data = res.data.dishFlavor.map((item: any, index: number) => {
      item['index'] = index + 1
      return item
    })
    flavorList.value = data
    console.log(flavorList)
  }).catch(() => {
    console.log('请求发送失败');
  })

}
onMounted(() => {
  getFlavor()
})


let flavorList = ref<FlavorType[]>([])
// 删除按钮
const handleDelete = (id: number) => {
  const name = flavorList.value.filter(item => item.id === id)[0].name
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
      const res = await http.delete('/admin/flavor', {
        data: {
          id: id
        }
      })
      console.log(res);
      ElMessage({
        type: 'success',
        message: `${name} 删除成功`,
      })
      getFlavor()
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