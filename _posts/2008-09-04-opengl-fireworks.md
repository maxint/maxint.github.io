---
title: "OpenGL上的烟花"
category: cg
tags: [cg, opengl]
---

参考这个做的： [http://blog.csdn.net/crazyjumper/archive/2007/10/19/1833483.aspx](http://blog.csdn.net/crazyjumper/archive/2007/10/19/1833483.aspx) 

![](https://cloud.githubusercontent.com/assets/85147/7809097/659e0c40-03ca-11e5-8833-0c1132441406.png)
![](https://cloud.githubusercontent.com/assets/85147/7809096/65289d70-03ca-11e5-8864-850824167eab.png)
![](https://cloud.githubusercontent.com/assets/85147/7809130/ab15d8f2-03ca-11e5-9739-29d43f200d4b.png)


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
