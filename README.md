## 运行

1、运行前端vue项目shenshicartoonVue3

输入命令：

 `cnpm install`

 `npm run serve`



2、本地运行Django项目ShenShiAniment

`python manage.py migrate`

`python manage.py runserver 127.0.0.1:8004`

或使用uwsgi启动

编辑后端目录下的uwsgi.ini文件

启动命令

`uwsgi -ini uwsgi.ini`



3、nginx配置



## 功能说明
1、动画播放链接防盗链，链接过期时间自定义。
2、用户登录后，可对动画收藏、评分，留意。
3、动画的搜索、分类筛选、历史播放记录。