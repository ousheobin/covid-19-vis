module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? '/production-sub-path/' : '/',
    pages: {
        index: {
            entry: './src/main.js',
            template: './public/index.html',
            title: 'COVID-19 数据可视化 - 武汉加油'
        }
    },
    publicPath: process.env.NODE_ENV === 'production' ? '/covid-19-vis/' : '/',
}