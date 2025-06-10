<template>
  <div class="dish-container">

    <el-table :data="dishList" style="width: 90%;" border>
      <el-table-column prop="index" label="序号" width="100" align="center" header-align="center"></el-table-column>
      <el-table-column prop="name" label="菜名" width="200" align="center" header-align="center"></el-table-column>
      <el-table-column prop="price" label="价格" width="100" align="center" header-align="center"></el-table-column>
      <el-table-column prop="order_count" label="销量" width="100" align="center" header-align="center"></el-table-column>
      <!-- <el-table-column prop="cover" label="封面"></el-table-column> -->
      <el-table-column prop="desc" label="描述" align="center" header-align="center"></el-table-column>
      <el-table-column prop="type" label="分类" width="100"></el-table-column>
      <el-table-column label="图片" width="200" align="center" header-align="center">
        <template v-slot="{ row }">
          <el-image style="width: 100px; height: 100px" :src="row.cover" :preview-src-list="[row.cover]"></el-image>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" align="center" header-align="center">
        <template v-slot="{ row }">
          <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
          <el-button type="warning" size="small" @click="handleEdit(row.id)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="my-page">
      <el-pagination background v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
        :page-sizes="[5, 10, 15, 20, 25]" @current-change="handleCurrentChange" @size-change="handleSizeChange"
        layout="sizes, prev, pager, next" :hide-on-single-page="false" />
    </div>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { ElTable, ElTableColumn, ElImage, ElButton, ElMessage, ElMessageBox } from 'element-plus';
import http from '@/utils/http';
import { DishType } from '@/utils/types';
import { useRouter } from 'vue-router'
const dishList = ref<DishType[]>([])
const router = useRouter()

// 当前页数
const currentPage = ref(1)
// 菜品总数
const total = ref(200)
// 分页数据，也就是一页的数量
const pageSize = ref(10)
const handleSizeChange = (val: number) => {
  // console.log(`${val} items per page`)
  pageSize.value = val
  getDish()
}
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  getDish()
}




// 获取公告
const getDish = () => {
  console.log(currentPage.value, typeof (currentPage.value));
  console.log(pageSize.value, typeof (pageSize.value))
  http.get(`/admin/dish?page=${currentPage.value}&page_size=${pageSize.value}`).then(res => {
    // console.log(res)
    const data = res.data.dish_list.map((item: any, index: number) => {
      item['index'] = (currentPage.value - 1) * pageSize.value + index + 1
      // print(item['index'])
      item['price'] = item['price'] + '￥'
      return item
    })
    dishList.value = data
    // console.log(data)
    // currentPage.value = parseInt(data.page_num)
    total.value = parseInt(res.data.dish_count)
    pageSize.value = parseInt(res.data.page_size)
    console.log(res);
  }).catch(() => {
    console.log('dish list 数据请求失败');
  })
}

// 编辑
const handleEdit = (id: number) => {
  console.log('当前传递的id为', id)
  router.push({
    name: 'dish-update',
    params: {
      id: id
    }
  })
  // alert(id)
}

// 删除菜品
const handleDelete = (id: number) => {
  const name = dishList.value.filter(item => item.id === id)[0].name
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
      const res = await http.delete('/admin/dish', {
        data: {
          id: id
        }
      })
      console.log(res);
      ElMessage({
        type: 'success',
        message: `${name} 删除成功`,
      })
      getDish()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      })
    })
};
onMounted(() => {
  getDish()
});


</script>
<style>
.my-page {
  width: 100%;
  margin: 30px 30%;
}
</style>