import request from '../../utils/request';

Page({
  data: {
    address: null,
    editAddress: '',
    isEditing: false
  },

  onLoad: function() {
    this.checkLoginAndGetAddress();
  },

  onShow: function() {
    this.checkLoginAndGetAddress();
  },

  // 检查登录状态并获取地址
  checkLoginAndGetAddress: function() {
    const sessionid = wx.getStorageSync('sessionid');
    if (!sessionid) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
      return;
    }
    this.getAddress();
  },

  // 获取地址
  getAddress: function() {
    wx.showLoading({
      title: '加载中...'
    });

    request.getAddress()
      .then(res => {
        if (res.status === 'success') {
          this.setData({
            address: res.data.addr || null,
            editAddress: res.data.addr || ''
          });
        }
      })
      .catch(err => {
        console.error('获取地址失败：', err);
        wx.showToast({
          title: err.data?.msg || '获取地址失败',
          icon: 'none'
        });
      })
      .finally(() => {
        wx.hideLoading();
      });
  },

  // 添加新地址
  handleAddress: function() {
    const sessionid = wx.getStorageSync('sessionid');
    if (!sessionid) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }

    wx.chooseAddress({
      success: (res) => {
        wx.showLoading({
          title: '保存中...'
        });

        const addr = `${res.provinceName}${res.cityName}${res.countyName}${res.detailInfo}`;
        request.updateAddress({
          addr: addr
        })
          .then((result) => {
            if (result.status === 'success') {
              this.setData({
                address: result.data.addr,
                editAddress: result.data.addr,
                isEditing: false
              });
              wx.showToast({
                title: '保存成功',
                icon: 'success'
              });
            }
          })
          .catch(err => {
            console.error('保存地址失败：', err);
            wx.showToast({
              title: err.data?.msg || '保存失败',
              icon: 'none'
            });
          })
          .finally(() => {
            wx.hideLoading();
          });
      },
      fail: (err) => {
        if (err.errMsg !== "chooseAddress:fail cancel") {
          wx.showToast({
            title: '选择地址失败',
            icon: 'none'
          });
        }
      }
    });
  },

  // 进入编辑模式
  handleEdit: function() {
    this.setData({
      isEditing: true,
      editAddress: this.data.address || ''
    });
  },

  // 取消编辑
  handleCancel: function() {
    this.setData({
      isEditing: false,
      editAddress: this.data.address || ''
    });
  },

  // 处理输入
  handleInput: function(e) {
    this.setData({
      editAddress: e.detail.value
    });
  },

  // 保存地址
  handleSave: function() {
    if (!this.data.editAddress.trim()) {
      wx.showToast({
        title: '地址不能为空',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({
      title: '保存中...'
    });

    request.updateAddress({
      addr: this.data.editAddress.trim()
    })
      .then((result) => {
        if (result.status === 'success') {
          this.setData({
            address: result.data.addr,
            isEditing: false
          });
          wx.showToast({
            title: '保存成功',
            icon: 'success'
          });
        }
      })
      .catch(err => {
        console.error('保存地址失败：', err);
        wx.showToast({
          title: err.data?.msg || '保存失败',
          icon: 'none'
        });
      })
      .finally(() => {
        wx.hideLoading();
      });
  }
}); 