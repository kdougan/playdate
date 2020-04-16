module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/assets': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/graphql': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
};
