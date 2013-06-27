---
layout: post
title: "怎么搭建一个这样的博客"
description: ""
category: life
tags: [web]
---
{% include JB/setup %}

[本博客][4]托管在[GitHub Page](http://page.github.com)上，后台由[Jekyll](http://jekyllrb.com/docs/installation/)生成静态网页。先简单介绍下Jekyll，它由ruby编写的，结合了markdown、Liquid等技术，简化了静态网站的构建过程，配合[disqus](http://www.disqus.com)等在线留言板服务，可以方便的生成具有简单动态功能的网站。

# 在GitHub Page上建立博客

* 注册GitHub账号
* 参考[这里][3]，建立一个 `yourname.github.com` 的repository
* 然后就可以访问这个博客了，地址为：<http://yourname.github.io/>

# 本地调试环境

* 安装[Ruby](http://rubyinstaller.org/downloads/)，推荐Ruby v1.9，v2.0使用时有错误
* 通过[RubyGems](http://docs.rubygems.org/read/chapter/3)安装Jekyll
> $ gem install jekyll

# 本地代码高亮支持（可选）

GitHub Page本身是支持代码高亮的，使用格式如下：

<code><pre>
{&#37; highlight cpp %}
class Test
{
public:
    Test();
    ~Test();
};
{&#37; endhighlight %}
</pre></code>

为了方便本地浏览效果，需要安装Pygments，安装步骤如下：

* 安装[DevKit](http://rubyinstaller.org/downloads/)
* 安装[Python](http://www.python.org)，推荐Python 2.7
* 安装Python [setuptools](http://pypi.python.org/pypi/setuptools)
* 安装Pygments
> $ easy_install pygments

# Jekyll使用说明

### 生成网站

    $ jekyll build [--watch]

### 启动网站后台

    $ jekyll serve [--watch]

这样可以一边修改一边在浏览器中实时刷新查看修改结果，很是方便。

# 代码和管理

GitHub Page当然是由代码管理工具[Git](http://git-scm.com/)来维护，所以需要熟悉使用它。当本地修改好后，push到GitHub就完成网站发布和更新了，很方便。更多关于如何编写Jekyll代码，查看[这里][2]。

# 参考

* [用GitHub Pages搭建博客和Jekyll环境搭建] [1]
* [Jekyllrb Doc] [2]
* [GitHub Page Doc] [3]
* [本博客代码] [4]

[1]: http://greeensy.github.io/github-jekyll/   "用GitHub Pages搭建博客和Jekyll环境搭建"
[2]: http://jekyllrb.com/docs/home/             "Jekyllrb Doc"
[3]: https://help.github.com/categories/20/articles "GitHub Page Doc"
[4]: https://github.com/maxint/maxint.github.io "本博客代码"
