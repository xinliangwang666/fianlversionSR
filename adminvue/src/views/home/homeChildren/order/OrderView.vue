<template>
  <el-table :data="orderList" style="width: 100%" border>
    <el-table-column fixed prop="index" label="序号" width="100" align="center" header-align="center" />
    <el-table-column prop="user_name" label="下单用户" width="80" align="center" header-align="center" />
    
    <!-- 整合后的状态列 -->
    <el-table-column label="状态" width="120" align="center">
      <template #default="{ row }">
        <el-tag :type="getStatusTagType(row.status)">
          {{ getStatusText(row.status) }}
        </el-tag>
      </template>
    </el-table-column>

    <el-table-column label="菜品信息" width="720" show-header="false" align="center" header-align="center">
      <template #default="{ row }">
        <el-table :data="row.dishes" style="width: 100%">
          <el-table-column prop="dish_name" />
          <el-table-column width="200" show-headers="false">
            <template #default="{ row }">
              <el-image :src="row.dish_img" style="width: 80px; height: 80px;" />
            </template>
          </el-table-column>
          <el-table-column prop="dish_price" :formatter="formatPrice" />
          <el-table-column prop="dish_count" :formatter="formatDishCount" />
          <el-table-column prop="dish_total_price" :formatter="formatPrice" />
        </el-table>
      </template>
    </el-table-column>

    <el-table-column prop="order_time" label="下单时间" :formatter="formatTime" width="200" align="center" header-align="center" />
    <el-table-column prop="order_total_price" label="总计" width="100" align="center" header-align="center" />
    <el-table-column prop="order_flavor" label="口味" width="120" align="center" header-align="center" />

    <!-- 整合后的操作列 -->
    <el-table-column fixed="right" label="操作" width="280" align="center">
      <template #default="{ row }">
        <!-- 接单按钮：商家和管理员都可见 -->
        <el-button
          v-if="row.status === 'paid'"
          type="success"
          size="small"
          @click="handleOrderAction(row, 'accept')"
        >
          接单
        </el-button>

        <!-- 拒单按钮：商家和管理员都可见 -->
        <el-button
          v-if="row.status === 'paid'"
          type="warning"
          size="small"
          @click="handleOrderAction(row, 'reject')"
          style="margin-left: 8px"
        >
          拒单
        </el-button>

        <!-- 完成按钮：商家和管理员都可见 -->
        <el-button
          v-if="row.status === 'accepted'"
          type="primary"
          size="small"
          @click="handleOrderAction(row, 'complete')"
          style="margin-left: 8px"
        >
          出餐完成
        </el-button>

        <!-- 删除按钮：只有管理员和超管可见 -->
        <el-button
          v-if="userRole === '管理员' || userRole === '超级管理员'"
          type="danger"
          size="small"
          @click="deleteOrder(row)"
          style="margin-left: 16px"
        >
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <div class="my-page">
    <el-pagination background v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
      :page-sizes="[2, 4, 8, 10, 12, 15, 16, 20, 25]" @current-change="handleCurrentChange"
      @size-change="handleSizeChange" layout="sizes, prev, pager, next" :hide-on-single-page="false" />
  </div>
  <audio ref="myAudio" style="opacity: 0;"></audio>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue'
import http from '@/utils/http'
import { ElMessageBox, ElMessage } from 'element-plus'

const myAudio = ref<HTMLAudioElement | null>(null)
let lastOrderId = -1

// 添加用户角色
const userRole = ref('')

onMounted(() => {
  // 获取用户信息
  const userInfo = JSON.parse(localStorage.getItem('loginUser') || '{}')
  userRole.value = userInfo.role || '商家'

  if (myAudio.value != null) {
    myAudio.value.src = require('@/assets/newOrder.mp3')
    myAudio.value.controls = true
    // 添加音频播放结束事件监听
    myAudio.value.onended = () => {
      audioPlay.value = false
    }
  }

  getOrder()
  // 轮询
  hasNewOrder()
  setInterval(() => {
    hasNewOrder()
  }, 1500)  // 改为1.5秒，使提示更及时
})

// 音频播放
const audioPlay = ref(false)
// 当前页数
const currentPage = ref(1)
// 菜品总数
const total = ref(100)
// 分页数据，也就是一页的数量
const pageSize = ref(2)

const handleSizeChange = (val: number) => {
  pageSize.value = val
  getOrder()
}

// 监听播放
watch(audioPlay, (newValue, oldValue) => {
  if (newValue && !oldValue) {
    console.log('当前为true,执行播放')
    myAudio.value?.play()
  }
})

// 当前currentchange发生变化
const handleCurrentChange = (val: number) => {
  console.log('当前发生了变化', val)
  currentPage.value = val
  getOrder()
}

// 格式化数量
const formatPrice = (row: any, column: any, cellValue: string) => {
  return `${cellValue}￥`
}

// 格式化价格
const formatDishCount = (row: any, column: any, cellValue: string) => {
  return `x ${cellValue}`
}

// 格式化时间
const formatTime = (row: any, column: any, cellValue: string) => {
  const times = cellValue.split('T').join('-')
  return times
}

// 定义列表
const orderList = ref([
  {
    id: 1,
    order_total_price: 330,
    user_name: 'aa',
    order_time: '2023-4-20',
    order_flavor: '香辣',
    status: 'paid', // 添加状态示例
    dishes: [
      {
        dish_id: 2,
        dish_name: '烤全羊',
        dish_img: 'http://127.0.0.1:8000/media/dishes/l.png',
        dish_price: 255,
        dish_count: 4,
        dish_total_price: 1000
      },
      {
        dish_id: 1,
        dish_name: '烤乳猪',
        dish_img: 'http://127.0.0.1:8000/media/dishes/l.png',
        dish_price: 255,
        dish_count: 4,
        dish_total_price: 1000
      }
    ]
  }
])

// 整合DeepSeek的状态标签方法
const getStatusTagType = (status: 'unpaid' | 'paid' | 'accepted' | 'rejected' | 'completed') => {
  const map = {
    'unpaid': 'warning',
    'paid': '',
    'accepted': 'success',
    'rejected': 'danger',
    'completed': 'info'
  } as const
  return map[status] || ''
}

const getStatusText = (status: 'unpaid' | 'paid' | 'accepted' | 'rejected' | 'completed') => {
  const map = {
    'unpaid': '待支付',
    'paid': '已支付',
    'accepted': '已接单',
    'rejected': '已拒绝',
    'completed': '已完成'
  } as const
  return map[status] || status
}

// 整合DeepSeek的订单状态更新逻辑
const handleOrderAction = (row: any, action: 'accept' | 'reject' | 'complete') => {
  const actionTextMap = {
    'accept': '接单',
    'reject': '拒单',
    'complete': '完成'
  } as const
  
  ElMessageBox.confirm(
    `确定要${actionTextMap[action] || action}订单吗?`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    http.put('/admin/order', {
      id: row.order_id,
      action: action
    }).then(() => {
      ElMessage.success('订单状态更新成功')
      getOrder()
    }).catch(() => {
      ElMessage.error('操作失败')
    })
  })
}

const getOrder = () => {
  http.get(`/admin/order?page=${currentPage.value}&page_size=${pageSize.value}`).then(res => {
    console.log(res.data.order_list)
    total.value = parseInt(res.data.order_count)
    currentPage.value = parseInt(res.data.page_num)
    pageSize.value = parseInt(res.data.page_size)
    
    const data = res.data.order_list.map((item: any, index: number) => {
      item['index'] = total.value - ((currentPage.value - 1) * pageSize.value + index)
      return item
    })
    orderList.value = data
  })
}

const deleteOrder = (row: any) => {
  // 解构赋值并重命名
  const { user_name, order_id: id } = row
  ElMessageBox.confirm(
    `确定要删除${user_name}的这条订单吗`,
    'Warning',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      http.delete('/admin/order', {
        data: {
          id: id
        }
      }).then(() => {
        ElMessage({
          type: 'success',
          message: `${user_name} 的订单删除成功`,
        })
        getOrder()
      }).catch(() => {
        ElMessage({
          type: 'error',
          message: '订单删除失败',
        })
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      })
    })
}

// 轮询查询是否有新订单
const hasNewOrder = () => {
  http.get(`/admin/hasNew?orderId=${lastOrderId}`).then(res => {
    console.log('change', res.data.change)
    const flag = res.data?.change
    // 发生了变化就再次请求当前页面
    if (flag) {
      console.log('当前您有新订单')
      lastOrderId = res.data.lastId
      getOrder()
      // 只有在真正有新订单时才播放音频
      if (!audioPlay.value) {  // 防止重复播放
        audioPlay.value = true
      }
    }
    // 只有在第一次返回时才会触发
    if (!flag && lastOrderId == -1) {
      lastOrderId = res.data.lastId
    }
  }).catch(e => {
    // 移除错误时的音频播放
    console.error('检查新订单时发生错误:', e)
  })
}
</script>
<style lang="scss" scoped>
.el-table .el-table__row--striped:not(.el-table__row--expanded)>.el-table__cell {
  border-bottom: 1px solid #ebeef5;
}

.my-page {
  width: 100%;
  margin: 30px 30%;
}
</style>    