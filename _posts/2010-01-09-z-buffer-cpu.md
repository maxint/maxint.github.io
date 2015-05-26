---
title: "终于写好Z Buffer作业了"
category: cg
tags: [cg]
---

Z buffer这个算法比较简单，基本就照教材上写的，省去了活化多边形链表，感觉没必要。就核心代码，有位师兄用一个晚上就写好了，我比较挫用了一天时间。为了添加一些一般3D SDK（e.g. D3D OpenGL）的简单绘制功能，如局部光照模型、逐像素光照计算（Per Pixel Lighting）等，重新整理了程序架构和算法。实现的主要功能：

*    obj文件载入，只用到顶点位置和法向量信息，没有法向的根据模型计算法向，取差角小于90度的邻面共点平均。
*    Gouraud和Phong绘制模型，即对颜色的双线性插值（Gouraud Shading or Per Vertex Shading）和对法向量的双线性插值（Phong Shading or Per Pixel Shading）。
*    光照计算，Phong光照模型，已实现点光源和方向光。
*    正交投影（Orthogonal Projection）和透视投影（Perspective Projection）。

数据结构是仿D3D的，接口是仿OpenGL的，依照OpenCV代码学用template，界面是Qt的，没有使用第三方3D库。

```cpp
class CScanLine
{
public:
    CScanLine(int _w, int _h, QImage *_img);

    void setRenderTarget(int _w, int _h, QImage *_img);

    // start create target
    void begin(TargetType _type);
    void end();

    // 数据输入
    void vertex3d(double _x, double _y, double _z);
    void color3f(float _r, float _g, float _b); 

    // 清空缓存
    void clear(int _target, const Color4u & _c = Color4u(0,0,0,255), double _depth = 1.0);

    // 相机相关, facade design model
    void lookAt(const Vec3d & eye, const Vec3d & at, const Vec3d & up);
    void perspective(double fovy, double aspect, double zNear, double zFar);
    void frustum(double left, double right, double bottom, double top, double near, double far);
    void ortho(double left, double right, double bottom, double top, double near, double far);

    void setRenderState(int _state, int _val);
};
```

**存在问题：** 多边形边沿部分有锯齿，主要是因为相邻多边形在这里深度都一样，反复覆盖。

下面是一些截图

![](http://hiphotos.baidu.com/maxint/pic/item/90c84eaf6597dafd7dd92a1f.jpg) 

[![](http://hiphotos.baidu.com/maxint/abpic/item/17418e81ff7660e9bd3e1ec9.jpg)](http://hiphotos.baidu.com/maxint/pic/item/17418e81ff7660e9bd3e1ec9.jpg)
[![](http://hiphotos.baidu.com/maxint/abpic/item/68e709c466393a988326acca.jpg)](http://hiphotos.baidu.com/maxint/pic/item/68e709c466393a988326acca.jpg)
[![](http://hiphotos.baidu.com/maxint/abpic/item/6d03b066616b7015aa184cca.jpg)](http://hiphotos.baidu.com/maxint/pic/item/6d03b066616b7015aa184cca.jpg)
[![](http://hiphotos.baidu.com/maxint/abpic/item/57aa76ee996143182cf534cb.jpg)](http://hiphotos.baidu.com/maxint/pic/item/57aa76ee996143182cf534cb.jpg)
[![](http://hiphotos.baidu.com/maxint/abpic/item/45d1e508c5466601e82488d4.jpg)](http://hiphotos.baidu.com/maxint/pic/item/45d1e508c5466601e82488d4.jpg)
[![](http://hiphotos.baidu.com/maxint/abpic/item/303a554591d6fb17cefca3d5.jpg)](http://hiphotos.baidu.com/maxint/pic/item/303a554591d6fb17cefca3d5.jpg)
[![](http://hiphotos.baidu.com/maxint/abpic/item/a2cfe8557c9b92f5b645aed0.jpg)](http://hiphotos.baidu.com/maxint/pic/item/a2cfe8557c9b92f5b645aed0.jpg)
[![](http://hiphotos.baidu.com/maxint/abpic/item/09e5ecf4b256d45fdcc474d0.jpg)](http://hiphotos.baidu.com/maxint/pic/item/09e5ecf4b256d45fdcc474d0.jpg)