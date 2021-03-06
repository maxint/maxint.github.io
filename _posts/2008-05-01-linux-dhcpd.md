---
title: "Linux下的DHCP服务配置"
category: linux
tags: [linux]
---

### 测试环境 ###

VirtualBox 下的两台 Archlinux，网络配置都是 Host Interface Networking，在WINDOWS下桥接两虚拟网卡（如下图），网络桥IP为192.168.0.1，guests以这个 IP 为网关，具体实现见前面的日志。有关路由、子网掩码、广播地址、dhcp、DNS的知识，可以去百度百科查看。

![](http://hiphotos.baidu.com/maxint/pic/item/65f789634ed2b7720e33fa6d.jpg)


#### guests(Arch)的网络配置： ####

```
Arch1：IP为192.168.0.98，是DNS服务器，也是DHCP服务器。
Arch2：eth0设为dhcp。
```

#### /etc/dhcpd.conf ####

```cfg
# dhcpd.conf
#
# Sample configuration file for ISC dhcpd
#
# option definitions common to all supported networks...
option domain-name"maxint.org";
option domain-name-servers 192.168.0.98,10.0.2.3 ;
default-lease-time 600;
max-lease-time 7200;
# Use this to enble / disable dynamic dns updates globally.
ddns-update-style none;
# If this DHCP server is the official DHCP server for the local
# network, the authoritative directive should be uncommented.
#authoritative;
# Use this to send dhcp log messages to a different log file (you also
# have to hack syslog.conf to complete the redirection).
log-facility local7;
slightly different configuration for an internal subnet.
subnet 192.168.0.0 netmask 255.255.255.0 {
    range 192.168.0.26 192.168.0.30; # dhcp分配的IP地址范围
    option routers 192.168.0.1;      # 默认路由（网关）
    option subnet-mask 255.255.255.0;# 子网掩码
#   option domain-name"maxint.org";  # 域名服务器的域名
#   option domain-name-servers 192.168.0.98,10.0.2.3; # 域名服务器地址
    option broadcast-address 192.168.0.255; # 广播地址
    default-lease-time 600;
    max-lease-time 7200;
}
```

### 测试技巧 ###

```bash
ip route # 查看路由信息
/etc/rc.d/network restart # 重启网络，再ifconfig检查IP分配情况
```

在Host上，通过/var/log/messages.log（或/var/dhcp/dhcpd.lease）文件查看dhcpd服务工作情况，这里也可以看到IP分配情况。
在Guest上，通过/etc/resolv.conf文件查看DNS分配。
