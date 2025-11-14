# 大模型自部署调查


# 自部署并发调查

由于我们的模型可能需要用到自己的第三方模型，因此需要自己部署。

一个是自己部署，自己维护可靠性，在一站式不成熟的情况下，避免和第三方公用资源。

优点如下：

- 无审核
- 纯自用，私密性
- 当主模型宕机，可以部分顶上



# 短期测试

**Ollama进行了v0.1.33版本更新，为本地部署的开源大型语言模型（LLMs）带来了重大改进。现在，多用户可以在同一台宿主机上与LLMs进行互动，实现同时聊天对话。**

**Linux为例**

1. 通过调用 编辑 systemd 服务systemctleditollama.service 这将打开一个编辑器。
2. Environment对于每个环境变量，在部分下添加一行`[Service]`：



```
#示例[Service]Environment="OLLAMA_HOST=0.0.0.0" #设置服务监听的主机地址Environment="OLLAMA_NUM_PARALLEL=4" #并行处理请求的数量Environment="OLLAMA_MAX_LOADED_MODELS=4" #同时加载的模型数量
```

3. 保存并退出。
4. 重新加载systemd并重新启动 Olama：

```
sudo systemctl daemon-reloadsudo systemctl restart ollama
```

tips：以上的变量值官方给出为4，并没有详细说明最大可以设置到多少





# 业界

前已经有不少框架支持了大模型的分布式部署，可以并行的提高推理速度。不光可以单机多卡，还可以多机多卡。
我自己没啥使用经验，简单罗列下给自己备查。不足之处，欢迎在评论区指出。

| 框架名称          | 出品方                | 开源地址                                                     |
| ----------------- | --------------------- | ------------------------------------------------------------ |
| FasterTranaformer | 英伟达                | [FasterTransformer github](https://github.com/NVIDIA/FasterTransformer) |
| TGI               | huggingface           | [huggingface/text-generation-inference](https://github.com/huggingface/text-generation-inference) |
| vLLM              | 伯克利大学 LMSYS 组织 | [github-vllm](https://github.com/vllm-project/vllm)          |
| deepspeed         | 微软                  | [github.com/microsoft/DeepSpeed](https://github.com/microsoft/DeepSpeed) |
| lmdeploy          | open-mmlab            | [InternLM/lmdeploy](https://github.com/InternLM/lmdeploy)    |
| TurboTransformers | 腾讯                  | [Tencent/TurboTransformers](https://github.com/Tencent/TurboTransformers) |

**faster transformer是英伟达的大模型推理方案，但是后续可能不再维护，因为英伟达推出了一个更新的框架TensorRT-LLM，它目前还在申请使用阶段，未来应该会全面开源吧。**



## case

**tensort+trition**是一套比较成熟的方案。







# 并发原理

并不是减少模型显存占用，而是在不减少模型显存占用的情况下，增加并发量

[基于vLLM加速大模型推理并评估性能 | Quantum Bit](https://www.eula.club/blogs/%E5%9F%BA%E4%BA%8EvLLM%E5%8A%A0%E9%80%9F%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86%E5%B9%B6%E8%AF%84%E4%BC%B0%E6%80%A7%E8%83%BD.html#_1-%E6%8E%A8%E7%90%86%E6%9C%8D%E5%8A%A1%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96)

# VLLM原理（讲得不错，建议多看看）



[LLM 大模型学习必知必会系列(十二)：VLLM性能飞跃部署实践：从推理加速到高效部署的全方位优化[更多内容：XInference/FastChat等框架] - 汀、人工智能 - 博客园](https://www.cnblogs.com/ting1/p/18225409)



## 推理的性能瓶颈

[[译] 大模型推理的极限：理论分析、数学建模与 CPU/GPU 实测（2024）](https://arthurchiao.art/blog/llm-inference-speed-zh/)

**作者发现大模型推理的性能瓶颈主要来自于内存。**一是自回归过程中缓存的K和V张量非常大，在LLaMA-13B中，单个序列输入进来需要占用1.7GB内存。二是内存占用是动态的，取决于输入序列的长度。由于碎片化和过度预留，现有的系统浪费了60%-80%的内存。

**并行情况下，算力也很容易成为瓶颈**







# 一些说明

## 并发一定需要多卡吗，VLLM哪怕并发上去了，速度也很快

不一定，单卡设置batch也可以





# 关于一些特殊型号的显卡

**可以考虑转化为onnx格式的模型来通知执行**



# ref

[TensorRT踩坑教程 - 银河渡舟](https://suborbit.net/posts/tensorrt-tutorial/)

[FeiGeChuanShu/trt2023: NVIDIA TensorRT Hackathon 2023复赛选题：通义千问Qwen-7B用TensorRT-LLM模型搭建及优化](https://github.com/FeiGeChuanShu/trt2023)

[TensorRT&Triton学习笔记(一)：triton和模型部署+client-CSDN博客](https://blog.csdn.net/sgyuanshi/article/details/123536579)



[ollama 支持并发之后和 vllm 相比性能如何？我们测测看_ollama vllm-CSDN博客](https://blog.csdn.net/arkohut/article/details/139076652) 

[自部署trition样例](https://iwiki.woa.com/p/4008548715?from=km_search)

[ollama vs vllm - 开启并发之后的 ollama 和 vllm 相比怎么样？_哔哩哔哩_bilibili ](https://www.bilibili.com/video/BV1Bw4m1D7K3/?vd_source=56312c73bc0637fc9a7e871063e28f0f)**单卡4090**


