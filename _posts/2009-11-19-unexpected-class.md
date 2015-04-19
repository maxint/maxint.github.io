---
title: "Compile error: unexpected class"
category: coding
tags: [cpp]
---

## VS2008错误提示

> error C2236: unexpected 'class' 'SkyCloudParticle'. Did you forget a ';'?

这是一个令人郁闷的错误提示，提示停在:

```cpp
class SkyCloudParticle
{ // << HERE
};
```

## 分析

怀疑是包含的头文件的类定义有问题，但检查后一切正常。后来终于想到可能是在其它地方 include 这个头文件时，前面的头文件中有 class 定义没写好。经查看所有头类定义，终于发现了问题。问题出现在另一个类（SkyCloudsManager）的定义上，包括关系如下：

```cpp
// file: SkyCloudsManager.cpp
#include "SkyCloudsManager.hpp"
#include "SkyCloud.hpp"
```

```cpp
// file: SkyCloud.hpp
#include "SkyCloudParticle.hpp"
```

```cpp
// file: SkyCloudsManager.hpp
class SkyCloudsManager
{
} << DEFINITION ERROR
```
## 总结

冷静思考！
