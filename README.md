# DesertHawk

www.ditanshow.com
## 安装依赖库

进入过程目录，直接执行`pip3 install -r requirements.txt`

## 安装mysql 

- 安装mysql并设置用户名密码，创建数据库`blogtest`

-  修改`DjangoBlog/setting.py` 修改数据库配置，如下所示：

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'blogtest',     # 数据库
          'USER': 'root',			# 用户名
          'PASSWORD': '123456',	# 密码
          'HOST': '127.0.0.1',
          'PORT': '3306'
      }
  }
  ```

##  迁移数据库

进入项目目录，执行

```shell
./manage.py makemigrations
./manage.py migrate
```

## 服务启动

进入项目目录，执行

```shell
./manage.py runserver 0.0.0.0:8080
```

浏览器输入 http://127.0.0.1:8080即可访问

## 创建超级管理员

进入项目目录，执行

```shell
./manage.py createsuperuser
```

## 后台管理

 http://127.0.0.1:8080/admin进入admin页面，添加文章





![](https://content-image-1251916339.cos.ap-beijing.myqcloud.com/2021/08/08/994f47f243ab448bb9c3d572042f6ea7.jpg)
![](https://content-image-1251916339.cos.ap-beijing.myqcloud.com/2021/08/08/5b43c5a2687e4475b5f9799f64ba30e5.jpg)



