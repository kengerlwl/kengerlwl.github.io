---
title: langchain使用入门指北
top: false
cover: false
toc: true
mathjax: true
date: 2024-08-05 15:27:31
password:
summary:
tags:
- langchain
- llm
categories:
- 学术
---
# 背景

需要用ai来实现提效。

```
【业务背景】针对运维开发中的业务问题引入LLM进行提效，实现自动化，智能化解决运维问题，面向用户是运维小组以及开发小组

【检索系统】基于ES和向量数据库实现多路召回检索，基于文档特性编写分割代码，从标题层级+语义两方面进行文档分割。引入父文档召回，文档打分重写机制

【知识问答】通过LLM语义判断过滤低质量文档，基于LLM引入思维链提高问答准确性，并兼容通用问题回答。

【业务接入】基于langchain接入具体业务代码，不同服务间基于trpc互相调用。引入多轮对话机制实现参数缺失补全

【模型微调】针对垂直领域，进行模型微调，SFT（终），LORA。构建垂直领域数据集，进行混元以及千问大模型微调。基于trition自部署大模型

【产品能效】得到总监和leader的一致认可，在公司中心试点运行。日活用户xx，最高qpsxxx
```



# chain



## demo chain

一个最简单的chain

```
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from LLM.Models import *

llm = HunyuanLLM()

prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain only specifying the input variable.
print(chain.run({"product": "pizza"}))
```



## Router Chain

**本笔记本演示了如何使用 `RouterChain` 范例来创建一个根据给定输入动态选择下一个链条的链条。**

路由器链条由两个组件组成:

- **RouterChain (负责选择下一个要调用的链条)，可以通过LLM语义来实现路由选择下一个chain**
- destination_chains: 路由器链条可以路由到的链条

[Langchain Chain - RouterChain 根据输入相关性进行路由的路由链_langchain routerchain-CSDN博客](https://blog.csdn.net/javastart/article/details/133881916)







## 顺序（Sequential）

顺序链允许您连接多个链并将它们组合成执行某个特定场景的管道。有两种类型的顺序链：

- `SimpleSequentialChain`：最简单的顺序链形式，每个步骤都有一个单一的输入/输出，一个步骤的输出是下一个步骤的输入。
- `SequentialChain`：更一般的顺序链形式，允许多个输入/输出。









# agent

## agent

**在langchain里面的agent本质上是一个tool选择器。**

**其plan函数来实现选择执行哪个tool。**







## agent执行器

[下一个平台Agent | 李乾坤的博客](https://qiankunli.github.io/2023/10/30/llm_agent.html)



下面这个图，**就展现出了 Agent 接到任务之后，自动进行推理，然后自主调用工具完成任务的过程。**

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/6fa9f6cffd328121122ebd7ec8ec7b85/ef8c5671e2853378b78d1346f8927a2e.jpg?wh=10666x5260)

那么，你看 LangChain，乃至整个大模型应用开发的核心理念就呼之欲出了。这个核心理念就是**操作的序列并非硬编码在代码中，而是使用语言模型（如 GPT-3 或 GPT-4）来选择执行的操作序列**。





**AgentExecutor由一个Agent和Tool的集合组成。AgentExecutor负责调用Agent，获取返回（callback）、action和action_input，并根据意图将action_input给到具体调用的Tool，获取Tool的输出，并将所有的信息传递回Agent，以便猜测出下一步需要执行的操作。`AgentExecutor.run也就是chain.run ==> AgentExecutor/chain.__call__ ==> AgentExecutor._call()` 和逻辑是 _call 方法，核心是 `output = agent.plan(); tool=xx(output); observation = tool.run();**

```
def initialize_agent(tools,llm,...)-> AgentExecutor:
    agent_obj = agent_cls.from_llm_and_tools(llm, tools, callback_manager=callback_manager, **agent_kwargs)
    AgentExecutor.from_agent_and_tools(agent=agent_obj, tools=tools,...)
    return cls(agent=agent, tools=tools, callback_manager=callback_manager, **kwargs)
# AgentExecutor 实际上是一个 Chain，可以通过 .run() 或者 _call() 来调用
class AgentExecutor(Chain):
    agent: Union[BaseSingleActionAgent, BaseMultiActionAgent]
    tools: Sequence[BaseTool]
    """Whether to return the agent's trajectory of intermediate steps at the end in addition to the final output."""
    max_iterations: Optional[int] = 15
    def _call(self,inputs: Dict[str, str],...) -> Dict[str, Any]:
        while self._should_continue(iterations, time_elapsed):
            next_step_output = self._take_next_step(name_to_tool_map,inputs,intermediate_steps,...)
            # 返回的数据是一个AgentFinish类型，表示COT认为不需要继续思考，当前结果就是最终结果，直接将结果返回给用户即可；
            if isinstance(next_step_output, AgentFinish):
                return self._return(next_step_output, intermediate_steps, run_manager=run_manager)
            if len(next_step_output) == 1:
                next_step_action = next_step_output[0]
                # See if tool should return directly
                tool_return = self._get_tool_return(next_step_action)
                if tool_return is not None:
                    return self._return(tool_return, intermediate_steps, run_manager=run_manager)
            iterations += 1
            time_elapsed = time.time() - start_time
        return self._return(output, intermediate_steps, run_manager=run_manager)          
    def _take_next_step(...):
        # 调用LLM决定下一步的执行逻辑
        output = self.agent.plan(intermediate_steps,**inputs,...)
        if isinstance(output, AgentFinish): # 如果返回结果是AgentFinish就直接返回
            return output
        if isinstance(output, AgentAction): # 如果返回结果是AgentAction，就根据action调用配置的tool
            actions = [output]
        result = []
        for agent_action in actions:
            tool = name_to_tool_map[agent_action.tool]
            observation = tool.run(agent_action.tool_input,...)
            result.append((agent_action, observation))  # 调用LLM返回的AgentAction和调用tool返回的结果（Obversation）一起加入到结果中
        return result
```

![refs/heads/master/image-20240807153658974](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/6fa9f6cffd328121122ebd7ec8ec7b85/d273d0b7ce818fb0c729db5e2204300b.png)









## agent type



这段代码定义了一个名为 `AgentType` 的枚举类，使用了 Python 的 `Enum` 模块。这个枚举类用于表示不同类型的智能代理（agent），每种类型的代理都有其特定的功能和用途。下面是对每个代理类型的详细解释：

1. **ZERO_SHOT_REACT_DESCRIPTION**:
   - 描述：这是一个零-shot（零样本）代理，它在采取行动之前会进行推理步骤。(**不支持工具参数的多输入**)
   - 用途：适用于不需要先前示例的情况下进行推理和决策的场景。

2. **REACT_DOCSTORE**:
   - 描述：同样是一个零-shot代理，但它可以访问一个文档存储库，以查找与问题相关的信息。
   - 用途：适合需要从文档中获取信息以回答问题的场景。

3. **SELF_ASK_WITH_SEARCH**:
   - 描述：这个代理会将复杂问题分解为一系列更简单的问题，并使用搜索工具查找这些简单问题的答案，以最终回答原始复杂问题。
   - 用途：适合处理复杂问题时需要逐步推理的场景。

4. **CONVERSATIONAL_REACT_DESCRIPTION**:
   - 描述：这是一个用于对话的零-shot代理，进行推理后采取行动。
   - 用途：适合需要在对话中进行推理和响应的场景。

5. **CHAT_ZERO_SHOT_REACT_DESCRIPTION**:
   - 描述：与 `ZERO_SHOT_REACT_DESCRIPTION` 类似，但专为聊天场景设计。
   - 用途：适合在聊天环境中进行推理和响应的场景。

6. **CHAT_CONVERSATIONAL_REACT_DESCRIPTION**:
   - 描述：用于对话的代理，具体功能未详细说明。
   - 用途：适合在对话中进行交互的场景。

7. **STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION**:
   - 描述：**一个优化用于聊天模型的零-shot反应代理，能够调用具有多个输入的工具。**
   - 用途：适合需要处理复杂输入的聊天场景。

8. **OPENAI_FUNCTIONS**:
   1. **这个是 LangChain对 [OpenAI Function Call](https://platform.openai.com/docs/guides/gpt/function-calling) 的封装**。关于 Function Calling的能力，可以看我这篇文章：[OpenAI Function Calling 特性有什么用](https://liduos.com/openai-function-call-how-work.html)
   2. 描述：一个优化用于使用 OpenAI 函数的代理。
   3. 用途：适合需要调用 OpenAI 提供的功能的场景。

9. **OPENAI_MULTI_FUNCTIONS**:
   - 描述：一个优化用于使用多个 OpenAI 函数的代理。
   - 用途：适合需要同时调用多个 OpenAI 功能的场景。

总的来说，这个枚举类为不同类型的智能代理提供了清晰的分类和描述，便于开发者在使用时选择合适的代理类型。







# ref

[LangChain Agent执行原理分析-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2286923)

[Langchain Chain - RouterChain 根据输入相关性进行路由的路由链_langchain routerchain-CSDN博客](https://blog.csdn.net/javastart/article/details/133881916)
