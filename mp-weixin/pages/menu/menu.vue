maskShow: function maskShow() {
  var _this2 = this;
  // 获取当前购物车中的菜品ID
  var cartDishId = [];
  this.curCart.forEach(function (item) {
    if (item.num > 0) {  // 只添加数量大于0的菜品
      cartDishId.push(item.id);
    }
  });
  
  // 如果购物车为空，不显示推荐
  if (cartDishId.length === 0) {
    this.recommendDishList = [];
    this.frostedShow = false;
    this.swiperDish = false;
    return;
  }

  // 发送请求获取推荐菜品
  (0, _request.request)({
    url: '/smartOrder',
    method: 'POST',
    data: {
      cartId: cartDishId
    }
  }).then(function (res) {
    // 限制推荐菜品数量，确保每个已选菜品对应一个推荐
    _this2.recommendDishList = res.data.slice(0, cartDishId.length);
  }).catch(function (e) {
    console.log(e);
    _this2.recommendDishList = [];
  });
}, 