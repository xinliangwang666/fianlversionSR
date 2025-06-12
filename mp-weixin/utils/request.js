const BASE_URL = 'http://127.0.0.1:8000'; // 本地开发环境

const request = (options) => {
  return new Promise((resolve, reject) => {
    // 获取存储的session_id
    const session_id = wx.getStorageSync('sessionid');
    
    wx.request({
      url: `${BASE_URL}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': session_id ? `Bearer ${session_id}` : '',
        ...options.header
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(res);
          wx.showToast({
            title: res.data.msg || '请求失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        reject(err);
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      }
    });
  });
};

export default {
  // 获取地址
  getAddress: () => {
    return request({
      url: '/address',
      method: 'GET'
    });
  },

  // 更新地址
  updateAddress: (data) => {
    return request({
      url: '/address',
      method: 'POST',
      data: data
    });
  }
}; 