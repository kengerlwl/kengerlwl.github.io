---
title: VMWare ESXi系统中给虚拟机硬盘扩容记录
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-06 15:27:31
password:
summary:
tags:
- 实验室
- linux
- 存储扩容
categories:
- 实验室

---



**基本概念：**

- 物理卷：PV，physical volume，将物理分区(如/dev/sda1)转换之后，具备LVM相关管理参数的存储逻辑块
- 物理单元：PE，physical extent，初始化后的PV的基本单元，PV的存储块
- 卷组：VG，volume group，可以理解为将物理卷合并在一起的一个大分区
- 逻辑卷：LV，logical extent，从VG中划分的逻辑分区，如root/swap等分区
- LVM更多释义：[LVM 百度百科](https://baike.baidu.com/item/LVM/6571177)

## 一、增加虚拟机磁盘并创建分区

1. 首先当然是在ESXi（我是vSphere）中修改对应虚拟机的磁盘空间啦：
![image-20210825200149158](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/d81e205c81c7a10b039aeb2ce7b85667/20bf9e4b2c26f318a056aa009ea36d6f.png)



2. 修改磁盘大小后，此时虚拟机中只是新增了未分配的空闲磁盘空间，所以需要将其创建分区，合并到VG中。

   ```bash
   #系统中当前的PV
   [root@centos7 ~]# lsblk
   NAME           MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
   sda              8:0    0  100G  0 disk 
   ├─sda1           8:1    0    1G  0 part /boot
   └─sda2           8:2    0   49G  0 part 
     ├─vg001-root 253:0    0 45.1G  0 lvm  /
     └─vg001-swap 253:1    0  3.9G  0 lvm  [SWAP]
   ```

   将空闲空间创建新分区：
   （为描述清楚，我将原始打印贴出，#注释为操作步骤与说明）

   ```bash
   #使用fdisk命令，设备为以上lsblk列出的/dev/sda
   [root@centos7 ~]# fdisk /dev/sda
   
   #输入n 新建分区，其他情况请输入m查看帮助
   Command (m for help): n
   
   Partition type: 
      p   primary (2 primary, 0 extended, 2 free)
      e   extended
   #输入p 选择主分区
   Select (default p): p
   
   #输入分区号，回车默认就行
   Partition number (3,4, default 3): 
   
   #输入起始扇区号，回车默认就行
   First sector (104857600-209715199, default 104857600): 
   Using default value 104857600
   
   #输入结束扇区号，回车默认就行
   Last sector, +sectors or +size{K,M,G} (104857600-209715199, default 209715199): 
   Using default value 209715199
   Partition 3 of type Linux and of size 50 GiB is set
   
   #输入t 修改分区类型
   Command (m for help): t
   
   #选择分区号，同上分区号，回车默认就行
   Partition number (1-3, default 3): 
   
   #输入8e，修改分区为LVM类型（8e就是Linux LVM的hex代码，可以输入L列出所有代码进行了解）
   Hex code (type L to list all codes): 8e
   Changed type of partition 'Linux' to 'Linux LVM'
   
   #输入w 写入分区表
   Command (m for help): w
   The partition table has been altered!
   ......
   the next reboot or after you run partprobe(8) or kpartx(8)
   Syncing disks.
   
   ###命令顺序依次为：
   fdisk /dev/sda
   n （新建分区）
   p （选择分区类型为主分区）
   3 （分区编号）
   回车 （起始扇区号，默认）
   回车 （结束扇区号，默认）
   t （修改分区类型）
   3 （要修改的分区号）
   8e （修改为LVM，8e为Hex代码）
   w （写入分区表）
   ```

   截图：

   [![image-20210825204858687](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/d81e205c81c7a10b039aeb2ce7b85667/d81a49051e4362a9450638a54c0824ce.png)](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/d81e205c81c7a10b039aeb2ce7b85667/d81a49051e4362a9450638a54c0824ce.png)

   

3. 保存分区表后可见，系统提示仍在使用分区表，重启系统或者执行`partprobe`进行磁盘同步

   ```bash
   [root@centos7 ~]# partprobe
   [root@centos7 ~]# lsblk
   NAME           MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
   sda              8:0    0  100G  0 disk 
   ├─sda1           8:1    0    1G  0 part /boot
   ├─sda2           8:2    0   49G  0 part 
   │ ├─vg001-root 253:0    0 45.1G  0 lvm  /
   │ └─vg001-swap 253:1    0  3.9G  0 lvm  [SWAP]
   └─sda3           8:3    0   50G  0 part 
   ```

4. s**da3就是新建的分区，需要将其格式化**
   xfs文件系统`mkfs.xfs /dev/sda3`

   ext4文件系统`mkfs.ext4 /dev/sda3` (**ubuntu为ext4系统**)

   (CentOS7默认文件系统为xfs，若不确定可以使用命令`df -hT`查看)

   ```bash
   [root@centos7 ~]# mkfs.xfs /dev/sda3
   meta-data=/dev/sda3              isize=512    agcount=4, agsize=3276800 blks
            =                       sectsz=512   attr=2, projid32bit=1
   ......
   ```

## 二、将创建好的新分区添加到已有的VG中，将该VG扩容

1. 进入LVM控制台：

   ```bash
   [root@centos7 ~]# lvm
   lvm> 
   ```

2. 初始化分区，即将物理分区初始化为LVM物理卷。转化后的PV，可以创建VG，也可以将其合并至现有VG中。

   ```bash
   lvm> pvcreate /dev/sda3
   WARNING: xfs signature detected on /dev/sda3 at offset 0. Wipe it? [y/n]: y
     Wiping xfs signature on /dev/sda3.
     Physical volume "/dev/sda3" successfully created.
   ```

3. 查看VG名

   ```bash
   lvm> vgdisplay
     --- Volume group ---
     VG Name               vg001
   ```

4. 将初始化好的`/dev/sda3` PV加入到以上VG

   ```bash
   lvm> vgextend vg001 /dev/sda3
     Volume group "vg001" successfully extended
   ```

5. 重新查看VG信息，**将Free PE（即新增的PV，请看开头基本概念）分配给LV**

   ```bash
   #确定VG信息，关键信息为Free  PE  12800
   lvm> vgdisplay
     --- Volume group ---
     VG Name               vg001
     ......
     VG Size               98.99 GiB
     PE Size               4.00 MiB
     Total PE              25342
     Alloc PE / Size       12542 / 48.99 GiB 
     #需要关注的信息：
     Free  PE / Size       12800 / 50.00 GiB
   ```

   ```bash
   #确定LV信息，关键信息为LV Path，即要扩容的LV，如root分区为/dev/vg001/root
   lvm> lvdisplay
     --- Logical volume ---
     LV Path                /dev/vg001/swap
     LV Name                swap
     VG Name                vg001
     ......
     LV Status              available
     LV Size                <3.88 GiB
     ......
   
     --- Logical volume ---
     LV Path                /dev/vg001/root #这就是我们的目标目录
     LV Name                root
     VG Name                vg001
     ......
     LV Status              available
     LV Size                <45.12 GiB
     ......
   ```

6. 扩容对应的LV，即将Free PE分配给该LV

   ```bash
   lvm> lvextend -l +12800 /dev/vg001/root
     Size of logical volume vg001/root changed from <45.12 GiB (11550 extents) to <95.12 GiB (24350 extents).
     Logical volume vg001/root successfully resized.
   ```

   再次vgdisplay，可见对应的LV已经扩容

   ```bash
   lvm> lvdisplay
    --- Logical volume ---
     LV Path                /dev/vg001/root
     LV Name                root
     VG Name                vg001
     ......
     LV Size                <95.12 GiB
   
   #退出lvm控制台
   lvm> quit
   ```

## 三、扩容文件系统

1. 之前的操作只是将LV（/root）分区扩容，仍需将文件系统扩容，否则不能使用扩容后的空间

2. **注意 centos为以下**

   ```bash
   [root@centos7 ~]# xfs_growfs /dev/vg001/root
   meta-data=/dev/mapper/vg001-root isize=512    agcount=4, agsize=2956800 blks
   ......
   data blocks changed from 11827200 to 24934400
   
   ```
   **ubuntu为以下**

   ```undefined
   要对应响应的文件系统
   resize2fs 对应的是 ext2、ext3、ext4
   resize2fs /dev/ubuntu-vg/ubuntu-lv
   ```

3. 查看分区大小，可见已扩容成功

   ```bash
   [root@template-centos7_6_1810 ~]# df -lh
   Filesystem              Size  Used Avail Use% Mounted on
   /dev/mapper/vg001-root   96G  3.3G   92G   4% /
   /dev/sda1              1014M  149M  866M  15% /boot
   ```





# ref

[centos](https://http.ooo/18.html)

[ubuntu](https://www.jianshu.com/p/ec7a8d80af13)