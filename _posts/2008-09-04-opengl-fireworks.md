---
title: "OpenGL上的烟花"
category: cg
tags: [cg, opengl]
---

参考这个做的： [http://blog.csdn.net/crazyjumper/archive/2007/10/19/1833483.aspx](http://blog.csdn.net/crazyjumper/archive/2007/10/19/1833483.aspx) 

![](http://hiphotos.baidu.com/maxint/pic/item/5c6a46c298fde8020ff47798.jpg)

![](http://hiphotos.baidu.com/maxint/pic/item/78329ed900f43bf038012f99.jpg)

![](http://hiphotos.baidu.com/maxint/pic/item/743d9b3107b08900eac4af9a.jpg)

只贴下数据结构

```cpp
#define MAX_PARTICLES  24             // 小烟花个数
#define MAX_TAIL       30             // 烟花尾部长度
#define MAX_FIRE       5              // 烟花总个数
#define PI             3.1415926
#define COLOR_NUM      12

static GLfloat colors[COLOR_NUM][3]=  // 彩虹颜色
{
     {1.0f,0.5f,0.5f},{1.0f,0.75f,0.5f},{1.0f,1.0f,0.5f},{0.75f,1.0f,0.5f},
     {0.5f,1.0f,0.5f},{0.5f,1.0f,0.75f},{0.5f,1.0f,1.0f},{0.5f,0.75f,1.0f},
     {0.5f,0.5f,1.0f},{0.75f,0.5f,1.0f},{1.0f,0.5f,1.0f},{1.0f,0.5f,0.75f}
};

GLfloat zoom = -40.0f;                // 视角远近

typedef struct
{
     float x, y, z;                   // 粒子位置
} PARTICLE;

typedef struct
{
     PARTICLE particles[MAX_TAIL];
     float xspeed, yspeed, zspeed;    // 粒子速度
     float xg, yg, zg;                // 加速度
} TAIL;

struct
{
     TAIL tails[MAX_PARTICLES];
     float r, g, b;                   // 颜色
     GLfloat life;                    // 生命
     GLfloat fade;                    // 衰减速度
     GLfloat rad;                     // xz平面上的运动速度
     int style;                       // 上升还是下降
     int count;                       // 小烟花尾部点数
} Fire[MAX_FIRE];
```
