<template>
  <view class="order-box">
    <!-- 订单类型选择 -->
    <view class="order-sub">
      <u-subsection :list="list" :curNow.sync="curNow" @change="sectionChange"></u-subsection>
    </view>

    <!-- 当前购物车内容 -->
    <view class="cart-section" v-if="curNow === 0 && totalNum > 0">
      <view class="cart-header">
        <text>当前购物车</text>
        <text class="total-price">合计：¥{{ totalPrice }}</text>
      </view>
      <view class="cart-items">
        <view v-for="(item, index) in curCart" :key="index" class="cart-item">
          <image :src="item.dish_img" mode="aspectFill" class="dish-image"></image>
          <view class="dish-info">
            <text class="dish-name">{{ item.name }}</text>
            <text class="dish-price">¥{{ item.price }}</text>
          </view>
          <view class="dish-controls">
            <text class="control-btn" @tap="updateCart(item, false)">-</text>
            <text class="dish-count">{{ item.num }}</text>
            <text class="control-btn" @tap="updateCart(item, true)">+</text>
          </view>
        </view>
      </view>
      <view class="cart-footer">
        <view class="flavor-select" @tap="selectFlavor">
          <text>口味：{{ flavorName }}</text>
        </view>
        <button class="pay-btn" @tap="submitOrder">立即支付</button>
      </view>
    </view>

    <!-- 订单列表 -->
    <swiper class="my-swiper" :current="curNow" @change="changeCur">
      <swiper-item>
        <scroll-view scroll-y class="historical-order">
          <view class="order-list-box">
            <view v-if="curNow === 0 && order_list.filter(item => item.order_status === '未支付').length === 0">
              <u-empty mode="order" icon="http://cdn.uviewui.com/uview/empty/car.png"></u-empty>
            </view>
            <view v-else-if="curNow === 1 && order_list.filter(item => item.order_status === '已支付').length === 0">
              <u-empty mode="order" icon="http://cdn.uviewui.com/uview/empty/car.png"></u-empty>
            </view>
            <view v-else v-for="(items, index) in filteredOrders" :key="index" class="order-item">
              <!-- 订单头部 -->
              <view class="dish-title">
                <text>订单时间：{{ items.order_time }}</text>
                <text>订单状态：{{ items.order_status }}</text>
              </view>
              <!-- 订单内容 -->
              <view class="dish-content">
                <view v-for="(dish, dishIndex) in items.dishes" :key="dishIndex" class="dish-item">
                  <image :src="dish.dish_img" mode="aspectFill" class="dish-image"></image>
                  <view class="dish-info">
                    <text class="dish-name">{{ dish.dish_name }}</text>
                    <text class="dish-count">x{{ dish.dish_count }}</text>
                    <text class="dish-price">¥{{ dish.dish_price }}</text>
                  </view>
                </view>
              </view>
              <!-- 订单底部 -->
              <view class="dish-footer">
                <text>口味：{{ items.order_flavor }}</text>
                <text>总价：¥{{ items.order_total }}</text>
                <text>数量：{{ items.order_num }}</text>
              </view>
              <!-- 未支付订单的支付按钮 -->
              <view class="order-actions" v-if="items.order_status === '未支付'">
                <button class="pay-btn" @tap="payOrder(items)">立即支付</button>
              </view>
            </view>
          </view>
        </scroll-view>
      </swiper-item>
      <swiper-item>
        <scroll-view scroll-y class="historical-order">
          <view class="order-list-box">
            <view v-if="order_list.filter(item => item.order_status === '已支付').length === 0">
              <u-empty mode="order" icon="http://cdn.uviewui.com/uview/empty/car.png"></u-empty>
            </view>
            <view v-else v-for="(items, index) in historyOrders" :key="index" class="order-item">
              <!-- 订单头部 -->
              <view class="dish-title">
                <text>订单时间：{{ items.order_time }}</text>
                <text>订单状态：{{ items.order_status }}</text>
              </view>
              <!-- 订单内容 -->
              <view class="dish-content">
                <view v-for="(dish, dishIndex) in items.dishes" :key="dishIndex" class="dish-item">
                  <image :src="dish.dish_img" mode="aspectFill" class="dish-image"></image>
                  <view class="dish-info">
                    <text class="dish-name">{{ dish.dish_name }}</text>
                    <text class="dish-count">x{{ dish.dish_count }}</text>
                    <text class="dish-price">¥{{ dish.dish_price }}</text>
                  </view>
                </view>
              </view>
              <!-- 订单底部 -->
              <view class="dish-footer">
                <text>口味：{{ items.order_flavor }}</text>
                <text>总价：¥{{ items.order_total }}</text>
                <text>数量：{{ items.order_num }}</text>
              </view>
            </view>
          </view>
        </scroll-view>
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
      list: ['当前订单', '历史订单'],
      curNow: 0,
      order_list: [],
      flavorList: [],
      flavor: 1,
      flavorName: '正常'
    }
  },
  computed: {
    ...mapState(['curCart', 'totalNum', 'totalPrice']),
    // 当前订单（未支付）
    filteredOrders() {
      return this.order_list.filter(item => item.order_status === '未支付')
    },
    // 历史订单（已支付）
    historyOrders() {
      return this.order_list.filter(item => item.order_status === '已支付')
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
    }
  },
  onShow() {
    this.getOrderList()
    this.getFlavorList()
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