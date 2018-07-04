---
title: "终于写好Z Buffer作业了"
category: cg
tags: [cg]
---

Z buffer这个算法比较简单，基本就照教材上写的，省去了活化多边形链表，感觉没必要。就核心代码，有位师兄用一个晚上就写好了，我比较挫用了一天时间。为了添加一些一般3D SDK（e.g. D3D OpenGL）的简单绘制功能，如局部光照模型、逐像素光照计算（Per Pixel Lighting）等，重新整理了程序架构和算法。

# 主要功能

*    obj文件载入，只用到顶点位置和法向量信息，没有法向的根据模型计算法向，取差角小于90度的邻面共点平均。
*    Gouraud和Phong绘制模型，即对颜色的双线性插值（Gouraud Shading or Per Vertex Shading）和对法向量的双线性插值（Phong Shading or Per Pixel Shading）。
*    光照计算，Phong光照模型，已实现点光源和方向光。
*    正交投影（Orthogonal Projection）和透视投影（Perspective Projection）。

数据结构是仿D3D的，接口是仿OpenGL的，依照OpenCV代码学用template，界面是Qt的，没有使用第三方3D库。

```cpp
class CScanLine
{
public:
    CScanLine(int w, int h, QImage *img);

    void setRenderTarget(int w, int h, QImage *img);

    // start create target
    void begin(TargetType type);
    void end();

    // 数据输入
    void vertex3d(double x, double y, double z);
    void color3f(float r, float g, float b); 

    // 清空缓存
    void clear(int target, const Color4u & c = Color4u(0,0,0,255), double depth = 1.0);

    // 相机相关, facade design model
    void lookAt(const Vec3d & eye, const Vec3d & at, const Vec3d & up);
    void perspective(double fovy, double aspect, double zNear, double zFar);
    void frustum(double left, double right, double bottom, double top, double near, double far);
    void ortho(double left, double right, double bottom, double top, double near, double far);

    void setRenderState(int state, int val);
};
```

# 存在问题

多边形边沿部分有锯齿，主要是因为相邻多边形在这里深度都一样，反复覆盖。

# 截图

![](https://cloud.githubusercontent.com/assets/85147/7808995/b8dba6ac-03c9-11e5-8555-22f620c6cb8b.png)
![](https://cloud.githubusercontent.com/assets/85147/7809021/e0a6e64c-03c9-11e5-8a27-f86bf94bfb08.png)
![](https://cloud.githubusercontent.com/assets/85147/7809022/e0ad1e5e-03c9-11e5-9a47-07a051de4ddc.png)

