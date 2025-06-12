Page({
  data: {
    
  },

  onLoad() {
    
  },

  // 打开政策页面
  openPolicy(e) {
    const type = e.currentTarget.dataset.type;
    let url = '';
    let title = '';
    
    switch(type) {
      case 'service':
        url = 'https://example.com/service-agreement';
        title = '用户服务协议';
        break;
      case 'privacy':
        url = 'https://example.com/privacy-policy';
        title = '隐私政策';
        break;
      case 'terms':
        url = 'https://example.com/terms-of-use';
        title = '使用条款';
        break;
    }
    
    if (url) {
      wx.navigateTo({
        url: `/pages/webview/webview?url=${encodeURIComponent(url)}&title=${title}`
      });
    }
  },

  // 分享应用
  onShareAppMessage() {
    return {
      title: '智慧餐厅订餐系统',
      desc: '让用餐变得更智能、更便捷',
      path: '/pages/menu/menu'
    };
  }
});
