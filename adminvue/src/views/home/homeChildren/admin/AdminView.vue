<template>
  <el-table :data="AdminList" border>
    <el-table-column prop="index" label="序号" width="200" align="center" header-align="center"></el-table-column>
    <el-table-column prop="name" label="标题" align="center" header-align="center"></el-table-column>
    <el-table-column prop="password" label="密码" align="center" header-align="center"></el-table-column>
    <el-table-column prop="phone" label="电话" align="center" header-align="center"></el-table-column>
    <el-table-column prop="role" label="角色" align="center" header-align="center"></el-table-column>
    <el-table-column label="操作" align="center" header-align="center">
      <template v-slot="{ row }">
        <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { ElTable, ElTableColumn, ElButton, ElMessageBox, ElMessage } from 'element-plus';
import { AdminType } from '@/utils/types'
import http from '@/utils/http'

// 添加按钮const formInline = reactive({


const AdminList = ref<AdminType[]>([])
// 添加事件
// const onSubmit = () => {
//   alert(111)
// }

// 获取数据
const getAdmin = () => {
  http.get('admin/adminInfo').then(res => {
    const data = res.data.admin_list.map((item: any, index: number) => {
      const role = ['超管', '管理员', '商家']
      item['index'] = index + 1
      item['role'] = role[parseInt(item.role)]
      return item
    })
    AdminList.value = data
    // console.log(res)
  }).catch(() => {
    console.log('请求发送失败');
  })

}
onMounted(() => {
  getAdmin()
})


// 删除按钮
const handleDelete = (id: number) => {
  const name = AdminList.value.filter(item => item.id === id)[0].name
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
      http.delete('/admin/adminInfo', {
        data: {
          id: id
        }
      })

      ElMessage({
        type: 'success',
        message: `${name} 删除成功`,
      })
      getAdmin()
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