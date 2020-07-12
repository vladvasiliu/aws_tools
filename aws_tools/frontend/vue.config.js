if (!process.env.VUE_APP_VERSION) {
  const { gitDescribeSync } = require('git-describe')
  const gitInfo = gitDescribeSync({ dirtyMark: '-dev' })
  process.env.VUE_APP_VERSION = gitInfo.semverString
}

module.exports = {
  devServer: {
    proxy: {
      '/admin': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/static/admin': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/static/rest_framework': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}
