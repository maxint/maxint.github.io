---
title: "一个无奈的 BUG"
category: cg
tags: [cg]
---

最近一直在忙毕设，做的是一个增强实现相关的课题。也有好久没写日志了，主要是因为把思绪整理成文字是一件比较费时的事，且自己掌握的知识有限，当心误导群众，所以平时的些许感想或牢骚都直接发在 [微博](http://t.sina.com/maxint) 上了。寒假回家，又得重新修理家里的老机子，因一个SATA接口出问题，使我误以为硬盘出现坏道，删除格式化整块硬盘好几次。后来另了一个SATA接口，问题解决了，但整块硬盘的数据没了，我的游戏和电影呀 :sob:。死马当成活马医，最后终于用硬盘恢复软件 "Recover My Files“ 恢复了大部分数据 :blush:，很是强大！于是，开学刚后来就开始整理硬盘操作心得，写了一半，后来因时间不多就忙别的事了，目前还一直是草稿状态。。

<!--more-->

再接着说说毕设的事。不得不嘘下自己的一个恶习，什么事都想整得完美些，把很多时间浪费在次要的细节上了，这次选编程平台就是一个例子。因为整个项目算是属于可视化的，用 OGRE 做可视化的好像比较少。学术业用 OpenGL 的比较多，但资源和绘制状态管理起来又比较麻烦了。直接用 OpenGL、D3D API 与用 OGRE、OSG 等基于场景树管理的绘制引擎的一个重要区别是它们的绘制模式不同，前者使用的是 立即模式（[Immidiate Mode](http://en.wikipedia.org/wiki/Immediate_mode)），后者使用的是保留模式 （[Retained Mode](http://en.wikipedia.org/wiki/Retained_mode)）。简单的说，前者需要用户（程序员）控制绘制的每一个细节，调用 API 立即得到绘制结果，如调用 glCallList() 后，就<strong>立即</strong>把绘制结果写到 color buffer、depth buffer 或 stecile buffer 中的。而后者只需要给引擎一些高级的命令，如物体放哪里，什么材质的，然后引擎控制绘制细节，优化绘制顺序（如尽可能减少绘制状态切换），调用相关的低层 API，用户<strong>不能立即</strong>得到绘制结果。就好像你先把命令录制在磁带上，之后引擎不断回放这磁带。大多数新手都是看 OpenGL 红宝书过来的，习惯了立即模式，当要实现一个在保留模式中不直观的操作时就郁闷了，如 stencil buffer、depth buffer 和 clip plane 相关的操作。遇到问题第一时间 google，翻 WIKI 或 BBS 就对了，如果还没有解决就只好看源代码。花了一些时间去尝试几个绘制引擎库，有 [G3D](http://g3d.sourceforge.net/)、[Visualization Library](http://www.visualizationlibrary.com/)、[OSG](http://www.openscenegraph.org/)、[Coin3D](http://www.coin3d.org/)、[OGRE](http://www.ogre3d.org/)，留下的印象是：

- `G3D`：见过实验室的几个项目是用这做的。称各模块（如纹理、材质类）可以独立使用；几乎没什么场景树管理，支持传统的立即模式；附带光线跟踪引擎，例程比较酷；自带GUI。
- `Visualization Library`：不怎么出名，偶得。如其名，主要针对可视化而设计的；有场景树管理，也支持立即模式，不过这两者混合也不好控制吧；带线绘制、体绘制等可视化算法。
- `OSG`：本科做SRTP时接触的第一个绘制引擎，看了王锐博士翻译的一本教程后，因为课题改做图像就没用过了，老牌绘制引擎，在学术界用得比较多（相当大部分人还是直接用 `OpenGL` 或自己写引擎）。与 `OGRE` 相比，场景树节点带有材质属性；有很多官方扩展插件，如地形、虚拟仿真、体绘制等。
- `Coin3D`：`Qt` 官方推荐的，与 `SGI` 的老牌图形 `API` [Open Inventor](http://en.wikipedia.org/wiki/Open_Inventor) 兼容，在翻阅了一些文档和代码后，还是没理出思路，果断不用了。
- `OGRE`：参与HJ师兄的项目时接触到的，摸索了很久（至今还有摸索），工业界认可度比较高，已有好些游戏使用，如 [Torchlight] (http://www.runicgames.com/)。场景树节点属性简单，场景内容不是场景树节点的子类；用脚本定义资源，资源管理功能强大；很是 ym ex-leader sinbad，贡献了那么好的一个绘制平台，并在 BBS 上热心回复新手的各种问题。


目前的编程平台是 `Qt` + `OGRE` + `OpenCV` + `ARToolKitPlus`，就是一个大杂烩，毕竟是搞研究嘛，如果再把时间花费在一些工程细节上就是和自己过不去了。

下面说说昨天花了一个晚上看源代码都没解决的苦笑不得的问题。我想使用一个类似 [Deferred Shading](http://en.wikipedia.org/wiki/Deferred_shading) 的基于 GBuffer 的绘制方式，使用的是 OGRE 的 Compositor System。这里需要用到几张纹理，使用 Render To Texture （RTT）技术，一个问题是每张RTT 都是有个自的 depth buffer 和 color buffer，而场景内容的正确绘制依赖于 depth buffer（做过 z-buffer 作业的同学应该都明白吧）。后来偶然[从OGRE BBS 上看到](http://www.ogre3d.org/forums/viewtopic.php?f=2&amp;t=46263&amp;start=0)，compositor 中的 RTT，如果大小和格式一样，会共用同一个 depth buffer。这不仅节约了资源，还可以使一些依赖 depth buffer 的操作更方便了（当然手动 copy depth buffer 也是可行的，只是要多一些操作）。于是，我想把部分物体绘制到第一张 RTT 中，再开始第二张 RTT 的绘制时，只清空 color buffer（上一帧留下的结果），保留第一张 RTT 的 depth buffer。在 [OGRE 相关文档](http://www.ogre3d.org/docs/manual/manual_32.html#compositor_clear)，于是改写脚本为：


```
pass clear
{
    buffers colour
}
```

但结果显示 depth buffer 还是被清除了，第一时间反应是共享没成功吗？ debug 跟踪到 `OGRE` 源代码，发现 `pass->getClearBuffers()` 得到的结果居然包含 `FBT_DEPTH`，难道系统没解析到这一句话吗？在源码中穿梭良久，后来终于发现一个有一条错误输出，怎么出问题不先去看看 log 呀。


```
unknown error in model.compositor(38): token "buffers" is not recognized
```

google 到 [BBS 上的一个帖](http://www.ogre3d.org/forums/viewtopic.php?f=2&amp;t=46043&amp;p=422642#p422642)，又是 sinbad 的回复解决了问题。看完第一楼时以为明白了，改成：

```
clear
{
    buffers colour
}
```

断续 error，再往下看才明白，我和 lz 犯了同样的错误，正确的写法应该是：

```
pass clear
{
    clear
    {
        buffers colour
    }
}
```

太汗了~不看这个帖，我不知还得在这里郁闷多久，manual 上是不是应该给出一个 WARNING 或代码段之类的啊。

### 总结

- 不要追求事事完美，特别是一些无关大局的细节。
- 不要把事情复杂化，KISS 原则，先用简单的方法，实在万不得以才去大动干戈。
