---
title: K8S学习
top: false
cover: false
toc: true
mathjax: true
draft: true
date: 2024-04-11 15:27:31
password:
summary:
tags:
- 运维
categories:
- find JOB

---





# K8S学习

## ref

[kubernetes面试题汇总详解-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/1628686)

[Document - K8S 教程 - 易文档](https://k8s.easydoc.net/docs/dRiQjyTY/28366845/6GiNOzyZ/puf7fjYr)



## 为什么需要K8S

传统的docker应用，虽然能够直接将服务打包，快速部署，但是当涉及多个机器，多个容器一起编排运维的时候，就会很麻烦，docker-compose一般也只在一台机器上work。多个机器就会很困难。因此，**需要K8S实现多台机器的自动部署，弹性伸缩。**



## 整体结构

主要由以下几个核心组件组成：

- **etcd（key-value）** **负责存储集群中各种资源对象的信息**。；
- **apiserver 提供了资源操作的唯一入口**，并提供认证、授权、访问控制、API 注册和发现等机制；
- controller manager 负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
- **scheduler 负责资源的调度**，按照预定的调度策略**将 Pod 调度到相应的机器上**；
- kubelet 负责维护容器的生命周期，同时也负责 Volume（CSI）和网络（CNI）的管理；
- **Container runtime（支持docker等常见的的CRI） 负责镜像管理以及 Pod 和容器的真正运行（CRI）**；
- **kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡**；



![Kuberentes 架构（图片来自于网络）](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/6a942e0fbd78bbacf026b27ac02bef3b/b3309a121a94959a6874384cd23a45f7.png)

结构构成

- **master节点，主控节点**
- **node，实际运行服务的节点**
- pod是实际的容器，运行在node里面。**Pod 是在 Kubernetes 集群中运行部署应用或服务的最小单元**，它是可以**支持多容器**的



### 简述 Kubernetes kubelet 的作用？

在 Kubernetes 集群中，在**每个 Node（又称 Worker）上都会启动一个 kubelet 服务进程。**

该进程**用于处理 Master 下发到本节点的任务，管理 Pod 及 Pod 中的容器**。

**每个 kubelet 进程都会在 API Server 上注册节点自身的信息，定期向 Master 汇报节点资源的使用情况**，并通过 cAdvisor 监控容器和节点资源。



### pod是什么

**Pod 是 k8s 中集群部署应用和服务的最小单元，一个 pod 中可以部署多个容器。**

### 副本集（Replica Set，RS）

RS 是新一代 RC，提供同样的高可用能力，区别主要在于 RS 后来居上，能支持更多种类的匹配模式。副本集对象一般不单独使用，而是作为 Deployment 的理想状态参数使用。

Replication Controller **是实现弹性伸缩、动态扩容和滚动升级的核心。**

### 部署（Deployment）

Deployment 提供了一种对 Pod 和 ReplicaSet 的管理方式，每一个 Deployment 都对应集群中的一次部署，是非常常见的 Kubernetes 对象。**用于管理 Pod 的部署和扩展**



### K8s的Service是什么？

答：Pod每次重启或者重新部署，其IP地址都会产生变化，这使得pod间通信和pod与外部通信变得困难，这时候，就需要Service为pod提供一个固定的入口。

Service的Endpoint列表通常绑定了一组相同配置的pod，通过负载均衡的方式把外界请求分配到多个pod上



#### 简述 kube-proxy ipvs 和 iptables 的异同？

iptables 与 IPVS 都是基于 Netfilter 实现的，但因为定位不同，二者有着本质的差别：**iptables 是为防火墙而设计的；IPVS 则专门用于高性能负载均衡，并使用更高效的数据结构（Hash 表），允许几乎无限的规模扩张。**

与 iptables 相比，IPVS 拥有以下明显优势：

1. 为大型集群提供了更好的可扩展性和性能；
2. 支持比 iptables 更复杂的复制均衡算法（最小负载、最少连接、加权等）；
3. 支持服务器健康检查和连接重试等功能；
4. 可以动态修改 ipset 的集合，即使 iptables 的规则正在使用这个集合。



### ingress负载均衡

**但是一般智能用于一些无状态的分发**

Ingress 是反向代理规则，用来规定 HTTP/S 请求应该被转发到哪个 Service 上，比如根据请求中不同的 Host 和 url 路径让请求落到不同的 Service 上。

### 命名空间（Namespace）

**命名空间为 Kubernetes 集群提供虚拟的隔离作用**，Kubernetes 集群初始有两个命名空间，分别是默认命名空间 default 和系统命名空间 kube-system，除此以外，管理员可以可以创建新的命名空间满足需要。

名字空间适用于存在很多跨多个团队或项目的用户的场景。对于只有几到几十个用户的集群，根本不需要创建或考虑名字空间。





## 数据持久化方案

#### EmptyDir（空目录）

没有指定要挂载宿主机上的某个目录，直接由Pod内部映射到宿主机上。类似于docker中的manager volume。

**主要使用场景**：

- 只需要临时将数据保存在磁盘上，比如在合并/排序算法中；
- **作为两个容器的共享存储**，使得第一个内容管理的容器可以将生成的数据存入其中，同时由同一个webserver容器对外提供这些页面。

**emptyDir**的**特性**：

同个pod里面的不同容器，共享同一个持久化目录，当pod节点删除时，volume的数据也会被删除。如果仅仅是容器被销毁，pod还在，则不会影响volume中的数据。

总结来说：emptyDir的数据持久化的生命周期和使用的pod一致。一般是作为临时存储使用。

#### 2）Hostpath

**将宿主机上已存在的目录或文件挂载到容器内部**。类似于docker中的bind mount挂载方式。

这种数据持久化方式，运用场景不多，因为它增加了pod与节点之间的耦合。

一般对于k8s集群本身的数据持久化和docker本身的数据持久化会使用这种方式，可以自行参考apiService的yaml文件，位于：/etc/kubernetes/main…目录下。

#### 3）PersistentVolume（简称PV）

- **PV/PVC**：PV 和 PVC 提供了一个抽象层级，**使得存储资源可以被抽象和独立于 Pod 使用。PV 和 PVC 的存在使得存储的管理更加灵活，可以动态地分配和释放存储资源。**
- **使得存储资源可以在不同的环境中进行移植和重用，而不受底层存储技术的限制。**

**基于NFS服务的PV，也可以基于GFS的PV。它的作用是统一数据持久化目录，方便管理**。

在一个PV的yaml文件中，可以对其配置PV的大小，指定PV的访问模式：

- ReadWriteOnce：只能以读写的方式挂载到单个节点；
- ReadOnlyMany：能以只读的方式挂载到多个节点；
- ReadWriteMany：能以读写的方式挂载到多个节点。以及指定pv的回收策略：
-  recycle：清除PV的数据，然后自动回收；
- Retain：需要手动回收；
- delete：删除云存储资源，云存储专用；





## 基本的hello world应用

我这里使用minikube。初步搭建一个玩玩

#### 创建一个简单的http web应用

```
kubectl create deployment hello-minikube1 --image=registry.cn-hangzhou.aliyuncs.com/google_containers/echoserver:1.10


# 也可以选择run
kubectl run hello-minikube --image=tomcat:8.0 --port=8001
```

这个会创建一个简单的提供一个hello world的web服务应用。并提供一个内部的端口

![image-20240412140417684](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/6a942e0fbd78bbacf026b27ac02bef3b/522cdda19a744e4f30963e5e4251f4ed.png)

**192这个就是k8s的内部节点ip。宿主机是不能直接curl访问的。pod的ip一般是10开的。**

**相当于在你的电脑上搭建了一个局域网，然后某个节点ip是192。**

在 Kubernetes 中，`Deployment` 和 `Run` 是两种不同的方式来管理应用程序的运行。

1. **Deployment**：
   - `Deployment` 是 Kubernetes 中用来创建和管理 Pod 的一种资源对象。
   - 通过 Deployment，你可以定义应用程序的期望状态，并让 Kubernetes 管理和保持该状态，即使在节点故障或者应用程序需要更新时也是如此。
   - Deployment 提供了滚动更新和回滚功能，使得你可以方便地进行应用程序的版本管理。
   - 通常，建议使用 Deployment 来管理长期运行的应用程序。
2. **Run**：
   - `Run` 是 Kubernetes 提供的一种快速创建 Pod 的命令行工具，用于快速部署容器。
   - 通过 `kubectl run` 命令，你可以快速创建一个 Pod，并指定容器镜像和其他配置参数。
   - `Run` 创建的 Pod 没有复杂的控制器或者管理功能，它们只是简单地创建并运行，不会进行自动的故障恢复或者滚动更新。
   - `Run` 主要用于临时任务、快速测试或者一次性作业。



#### 暴露端口

```
kubectl expose deployment hello-minikube1 --type=LoadBalancer --port=8000
```

然后就可以通过**宿主机ip：8000** 端口访问了







### 介绍K8S的服务暴露方式



##### ClusterIP

默认的，仅在集群内可用

##### NodePort

暴露端口到节点，提供了集群外部访问的入口
端口范围固定 30000 ~ 32767

##### LoadBalancer

需要负载均衡器（通常都需要云服务商提供，裸机可以安装 [METALLB](https://metallb.universe.tf/) 测试）
会额外生成一个 IP 对外服务
K8S 支持的负载均衡器：[负载均衡器](https://kubernetes.io/zh/docs/concepts/services-networking/service/#internal-load-balancer)



## 配置文件使用









当编写 YAML 文件时，对于不同的 Kubernetes 资源种类（kind），你需要根据其特定的规范来填写字段。下面是一些常见 Kubernetes 资源种类的示例 YAML 文件：

### pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test-container
      image: ccr.ccs.tencentyun.com/k8s-tutorial/test-k8s:v1

```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: test-container
        image: ccr.ccs.tencentyun.com/k8s-tutorial/test-k8s:v1 # 开启一个8080的web页面
```

通过exec进入pod容器内部访问目标端口

```
服务的默认类型是ClusterIP，只能在集群内部访问，我们可以进入到 Pod 里面访问：
kubectl exec -it pod-name -- bash
```

![image-20240413191151261](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/6a942e0fbd78bbacf026b27ac02bef3b/dd2639162ad1bb2ffa4ce6f3e75e43e4.png)



### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-service
spec:
  selector:
    app: test-app
  type: NodePort # 默认是ClusterIP， 只有集群内部才能访问。我们可以使用NodePort和Loadbalancer 让外部访问

  ports:
    - port: 8080        # 本 Service 的端口
      targetPort: 8080  # 容器端口
      nodePort: 31000   # 节点端口，范围固定 30000 ~ 32767, 暴露给外部的node:ip
```

> **注意！！！：如果你是用 minikube，因为是模拟集群，你的电脑并不是节点，节点是 minikube 模拟出来的，所以你并不能直接在电脑上访问到服务**
>
> 要先获取node的ip。
>
> ```
> ❯ minikube ip
> 192.168.49.2
> 
> # 注意，ubuntu上可以直接访问，但是我的mac上node有防火墙（好像是路由不对，反正不行），只有进入容器内部能够直接访问，应该线进入node内部关闭防火墙，或者直接进入节点内部查看端口是否开启了相关服务
> ❯ curl 192.168.49.2:31000
> index page 
> 
> IP lo10.244.0.12, hostname: test-deployment-84757bcf57-nmfts
> ```

### ConfigMap

**ConfigMap 用于存储非敏感的配置数据**，例如应用程序的配置文件、环境变量、命令行参数等。

**config map 不支持热加载**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-config
data:
  key1: value1
  key2: value2
```

**可以直接用于生成pod环境变量，也可以挂载为数据卷**

```
# 启动配置
kubectl apply -f test-configmap.yaml
# 重新加载所有pod
ubectl delete -f test-deployment.yaml
kubectl apply -f test-deployment.yaml
```



只需要在pod配置加上

```
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: mycontainer
      image: myimage
      envFrom:
        - configMapRef:
            name: my-config
```

**结果**

![image-20240414164048526](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/6a942e0fbd78bbacf026b27ac02bef3b/97ef58e1c2455b172a40bf37ec99de16.png)



### Secret

**用于存储敏感的配置数据，例如密码、证书、API 密钥等。**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: test-secret
type: Opaque
data:
  username: <base64-encoded-username>
  password: <base64-encoded-password>
```

### PersistentVolume

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /data
```

### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: test-namespace
```

这些示例可以作为你编写 YAML 文件时的参考。记住根据你的需求调整各个字段。



## 常见命令



以下是一些常用的 kubectl 命令：

1. **查看资源列表**：
   ```bash
   kubectl get pods # 查看 Pod 列表
   kubectl get deployments # 查看 Deployment 列表
   kubectl get services # 查看 Service 列表
   kubectl get configmaps # 查看 ConfigMap 列表
   kubectl get secrets # 查看 Secret 列表
   kubectl get namespaces # 查看 Namespace 列表
   ```

2. **查看资源详细信息**：
   ```bash
   kubectl describe pod <pod-name> # 查看 Pod 的详细信息
   kubectl describe deployment <deployment-name> # 查看 Deployment 的详细信息
   kubectl describe service <service-name> # 查看 Service 的详细信息
   ```

3. **创建资源**：
   ```bash
   kubectl create -f <yaml-file> # 从 YAML 文件创建资源
   kubectl apply -f <yaml-file> # 应用 YAML 文件中定义的配置（支持创建和更新）
   ```

4. **删除资源**：
   
   ```bash
   kubectl delete pod <pod-name> # 删除 Pod
   kubectl delete deployment <deployment-name> # 删除 Deployment
   kubectl delete service <service-name> # 删除 Service
   ```
   
5. **修改资源**：
   ```bash
   kubectl edit pod <pod-name> # 编辑 Pod 配置
   kubectl edit deployment <deployment-name> # 编辑 Deployment 配置
   ```

6. **执行命令**：
   ```bash
   kubectl exec -it <pod-name> -- <command> # 在 Pod 中执行命令
   ```

7. **日志查看**：
   ```bash
   kubectl logs <pod-name> # 查看 Pod 日志
   ```

8. **管理命名空间**：
   ```bash
   kubectl create namespace <namespace-name> # 创建命名空间
   kubectl delete namespace <namespace-name> # 删除命名空间及其所有资源
   ```

9. **设置上下文**：
   ```bash
   kubectl config get-contexts # 查看可用上下文
   kubectl config use-context <context-name> # 切换上下文
   ```

10. **其他**：
    ```bash
    kubectl apply -f <directory> # 应用目录中所有 YAML 文件
    kubectl get events # 查看集群事件
    kubectl version # 查看 Kubernetes 版本信息
    ```

这些是一些基本的 kubectl 命令，可以帮助你管理 Kubernetes 集群中的资源。











## minikube使用



1. **启动 Minikube 集群**：使用 Minikube 命令启动一个新的 Minikube 集群，并指定你想要的节点数量。例如，要创建一个具有 3 个节点的集群，可以使用以下命令：

   ```
   minikube start --nodes=3
   ```

2. **等待集群启动**：等待 Minikube 集群启动完成。这可能需要一些时间，取决于你的计算机性能和网络状况。

3. **验证节点**：一旦集群启动完成，你可以使用 `kubectl get nodes` 命令来验证集群中的节点数量。

   ```
   kubectl get nodes
   ```

4. 停止节点

   ```
   # 启动集群
   minikube start
   
   # 停止集群
   minikube stop
   
   # 清空集群
   minikube delete --all
   ```

5. 添加节点

   ```
   -p 指定的目标集群，默认集群叫做minikube，可以通过`minikube profile list`查看
   
   minikube start -p minikube #创建主集群
   minikube node add -p minikube #增加节点
   minikube node list -p minikube #查看节点
   minikube dashboard -p minikube #启动主节点仪表盘
   ```

   **进入相关节点.**

   注意：minikube不同node之间是相互通信的。

   ````
   Minikube 常用命令
   进入节点服务器：
   
   
   minikube ssh
   执行节点服务器命令，例如查看节点 docker info：
   使用，查看当且节点列表
   ```
   ❯ kubectl get nodes
   NAME           STATUS   ROLES           AGE   VERSION
   minikube       Ready    control-plane   31h   v1.28.3
   minikube-m02   Ready    <none>          16m   v1.28.3 # 登录从节点
   ```
   连接从节点
   ```
   ❯ minikube ssh --node=minikube-m02
   ```
   
   
   
   minikube ssh -- docker info
   删除集群, 删除 ~/.minikube 目录缓存的文件：
   
   minikube delete
   关闭集群：
   
   minikube stop
   销毁集群：
   
   minikube stop && minikube delete
   ````

   

6. 宿主机转发 dashboard

   ```
   nohup minikube dashboard & # 后台开启管理面板
   
   kubectl proxy --port=10080 --address='10.20.208.22' --accept-hosts='^.*' # 启动宿主机转发到面板
   
   --port 需要暴露的端口号
   --address 服务器外网IP（宿主机IP）
   
   --accept-hosts 外部访问服务器的IP（白名单）
   然后就可以访问了
   
   http://10.20.208.22:10082/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/workloads?namespace=default
   ```

   

7. 其他

   ```
   # 安装集群可视化 Web UI 控制台
   minikube dashboard
   
   # 在浏览器自动打开应用
   minikube sercive 服务的名字
   
   查看内置的附加组件
   minikube addons list
   ```




## pod 通信

### **同一个POD上Container通信**

在k8s中每个Pod中管理着一组Docker容器，**这些Docker容器共享同一个网络命名空间**，Pod中的每个Docker容器拥有与Pod相同的IP和port地址空间，并且由于他们在同一个网络命名空间，**他们之间可以通过localhost相互访问。**

**什么机制让同一个Pod内的多个docker容器相互通信?就是使用Docker的一种网络模型：–net=container**

### **同一个Node，不同Pod**

**同一个node内部的pod之间，可以直接使用pod的10开的ip直接通信。** 

![Kubernetes之POD、容器之间的网络通信](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/6a942e0fbd78bbacf026b27ac02bef3b/781eaaa73ce58d43abedc39285678487.png)



### 不同node的pod通信

可以考虑通过service来实现不同node之间的服务通信。

**方法一：Service 抽象**：Kubernetes 中的 **Service 为一组执行相同功能的 Pods 提供一个稳定的访问地址。即使后端 Pod 发生变化，Service 的 IP 和端口保持不变。**如果pod变化了，service也会自动变化

- 当一个 Pod 尝试连接到另一个 Service 时，它实际上是连接到一个固定的虚拟 IP（即 Service IP），这个 IP 是由集群内部 DNS 服务解析的。这个请求被 kube-proxy 捕获并重定向到正确的 Pod。

**方法二：使用CNI 插件**

- **Calico**：提供高性能网络和网络策略。Calico 通过使用 BGP (Border Gateway Protocol) 或封装模式（如 VXLAN）来管理跨节点的网络流量。







## pod 的分配

一般默认是均匀分配到所有节点



## 将 Pod 指派给节点

可以通过亲和性来实现分配给指定节点，具体来说，依赖的是lable标签的办法来指定节点。





## 为什么有了容器还需要Pod：

- **多容器协同**：Pod可以包含多个容器，这些**容器可以共享相同的网络、存储等资源**，方便多容器之间的协同工作。
- **资源共享**：Pod中的容器可以共享相同的网络命名空间、IPC命名空间和存储卷，方便它们之间进行通信和共享数据。
- **扩展性和灵活性**：Pod可以方便地扩展为多容器架构，从而实现更灵活的部署和管理。





