# 大模型system Prompt为什么重要




# 背景

一直知道这玩意儿，也知道一部分其底层原理，但是没有实际深究过，决定mark一下。









## 大模型的记忆原理

从计算机科学的角度来看，最好**将LLM的推理过程视为无状态函数调用——给定输入文本，它会输出接下来应该做什么。**

大模型本身是没有记忆的，其之所以体验有记忆，本质上是：**用户每次提出一个问题时，模型收到的提示都会包含之前所有的对话内容，这些提示就是我们经常说的“上下文”。**







# 一个解释

本质上来说，system prompt也只不过是加了一个分割得token来和user prompt放在一起，直接写在user prompt是没有本质区别的。

![refs/heads/master/image-20240814200222542](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/b03a509485115100b891e5eeb8634fc7/cbdd56239bd34b020c0cb0702afa92c9.png)



![refs/heads/master/image-20240814200229217](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/b03a509485115100b891e5eeb8634fc7/bd8fd894bed17527f0e95a3813aa8357.png)







但是：理论上来说，没有区别。LLM 得到的只是一堆文本，不管是你自己输入的所有内容，还是前端自动添加的某些部分。

**话虽如此，格式很重要，不使用模型训练的格式可能会带来不利影响**。因此，最好让前端处理复杂的提示。



# 实际测试

感觉直接写到user prompt里面区别不大，基本都能work。





# ref

[可能对你有帮助的五个ChatGPT自定义Prompt - 大模型知识库|大模型训练|开箱即用的企业大模型应用平台|智能体开发|53AI](https://www.53ai.com/news/qianyanjishu/2024062652170.html)

[系统提示和用户提示有什么区别？：r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1cj4bfw/difference_between_system_prompt_and_user_prompt/)

