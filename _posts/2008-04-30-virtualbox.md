---
title: "关于VirtualBox虚拟机的网络配置"
category: software
tags: [linux, virtualbox]
---

VB而不用VM（vmware）呢？VM的网络配置不是比VB的简单得多吗？其实没什么在原因，只是最近对开源的东西热情高涨，且VB的体积比VM小得多，安装文件VB：17M，而VM6：130M+，我得承认我是洁癖男（嘿嘿~所以才喜欢Arch）。好，现在进入正题。


### 要求 ###

guest对host可见，这样host就可以用ssh登录guest了，guest通过NAT与host共享上网

![](http://hiphotos.baidu.com/maxint/pic/item/76cabb8253200bb00df4d2ce.jpg)

其中host上的external1设置：

![](http://hiphotos.baidu.com/maxint/pic/item/d2da4918c58c0f1534fa41dd.jpg)

guest（Archlinux）配置(/etc/rc.conf部分)：

```
lo="lo 127.0.0.1"eth0="eth0 192.168.0.98 netmask 255.255.255.0 broadcast 192.168.0.255"eth1="dhcp"INTERFACES=(lo eth0 eth1)
#
# Routes to start at boot-up (in this order)
# Declare each route then list in ROUTES
#     - prefix an entry in ROUTES with a ! to disable it
#
gateway="default gw 192.168.0.2"ROUTES=(!gateway)
```

这样guest通过192.168.0.2访问host，host通过192.168.0.98访问guest


### 两guest组网互连 ###

guests的配置与上面相同，在WIN的网络连接窗口里，选中两虚拟网卡，再右击桥接即可，可实现guests、host互可见，不过guests对外部网络还是不可见的，到现在我还不知道有什么方法实现。

![](http://hiphotos.baidu.com/maxint/pic/item/65f789634ed2b7720e33fa6d.jpg)


### Linux主机下的桥接方式 ###

还不大明白原理。

网桥工作在TCP/IP的第二层，数据链路层。它只能感知MAC地址，对IP及以上层是无法感知的。你可以把网桥想象成交换机，一般情况下有两个 口，数据在两个口之间转发，Linux下的桥接设备可以加入很多接口，真正地像一个多口的交换机，而且还支持STP( spanning tree protocol )。


### 参看 ###
[http://blog.ccidnet.com/blog-htm-do-showone-uid-61344-itemid-183967-type-blog.html](http://blog.ccidnet.com/blog-htm-do-showone-uid-61344-itemid-183967-type-blog.html) *    
[http://www.linuxsir.org/bbs/showthread.php?t=293771](http://www.linuxsir.org/bbs/showthread.php?t=293771) *
