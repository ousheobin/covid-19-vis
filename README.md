# 2019-covid-19

2019-covid 国内数据综合可视化面板. 

链接：https://ousheobin.github.io/covid-19-vis/#/

## 数据源
特别鸣谢以下数据源为本项目提供数据

- [国家统计局](http://data.stats.gov.cn/)
- [国家卫生健康委](http://www.nhc.gov.cn/)
- [BlankerL/DXY-COVID-19-Data](https://github.com/BlankerL/DXY-COVID-19-Data)
- [澎湃新闻美数课 - 疫情数据汇总](https://github.com/839-Studio/Novel-Coronavirus-Updates)
- [澎湃新闻美数课 - 病例数据汇总](https://github.com/839-Studio/Noval-Coronavirus-763-Cases)
- [百度指数](http://index.baidu.com/)
- [微博指数](https://data.weibo.com/index)

## 使用的技术
- Vue.js
- Element UI
- Antv G2
- Echarts (仅用于图的显示)

*本项目部分第三方库使用 bootcdn / unpkg 加速*

## 如何在本地运行
``` shell
$ pip install -r requirement.txt
$ bash ./buildData.sh
$ npm install
$ npm run dev
```

*本项目使用 Github Action 持续构建，并托管于 Github Action*
