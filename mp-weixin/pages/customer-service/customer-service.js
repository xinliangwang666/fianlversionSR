// pages/customer-service/customer-service.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    
  },

  /**
   * 拨打客服电话
   */
  makeCall: function(e) {
    const phone = e.currentTarget.dataset.phone;
    wx.makePhoneCall({
      phoneNumber: phone,
      success: function() {
        console.log('拨打电话成功');
      },
      fail: function() {
        wx.showToast({
          title: '拨打失败，请稍后重试',
          icon: 'none',
          duration: 2000
        });
      }
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  }
});