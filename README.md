# 短链接生成

面向少数注册用户的短链接生成服务，以 RESTful API 形式提供。

## 特性

- 短链接是随机生成的 URL-Safe Base64 字符串，长度通过 `settings.BITS` 控制，默认是 `4`，空间在 10<sup>7</sup> 到 10<sup>
  8</sup> 之间（参考[对照表](https://github.com/aixcyi/Seraphonogram/blob/main/cheatsheets/timestamp-mapping.md)），在 100
  个用户 * 100 条短链接的需求下，碰撞概率还是很低的。
- 短链接允许有效期为空，也就是 “长期有效” 的意思。数据库层面这样设计是方便在定期清理时筛选数据，换句话说就是不用遍历这么多行。
- 通过注册用户控制短链接数量膨胀，非常适合接入自己的生态平台，因此免去了长链接的唯一标识和重复性检测。

## 配置

1. 安装 `requirements.txt` 中的所有依赖。
2.
参照 [django template repo](https://github.com/aixcyi/django-template-repo?tab=readme-ov-file#%E9%85%8D%E7%BD%AE%E8%AE%BE%E7%BD%AE)
创建一个 `settings_dev.py` 进行配置。
3. 创建相应的数据库。本项目用的是 PostgreSQL 。
4. 确保缓存服务已经运行。本项目用的是 Redis 。

