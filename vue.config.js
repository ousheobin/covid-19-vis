module.exports = {
    publicPath: './',
    pages: {
        index: {
            entry: './src/main.js',
            template: './public/index.html',
            title: 'COVID-19 数据可视化 - 武汉加油'
        }
    },
    productionSourceMap:false,
    configureWebpack:{
        externals: {
            'vue': 'Vue',
            'echarts': 'echarts',
            'axios': 'axios',
            'element-ui': 'ELEMENT',
        },
    }
}   