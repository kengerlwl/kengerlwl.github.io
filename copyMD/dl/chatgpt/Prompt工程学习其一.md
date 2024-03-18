---
title: Prompt工程学习其一
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-7 15:27:31
password:
summary:
tags:
- prompt
categories:
- 学术
---


# 常见术语科普

## Zero-shot 、One-shot 、Few-shot Learning 简介与应用

由于LLM具有较强的跨领域泛化能力，所以可以很好的适用于这些学习方式，也就是说少量case案例的模式。

### Zero-shot Learning

**在训练集中没有某个类别的样本，但是在测试集中出现了这个类别**，那么我们就需要模型在训练过程中，即使没有接触过这个类别的样本，但是仍然**可以通过对于这个类别的描述，对没见过的类别进行分类**，目的是**让模型对于要分类的样本一次也不学习的同时具有人类的推理能力。**

例：**假设我们的模型已经能够识别马，老虎和熊猫了，现在需要该模型也识别斑马**，那么我们需要告诉模型，怎样的对象才是斑马，但是并不能直接让模型看见斑马。



### Few-shot Learning

在模型训练过程中，如果每个类别只有少量样本（一个或者几个），研究人员希望机器学习模型在学习了一定类别的大量数据后，对于新的类别，**只需要少量的样本就能快速学习，这就是 Few-shot Learning 要解决的问题**。few-shot learning是meta-learning的一种，本质上是让机器学会自己学习（learn to learn），**其实就是通过判断测试样本与训练样本的相似性，来推测测试样本属于什么类。**

**学习的目的是理解事物之间的不同，学会区分不同事物。给两张图像，不让学会是什么，而是学会是否相同。**

### One-shot Learning是Few-shot Learning的一种特殊情况











# 编写Prompt的基本原则



## 1 编写清晰、具体的指令

使用分隔符将一些内容和要求分割开

````
请把以下用```分割的内容精简一下
```
xxx
```
````



### 1.1 对于一些总结性的，请给出结构化输出

```
prompt = f"""
请生成包括书名、作者和类别的三本虚构书籍清单，\
并以 JSON 格式提供，其中包含以下键:book_id、title、author、genre。
"""
response = get_completion(prompt)
print(response)

```



### 1.2 在Prompt中可以设置判断条件

如果该文本不符合我的要求，可以输出不符合要求

```
# 有步骤的文本
text_1 = f"""
泡一杯茶很容易。首先，需要把水烧开。\
在等待期间，拿一个杯子并把茶包放进去。\
一旦水足够热，就把它倒在茶包上。\
等待一会儿，让茶叶浸泡。几分钟后，取出茶包。\
如果你愿意，可以加一些糖或牛奶调味。\
就这样，你可以享受一杯美味的茶了。
"""
prompt = f"""
您将获得由三个引号括起来的文本。\
如果它包含一系列的指令，则需要按照以下格式重新编写这些指令：

第一步 - ...
第二步 - …
…
第N步 - …

如果文本中不包含一系列的指令，则直接写“未提供步骤”。"
\"\"\"{text_1}\"\"\"
"""
response = get_completion(prompt)
print("Text 1 的总结:")
print(response)
```



### 1.3 提供一定的案例 few shot

```
prompt = f"""
你的任务是以一致的风格回答问题。

<孩子>: 教我耐心。

<祖父母>: 挖出最深峡谷的河流源于一处不起眼的泉眼；最宏伟的交响乐从单一的音符开始；最复杂的挂毯以一根孤独的线开始编织。

<孩子>: 教我韧性。
"""
response = get_completion(prompt)
print(response)
```





## 2 分步骤让模型思考

chatgpt等人工智能模型的推理能力不能说没有，只能说基本为0.很低，不能独立的完成一些逻辑性强或者复杂的任务，对于这种任务，可以适当的选择分步骤来让chatgpt一步步完成。

```
text = f"""
在一个迷人的村庄里，兄妹杰克和吉尔出发去一个山顶井里打水。\
他们一边唱着欢乐的歌，一边往上爬，\
然而不幸降临——杰克绊了一块石头，从山上滚了下来，吉尔紧随其后。\
虽然略有些摔伤，但他们还是回到了温馨的家中。\
尽管出了这样的意外，他们的冒险精神依然没有减弱，继续充满愉悦地探索。
"""
# example 1
prompt_1 = f"""
执行以下操作：
1-用一句话概括下面用三个反引号括起来的文本。
2-将摘要翻译成法语。
3-在法语摘要中列出每个人名。
4-输出一个 JSON 对象，其中包含以下键：French_summary，num_names。

请用换行符分隔您的答案。

Text:
```{text}```
"""
response = get_completion(prompt_1)
print("prompt 1:")
print(response)
```







# 应用



## prompt文本摘要生成

对一段文本内容进行浓缩也是常见的工作，方便快速掌握文本中我们所需要的信息

```
prompt = f"""
你的任务是从电子商务网站上生成一个产品评论的简短摘要。

请对三个反引号之间的评论文本进行概括，最多30个词汇，并且聚焦在产品运输上。

评论: ```{prod_review_zh}```
"""

response = get_completion(prompt)
print(response)
```





## 文本情感识别

```
prompt = f"""
以下用三个反引号分隔的产品评论的情感是什么？

用一个单词回答：「正面」或「负面」。

评论文本: ```{lamp_review_zh}```
"""
response = get_completion(prompt)
print(response)
```



## 实体识别

```
# 中文
lamp_review_zh = """
我需要一盏漂亮的卧室灯，这款灯具有额外的储物功能，价格也不算太高。\
我很快就收到了它。在运输过程中，我们的灯绳断了，但是公司很乐意寄送了一个新的。\
几天后就收到了。这款灯很容易组装。我发现少了一个零件，于是联系了他们的客服，他们很快就给我寄来了缺失的零件！\
在我看来，Lumina 是一家非常关心顾客和产品的优秀公司！
"""

prompt = f"""
从评论文本中识别以下项目：
- 评论者购买的物品
- 制造该物品的公司

评论文本用三个反引号分隔。将你的响应格式化为以 “物品” 和 “品牌” 为键的 JSON 对象。
如果信息不存在，请使用 “未知” 作为值。
让你的回应尽可能简短。
  
评论文本: ```{lamp_review_zh}```
"""
response = get_completion(prompt)
print(response)
```



## 主题提取

理论上也可以提前给定几个我想要设定的主题，然后让LLM判断该文本是否符合该主题，给出0/1

```
# 中文
story_zh = """
在政府最近进行的一项调查中，要求公共部门的员工对他们所在部门的满意度进行评分。
调查结果显示，NASA 是最受欢迎的部门，满意度为 95％。

一位 NASA 员工 John Smith 对这一发现发表了评论，他表示：
“我对 NASA 排名第一并不感到惊讶。这是一个与了不起的人们和令人难以置信的机会共事的好地方。我为成为这样一个创新组织的一员感到自豪。”

NASA 的管理团队也对这一结果表示欢迎，主管 Tom Johnson 表示：
“我们很高兴听到我们的员工对 NASA 的工作感到满意。
我们拥有一支才华横溢、忠诚敬业的团队，他们为实现我们的目标不懈努力，看到他们的辛勤工作得到回报是太棒了。”

调查还显示，社会保障管理局的满意度最低，只有 45％的员工表示他们对工作满意。
政府承诺解决调查中员工提出的问题，并努力提高所有部门的工作满意度。
"""


# 中文
prompt = f"""
确定以下给定文本中讨论的五个主题。

每个主题用1-2个单词概括。

输出时用逗号分割每个主题。

给定文本: ```{story_zh}```
"""
response = get_completion(prompt)
print(response)

```



## 文本转换，基本文字处理

LLM非常擅长将输入转换成不同的格式，例如**多语种文本翻译、拼写及语法纠正、语气调整、格式转换等。**

我常用格式转换



## 语气风格调整

```
prompt = f"""
将以下文本翻译成商务信函的格式: 
```小老弟，我小羊，上回你说咱部门要采购的显示器是多少寸来着？```
"""
response = get_completion(prompt)
print(response)
```



## 格式转换

```
data_json = { "resturant employees" :[ 
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
]}
prompt = f"""
将以下Python字典从JSON转换为命令行的pd表格，保留表格标题和列名：{data_json}
"""
response = get_completion(prompt)
print(response)
```



## 文本效验

```
text = f"""
Got this for my daughter for her birthday cuz she keeps taking \
mine from my room.  Yes, adults also like pandas too.  She takes \
it everywhere with her, and it's super soft and cute.  One of the \
ears is a bit lower than the other, and I don't think that was \
designed to be asymmetrical. It's a bit small for what I paid for it \
though. I think there might be other options that are bigger for \
the same price.  It arrived a day earlier than expected, so I got \
to play with it myself before I gave it to my daughter.
"""
prompt = f"""
针对以下三个反引号之间的英文评论文本，
首先进行拼写及语法纠错，
然后将其转化成中文，
再将其转化成优质淘宝评论的风格，从各种角度出发，分别说明产品的优点与缺点，并进行总结。
润色一下描述，使评论更具有吸引力。
输出结果格式为：
【优点】xxx
【缺点】xxx
【总结】xxx
注意，只需填写xxx部分，并分段输出。
将结果输出成Markdown格式。
```{text}```
"""
response = get_completion(prompt)
display(Markdown(response))
```



## 文本扩展（废话生成器）

关键点说明：

```
你是一名客户服务的AI助手。
你的任务是给一位重要的客户发送邮件回复。
根据通过“```”分隔的客户电子邮件生成回复，以感谢客户的评价。
如果情感是积极的或中性的，感谢他们的评价。
如果情感是消极的，道歉并建议他们联系客户服务。
请确保使用评论中的具体细节。
以简明和专业的语气写信。
以“AI客户代理”的名义签署电子邮件。
```

- 身份设定：你是xxx
- 目标设定：你的任务是x'x，请帮我xx
- 设定细节
  - 具体要求如：
  - 1,2,3



```
# given the sentiment from the lesson on "inferring",
# and the original customer message, customize the email
sentiment = "negative"

# review for a blender
review = f"""
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""


prompt = f"""
你是一名客户服务的AI助手。
你的任务是给一位重要的客户发送邮件回复。
根据通过“```”分隔的客户电子邮件生成回复，以感谢客户的评价。
如果情感是积极的或中性的，感谢他们的评价。
如果情感是消极的，道歉并建议他们联系客户服务。
请确保使用评论中的具体细节。
以简明和专业的语气写信。
以“AI客户代理”的名义签署电子邮件。
客户评价：```{review}```
评论情感：{sentiment}
"""
response = get_completion(prompt, temperature=0.7)
print(response)
```

