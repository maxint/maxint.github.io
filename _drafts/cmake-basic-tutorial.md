---
title: "CMake 教程（基础篇）"
category: coding
tags: [c++, tool]
---
{% include JB/setup %}

# 引言

从在学校到工作，使用CMake已经有5年了。刚开始怎么知道这个工具不记不清了，印象是实验室项目用了OGRE图形绘制引擎，它在某个版本开始使用CMake统一各个平台的编译配置。当时正在研究OGRE，对它的所有信息都很关注，由此使用了Mericual代码版本管理工具（类Git，但更易用，Python编写）。扯远了，回正题。对CMake的第一感觉是语法笨拙，各种全局变量，比较混乱。所以当时想不通为什么好些大的开源项目（如OpenCV、KDE、LLVM、Blender等)转向使用CMake，而且每个的CMake配置文件（CMakeLists.txt文件）都写得很长很复杂，新手各种看不明白呀。

但用CMake定义工程有它的优势所在。第一，良好的多平台、多编译环境支持。比如一个多人参与的项目，大家都有自己喜欢或习惯的编译环境，如不同版本的Visual Studio、XCode、Makefiler和Eclipse，甚至不同系统下的IDE。当然，可以为每个平台维护一套工程文件，但同步就成了一个比较烦人的工作。另一方面
