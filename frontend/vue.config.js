const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',
  assetsDir: '',
  publicPath: '/',
  filenameHashing: true,
  productionSourceMap: false,
  // chainWebpack: config => {
  //   config.module
  //     .rule('js')
  //     .use('babel-loader')
  //     .tap(options => {
  //       options.plugins = [
  //         ...(options.plugins || []),
  //         '@babel/plugin-proposal-optional-chaining'
  //       ];
  //       return options;
  //     });
  // },
  devServer: {
    port: 8081,
    proxy: {
      '^/api': {
        target: 'http://localhost:8080',
        ws: true,
        changeOrigin: true,
        logLevel: 'debug' // Add to see detailed proxy logs
      },
      '^/auth': {
        target: 'http://localhost:8080',
        ws: true,
        changeOrigin: true
      }
    }
  }
})