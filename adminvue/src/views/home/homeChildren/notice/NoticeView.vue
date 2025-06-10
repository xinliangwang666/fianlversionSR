<template>
  <!-- <el-button type="primary" class="addNotice" @click="addNotice">添加公告</el-button> -->
  <el-table :data="listData" style="width: 90%;" border>
    <el-table-column prop="index" label="序号" align="center" header-align="center" width="100"></el-table-column>
    <el-table-column prop="title" label="标题" align="center" header-align="center" width="200"></el-table-column>
    <el-table-column prop="description" label="描述" align="center" header-align="center"></el-table-column>
    <el-table-column label="图片" align="center" header-align="center" width="200">
      <template v-slot="{ row }">
        <el-image style="width: 100px; height: 100px" :src="row.img_url" :preview-src-list="[row.img_url]"></el-image>
      </template>
    </el-table-column>
    <el-table-column label="操作" align="center" header-align="center">
      <template v-slot="{ row }">
        <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { ElTable, ElTableColumn, ElImage, ElButton, ElMessage, ElMessageBox } from 'element-plus';
import { NoticeType } from '@/utils/types'
import http from '@/utils/http';
interface Res {
  total: number;
  noticeList: Array<any>;
}
let listData = ref<NoticeType[]>([
  {
    id: 1,
    title: '春天',
    pub_date: 'stringifyQuery',
    description: '相当的不错',
    img_url: 'https://tse3-mm.cn.bing.net/th/id/OIP-C.mcy-SG3iFHkYQErFJcrO0wHaE7?w=203&h=135&c=7&r=0&o=5&dpr=1.5&pid=1.7'
  }
])

// 获取公告
const getNotice = async () => {
  try {
    const res: Res = await http.get('/admin/notice')
    // listData.value = res?.noticeList.map((item: any, index: number) => {
    //   item['index'] = index + 1
    //   return item
    // })
    // console.log(res)
    // listData.value = res.noticeList
    // console.log(res);
    listData.value = res.noticeList.map((item: any, index: number) => {
      item['index'] = index + 1
      return item
    })
  } catch (e) {
    console.log(e)
  }
}
// 删除公告
const deleteNotice = async (id: number) => {
  const name = listData.value.filter(item => item.id === id)[0].title
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
      const res = await http.delete('/admin/notice', {
        data: {
          id: id
        }
      })
      console.log(res);
      ElMessage({
        type: 'success',
        message: `${name} 删除成功`,
      })
      getNotice()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      })
    })
}



const handleDelete = (id: number) => {
  console.log(`删除ID为${id}的数据`);
  deleteNotice(id)
  getNotice()
};
onMounted(() => {
  getNotice()
});


</script>
<style lang="scss" scoped></style>