<template>
  <div>
    <el-table :data="userData" style="width: 100%" border>
      <el-table-column fixed prop="index" label="序号" width="100" align="center" header-align="center" />
      <el-table-column label="用户头像" width="140" align="center" header-align="center">
        <template v-slot="{ row }">
          <el-image style="width: 100px; height: 100px" :src="row.avatar_url"
            :preview-src-list="[row.img_url]"></el-image>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="用户名" width="120" align="center" header-align="center" />
      <el-table-column prop="password" label="密码" width="200" align="center" header-align="center" />
      <el-table-column prop="gender" label="性别" width="100" align="center" header-align="center" />
      <el-table-column prop="phone" label="电话" width="120" align="center" header-align="center" />
      <el-table-column prop="email" label="邮箱" width="220" align="center" header-align="center" />
      <el-table-column prop="integral" label="积分" width="120" align="center" header-align="center" />
      <el-table-column fixed="right" label="Operations" width="220" align="center" header-align="center">
        <template #default="{ row }">
          <el-button type="danger" size="small" @click="deleteUser(row.id)">删除</el-button>
          <el-button type="primary" size="small" @click="editUser(row.id)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="my-page">
      <el-pagination background v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
        :page-sizes="[5, 10, 15, 20, 25, 50]" @current-change="handleCurrentChange" @size-change="handleSizeChange"
        layout="sizes, prev, pager, next" :hide-on-single-page="false" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import http from '@/utils/http'
import { UserType } from '@/utils/types'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
const router = useRouter()
onMounted(() => {
  getUser()
})
// 当前页数
const currentPage = ref(1)
// 菜品总数
const total = ref(100)
// 分页数据，也就是一页的数量
const pageSize = ref(5)
const handleSizeChange = (val: number) => {
  pageSize.value = val
  getUser()
}
// 当前currentchange发生变化
const handleCurrentChange = (val: number) => {
  console.log('当前发生了变化', val);
  currentPage.value = val
  getUser()
}






// 定义用户列表
const userData = ref<UserType[]>([])

// 获取用户数据
const getUser = () => {
  http.get(`/admin/user?page=${currentPage.value}&page_size=${pageSize.value}`).then(res => {
    // console.log(res);

    // 对返回的结果进行处理，
    userData.value = res.data.user_list.map((item: any, index: number) => {
      item['index'] = index + 1
      item['gender'] = item['gender'] ? '男' : '女'
      return item
    })
    currentPage.value = parseInt(res.data.page_num),
      pageSize.value = parseInt(res.data.page_size),
      total.value = parseInt(res.data.total)
  }).catch(e => {
    console.log(e);
  })
}

// 删除用户
const deleteUser = (id: number) => {
  const name = userData.value.filter(item => item.id === id)[0].name
  ElMessageBox.confirm(
    `确定要删除${name}吗`,
    'Warning',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      http.delete('/admin/user', {
        data: {
          id: id
        }
      })

      ElMessage({
        type: 'success',
        message: `${name} 删除成功`,
      })
      getUser()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      })
    })
}
// 编辑用户
const editUser = (id: number) => {
  router.push({
    name: 'user-update',
    params: {
      id: id
    }
  })
}
</script>
<style>
.my-page {
  width: 100%;
  margin: 30px 30%;
}
</style>
