<template>
  <view class="order-box">
    <!-- 订单类型选择 -->
    <view class="order-sub">
      <u-subsection :list="list" :current="curNow" mode="subsection" @change="sectionChange"></u-subsection>
    </view>

    <swiper class="my-swiper" :style="'height:'+swiperHeight+'px;'" :current="curNow" @change="changeCur">
      <swiper-item>
        <view :id="'content-wrap'+curNow">
          <!-- 历史订单（非未支付状态的订单） -->
          <view v-if="historyOrders.length === 0">
            <u-empty mode="order" icon="http://cdn.uviewui.com/uview/empty/order.png"></u-empty>
          </view>
          <view v-else class="historical-order">
            <view class="order-list-box padding-xs solid">
              <view v-for="(items, index) in historyOrders" :key="index" class="order-item bg-white text-center margin-tb-xs">
                <view class="dish-title flex text-df text-cut justify-around margin-tb-sm">
                  <view class="margin-right-xs">
                    <text class="margin-right-xs">订单号</text>
                    <text>{{items.order_id}}</text>
                  </view>
                  <text>{{items.order_time | timeFormat}}</text>
                  <view class="order-status text-orange" :style="'padding:4rpx 12rpx;border-radius:4rpx;'+getStatusStyle(items.order_status)">
                    {{items.order_status}}
                  </view>
                </view>
                <view v-for="(dish, index) in items.dishes" :key="index" class="dish-box grid col-5">
                  <view class="img">
                    <image mode="scaleToFill" :src="dish.dish_img"></image>
                  </view>
                  <view class="dish_name">{{dish.dish_name}}</view>
                  <view class="dish_price">{{dish.dish_price}}￥</view>
                  <view class="dish_num">x{{dish.dish_count}}</view>
                  <view class="dish_total">{{dish.dish_total_price}}￥</view>
                </view>
                <view class="flex justify-end">
                  <text class="text-left">菜品：{{items.order_num}}-共计{{items.order_total}}￥</text>
                  <button v-if="items.order_status === '已完成'" class="cu-btn content bg-blue margin-left-xs" @tap="againOrder(items)">再来一单</button>
                </view>
              </view>
            </view>
          </view>
        </view>
      </swiper-item>
      
      <swiper-item>
        <view :id="'content-wrap'+curNow">
          <!-- 当前订单（未支付的订单） -->
          <view v-if="currentOrders.length === 0">
            <u-empty mode="car" icon="http://cdn.uviewui.com/uview/empty/car.png"></u-empty>
          </view>
          <view v-else class="historical-order">
            <view class="order-list-box padding-xs solid">
              <view v-for="(items, index) in currentOrders" :key="index" class="order-item bg-white text-center margin-tb-xs">
                <view class="dish-title flex text-df text-cut justify-around margin-tb-sm">
                  <view class="margin-right-xs">
                    <text class="margin-right-xs">订单号</text>
                    <text>{{items.order_id}}</text>
                  </view>
                  <text>{{items.order_time | timeFormat}}</text>
                  <view class="order-status text-orange" style="padding:4rpx 12rpx;background-color:#FF9745;color:white;border-radius:4rpx;">
                    {{items.order_status}}
                  </view>
                </view>
                <view v-for="(dish, index) in items.dishes" :key="index" class="dish-box grid col-5">
                  <view class="img">
                    <image mode="scaleToFill" :src="dish.dish_img"></image>
                  </view>
                  <view class="dish_name">{{dish.dish_name}}</view>
                  <view class="dish_price">{{dish.dish_price}}￥</view>
                  <view class="dish_num">x{{dish.dish_count}}</view>
                  <view class="dish_total">{{dish.dish_total_price}}￥</view>
                </view>
                <view class="flex justify-end">
                  <text class="text-left">菜品：{{items.order_num}}-共计{{items.order_total}}￥</text>
                  <button class="cu-btn content bg-orange margin-left-xs" @tap="payOrder(items)">立即支付</button>
                </view>
              </view>
            </view>
          </view>
        </view>
      </swiper-item>
    </swiper>

    <!-- 口味选择弹窗 -->
    <TypePick ref="flavor" @setFlavor="setFlavor" :flavorList="flavorList"></TypePick>
  </view>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import { request } from '@/common/request.js'
import TypePick from '@/components/TypePick.vue'

export default {
  components: {
    TypePick
  },
  data() {
    return {
      list: ['历史订单', '当前订单'],
      curNow: 0,
      swiperHeight: 2000,
      order_list: [],
      flavorList: [],
      flavor: 1,
      flavorName: '正常',
      // 添加订单状态样式映射
      statusStyle: {
        '已支付': 'background-color:#FF9745;color:white;',
        '已接单': 'background-color:#67C23A;color:white;',
        '已完成': 'background-color:#909399;color:white;',
        '未支付': 'background-color:#E6A23C;color:white;'
      }
    }
  },
  computed: {
    ...mapState(['curCart', 'totalNum', 'totalPrice']),
    // 历史订单（所有非未支付状态的订单）
    historyOrders() {
      return this.order_list.filter(item => 
        ['已支付', '已接单', '已完成'].includes(item.order_status)
      )
    },
    // 当前订单（只显示未支付的订单）
    currentOrders() {
      return this.order_list.filter(item => item.order_status === '未支付')
    }
  },
  methods: {
    ...mapMutations(['ADD2CART', 'clearCart']),
    
    // 切换订单类型
    sectionChange(index) {
      this.curNow = index
    },
    
    // 更新购物车
    updateCart(item, isAdd) {
      this.ADD2CART({
        dish: item,
        add: isAdd
      })
    },
    
    // 选择口味
    selectFlavor() {
      this.$refs.flavor.show = true
    },
    
    // 设置口味
    setFlavor(val) {
      const data = this.flavorList[0][val]
      this.flavor = data.id
      this.flavorName = data.name
    },
    
    // 提交订单
    submitOrder() {
      if (this.totalNum === 0) {
        uni.showToast({
          title: '请先选择菜品',
          icon: 'none'
        })
        return
      }
      
      uni.showModal({
        title: '确认支付',
        content: '总计：￥' + this.totalPrice,
        success: (res) => {
          if (res.confirm) {
            this.createOrder()
          }
        }
      })
    },
    
    // 创建订单
    createOrder() {
      request({
        url: '/order',
        method: 'POST',
        data: {
          total: this.totalPrice,
          flavor_id: this.flavor,
          dishes: this.curCart
        }
      }).then(res => {
        if (res.code === 200) {
          uni.showToast({
            title: '支付成功',
            icon: 'success'
          })
          this.clearCart()
          this.getOrderList()
        }
      })
    },
    
    // 支付已存在的订单
    payOrder(order) {
      uni.showModal({
        title: '确认支付',
        content: '总计：￥' + order.order_total,
        success: (res) => {
          if (res.confirm) {
            request({
              url: '/order/pay/' + order.order_id,
              method: 'POST'
            }).then(res => {
              if (res.code === 200) {
                uni.showToast({
                  title: '支付成功',
                  icon: 'success'
                })
                this.getOrderList()
              }
            })
          }
        }
      })
    },
    
    // 获取订单列表
    getOrderList() {
      request({
        url: '/order',
        method: 'GET'
      }).then(res => {
        this.order_list = res.order_list || []
      })
    },
    
    // 获取口味列表
    getFlavorList() {
      request({
        url: '/flavor'
      }).then(res => {
        this.flavorList = [res.flavorList]
      })
    },
    
    // 获取订单状态的样式
    getStatusStyle(status) {
      return this.statusStyle[status] || ''
    }
  },
  onShow() {
    this.getOrderList()
    this.getFlavorList()
  },
  filters: {
    timeFormat(time) {
      if (!time) return ''
      const re = time.split('T')
      return re.length > 1 ? `${re[0]} ${re[1].split('.')[0]}` : time
    }
  }
}
</script>

<style lang="scss" scoped>
.order-box {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 20rpx;
}

.cart-section {
  background-color: #fff;
  margin: 20rpx;
  border-radius: 12rpx;
  padding: 20rpx;
  
  .cart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20rpx;
    border-bottom: 1px solid #eee;
    
    .total-price {
      color: #ff6b6b;
      font-weight: bold;
    }
  }
  
  .cart-items {
    .cart-item {
      display: flex;
      align-items: center;
      padding: 20rpx 0;
      border-bottom: 1px solid #eee;
      
      .dish-image {
        width: 120rpx;
        height: 120rpx;
        border-radius: 8rpx;
      }
      
      .dish-info {
        flex: 1;
        padding: 0 20rpx;
        
        .dish-name {
          font-size: 28rpx;
          color: #333;
        }
        
        .dish-price {
          font-size: 26rpx;
          color: #ff6b6b;
          margin-top: 10rpx;
        }
      }
      
      .dish-controls {
        display: flex;
        align-items: center;
        
        .control-btn {
          width: 50rpx;
          height: 50rpx;
          line-height: 50rpx;
          text-align: center;
          background-color: #f5f5f5;
          border-radius: 25rpx;
        }
        
        .dish-count {
          padding: 0 20rpx;
        }
      }
    }
  }
  
  .cart-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20rpx;
    
    .flavor-select {
      font-size: 28rpx;
      color: #666;
    }
    
    .pay-btn {
      background-color: #ff6b6b;
      color: #fff;
      padding: 20rpx 40rpx;
      border-radius: 30rpx;
      font-size: 28rpx;
    }
  }
}

.order-item {
  background-color: #fff;
  margin: 20rpx;
  border-radius: 12rpx;
  padding: 20rpx;
  
  .dish-title {
    display: flex;
    justify-content: space-between;
    font-size: 28rpx;
    color: #666;
    padding-bottom: 20rpx;
    border-bottom: 1px solid #eee;
  }
  
  .dish-content {
    .dish-item {
      display: flex;
      align-items: center;
      padding: 20rpx 0;
      
      .dish-image {
        width: 120rpx;
        height: 120rpx;
        border-radius: 8rpx;
      }
      
      .dish-info {
        flex: 1;
        padding-left: 20rpx;
        
        .dish-name {
          font-size: 28rpx;
          color: #333;
        }
        
        .dish-count {
          font-size: 26rpx;
          color: #999;
          margin: 10rpx 0;
        }
        
        .dish-price {
          font-size: 26rpx;
          color: #ff6b6b;
        }
      }
    }
  }
  
  .dish-footer {
    display: flex;
    justify-content: space-between;
    font-size: 26rpx;
    color: #666;
    padding-top: 20rpx;
    border-top: 1px solid #eee;
  }
  
  .order-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 20rpx;
    
    .pay-btn {
      background-color: #ff6b6b;
      color: #fff;
      padding: 20rpx 40rpx;
      border-radius: 30rpx;
      font-size: 28rpx;
    }
  }
}

.historical-order {
  height: calc(100vh - 200rpx);
}
</style> 