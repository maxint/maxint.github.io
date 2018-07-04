---
layout: post
title: "用livecd-ftp手工打造arch手记"
category: linux
tags: [linux]
---

>   生命在于不断折腾                --- 不知谁先说的                                             

这些天无聊到arch的wiki上逛，看了些raid、lvm2之类的东西，手痒，于是又开始玩vb了。
也一直想自己手工组装下arch，所以就动手了，简直把google翻了个底朝天，在忙碌了两天和N次的重启（vb的）之后，终于成功了！

先说下总的想法：先选择性的安装base中的pkgs，再配置下sys，后安装kernel，最后安装grub，ok！


## Disks Partioning

这里我用了2块硬盘，用cfdisk or fdisk分区。本来想/dev/sda1为50M，为/boot，sda2为128M为swap。后发现组建raid1后，30%的空间就没了，/boot空间不够了，又不想重下pkgs，只好合并sda{1,2}。我这个raid组合不怎么合理，完全是玩玩的~

```
/dev/sda:
/dev/sda1, (T)fd, 50+128M
/dev/sda3, (T)8e, rest
/dev/sdb:
/dev/sdb1, (T)fd, 50+128M
/dev/sdb3, (T)8e, rest
```

创建raid和lvm分区，/dev/sd{a,b}1组建成raid1，挂载成/boot。因为grub无法支持raid，所以只能用raid1。/dev/sd{a,b}3组成vg(roup)，以支持动态空间分配。


```bash
modprobe dm-mod
pvcreate /dev/sda3
pvdisplay (检查，可选)
vgcreate vg /dev/sda3
vgextend vg /dev/sdb3
vgdisplay (检查，可选)
lvcreate -L3G -n root vg
lvcreate -L300M -n var vg
lvcreate -L1G -n home vg
lvcreate -L128M -n swap vg
modprobe raid1
mdadm --create /dev/md0 --level=1 --raid-device=2 /dev/sda1 /dev/sdb1
# or mdadm -Cv /dev/md0 -l1 -n2 /dev/sd{a,b}1
cat /proc/mdstat (检查raid，可选)    
```

格式化，突然喜欢上了reiserfs

```bash
mkreiserfs /dev/vg/root
mkreiserfs /dev/vg/home
mkreiserfs /dev/vg/var
mkreiserfs /dev/md0
mkswap /dev/vg/swap
swapon /dev/vg/swap 为操作多提供些空间    
```

挂载分区：

```bash
mount /dev/vg/root /mnt
mkdir /mnt/{home,var,boot}
mount /dev/vg/home /mnt/
mount /dev/vg/var /mnt/var
mount /dev/md0 /boot
```


## Configure Network

如果你的livecd做的比较好,网络应该会自动帮你配好了,所以就可以跳过这一步了
不过配置网络也不复杂:

```bash
modprobe 8139too or pcnet32(虚拟机)
ifconfig eth0 up
ifconfig lo up (optional)
dhcpcd eth0
route
ping 网关   
```

PS：如果route不小心设"坏"了，想再次dhcpcd，可以先#dhcpcd eth0 -k下，忘了意思，自己man，实现证明可行


## Selecting Pakages

先设置下/etc/pacman.conf的源
法一：可以从源上下载包列表
wget http://mumhero.8866.org/archlinux/core/os/i686
用sed、awk慢慢过滤吧，假设保存到ibase.tmp文件中

法二：用/arch/setup向导下载好pkgs后，从/mnt/var/cache/pacman/pkg/目录下，用ls、sed、awk出列表。再除去kernel26顶，因为在生成内核先还要设置一些加载modules，假设保存到ibase.tmp文件中


## Installing Pakages

再次检查下ibase.tmp文件内容，删去自己不想要的内容。如果3）步是选择第二个方法，为安装时不再次下载pkgs，可以用以下操作，chroot到/mnt，退出用exit or ctrl+D：

```bash
mount -o bind /dev /mnt/dev
mount -t proc none /mnt/proc
chroot /mnt /bin/bash  
```

现在可以安装了，如果是chroot了，后面的pacman的-r选项就不用了，切记

```
pacman.static -Sy -r /mnt
pacman.static -S cat ibase.tmp -r /mnt
```

## Configure System

```bash
vi /mnt/etc/rc.conf
vi /mnt/fstab 加
/dev/md0 /boot reiserfs noatime, notail（优化选项） 0 1
/dev/mapper/vg-root reiserfs noatime, notail 0 1
/dev/mapper/vg-home reiserfs noatime, notail 0 0
/dev/mapper/vg-var reiserfs noatime, notail 0 0
/dev/mapper/vg-swap swap swap 0 0
```

```bash
vi /mnt/etc/locale.gen
vi /mnt/etc/mkinitrd.conf 在MODULES在filesystem前中加raid、lvm2，以使内核支持raid和lvm
```


## Installing Kernel

生成fallback和normal版kernel

```bash
pacman.static -S kernel26 -r /mnt
```


## Installing Bootloader (Grub)

```bash
cp -a /mnt/usr/lib/grub/i386-pc/* /mnt/boot/grub
grub-install --root-directory=/mnt --recheck /dev/sda
```

如果安装不了，试试chroot到/mnt后，再安装，可以在sd{a,b}都安装

```bash
chroot /mnt
grub
root (hd0,0)
setup (hd0)
quit  
```

```
# /mnt/boot/grub/menu.lst
title Arch Linux [ (hd0,0) ]
boot (hd0,0)
kernel /vmlinuz26 root=/dev/mapper/vg-root md=0,/dev/sda1,/dev/sdb1 ro
initrd /kernel26.img

title Arch Linux [ (hd0,1) ]
boot (hd0,1)
kernel /vmlinuz26 dolvm2 root=/dev/mapper/vg-root md=0,/dev/sda1,/dev/sdb1 ro
initrd /kernel26.img
```

```bash
reboot
```

终于好了，手好酸~

想尝试的，中间遇到问题欢迎跟帖！

再传张安装好正常启动后的图 

![] (http://hiphotos.baidu.com/maxint/pic/item/bec6eed7f442c5c6a044df18.jpg)
