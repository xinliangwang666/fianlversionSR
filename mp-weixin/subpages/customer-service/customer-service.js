Page({
  data: {
    // 页面的初始数据
  },
  onLoad: function() {
    // 页面加载时执行的初始化逻辑
  },
  // 拨打电话
  callService: function() {
    wx.makePhoneCall({
      phoneNumber: '400-123-4567'
    })
  }
}) 