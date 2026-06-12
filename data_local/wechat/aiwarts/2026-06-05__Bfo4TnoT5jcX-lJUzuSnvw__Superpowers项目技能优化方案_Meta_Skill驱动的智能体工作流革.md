---
title: "Superpowers项目技能优化方案：Meta Skill驱动的智能体工作流革新"
channel: wechat
src_id: aiwarts
item_id: Bfo4TnoT5jcX-lJUzuSnvw
source_url: https://mp.weixin.qq.com/s/Bfo4TnoT5jcX-lJUzuSnvw
note_id: 1912591346490475064
task_id: 6a2b8ec94f25f709ed3b702a
task_elapsed: 60
fetched_at: 2026-06-12T04:45:58.557878+00:00
summary_len: 3098
body_len: 6786
---

# Superpowers项目技能优化方案：Meta Skill驱动的智能体工作流革新

> 原文: https://mp.weixin.qq.com/s/Bfo4TnoT5jcX-lJUzuSnvw

## AI 总结

### **📌 项目背景与核心问题**

**Superpowers项目概况**
- **GitHub数据**：当前**218k Star**（三个月内从10万翻倍），825 Watch，19.4k Fork，最新版本v5.1.0（2026年5月5日发布）。
- **核心功能**：提供14个开发相关**Skill**（技能），涵盖从需求分析到代码审查的全流程，但存在**调用冗余**和**Token消耗过高**问题。

**用户痛点**
- **Skill调用效率低**：Agent默认按固定顺序盲选技能，导致流程冗长（如14个Skill全量调用）。
- **Token成本高**：频繁读取Skill说明文档导致Token消耗激增，用户反馈Codex的/goal命令在周五即用尽周额度。

### **🔍 现有解决方案对比**

#### **(一) 传统优化方案：Caveman项目**
- **宣传效果**：声称可节省Claude Code 65% Token。
- **实际问题**：过度压缩导致模型性能下降（"干成呆瓜"），属于**Bad case**。

#### **(二) 创新方案：OpenSquilla项目**
- **核心机制**：提出**Meta Skill**概念，通过YAML定义技能的**步骤顺序、依赖关系和执行规则**，解决技能调用的盲目性。
- **项目现状**：Star数仅为OpenClaw的1/200，但性能表现突出。

### **📊 Meta Skill技术解析**

#### **(一) 定义与优势**
- **Meta Skill**：抽象多个普通Skill为结构化工作流，明确**执行顺序**（如先分类后总结）和**依赖关系**（如`depends_on: [classify]`）。
- **硬约束机制**：在Runtime层进行**步骤校验**，未通过依赖检查时直接拦截（0次API调用，$0成本）。

#### **(二) YAML配置示例**
```yaml
kind: meta
triggers:
  - classify request type
  - route this request
composition:
  steps:
    - id: classify
      kind: llm_classify
      output_choices: [BUG, FEATURE, QUESTION, OTHER]
      with:
        text: "{{ inputs.user_message }}"
    - id: summarize
      kind: agent
      skill: summarize
      depends_on: [classify]  # 依赖classify步骤完成
final_text_mode: "step:summarize"
```
### **🚀 性能测试与效果**

#### **(一) PinchBench 1.2.1基准测试**

| 指标                | OpenSquilla（多模型）               | OpenClaw（Claude Opus 4.7）         | 差异                  |
|---------------------|-------------------------------------|-------------------------------------|-----------------------|
| **平均得分**        | 0.9251                              | 0.9255                              | 性能接近              |
| **总输入Token**     | 1,721,328                           | 3,066,243                           | OpenSquilla少44%      |
| **总成本**          | $0.688                              | $6.233                              | **成本降低89%**       |

#### **(二) Superpowers技能组合测试**
- **测试任务**：搜索2026年AI Agent生产环境风险，生成工程经理总结报告。
- **关键对比**（Meta Skill vs 原生Skill）：

| 指标                | Meta Skill（3步组合）               | 原生Skill（3次独立调用）            | 优化效果              |
|---------------------|-------------------------------------|-------------------------------------|-----------------------|
| **API调用次数**     | 1次（含3内部步骤）                  | 3次                                 | 减少67%               |
| **总输入Token**     | 15,881                              | 48,448                              | **减少67%**           |
| **估算成本**        | $0.017                              | $0.034                              | **节省50%**           |
| **输出集中度**      | 2,154 chars（单文件）               | 25,131 chars（分散3个文件）         | 结果更聚焦            |

### **💡 补充细节与关键洞察**

#### **(一) 复合工程（Compound Engineering）整合**
- **核心工具**：通过`/ce-compound`命令将知识代码化，实现技能复用，用户在开发流程末尾添加持续学习环节。

#### **(二) 模型切换机制**
- **实现方式**：支持多模型路由（Opus 4.7、GLM5.1、DS4 Flash），通过本地小模型预处理任务分类（简单/复杂）。
- **限制**：仅支持**新会话切换**，避免同会话内模型切换导致的上下文混乱。

#### **(三) 行业趋势判断**
- **Skill数量陷阱**：Clawhub平台Skill数量达6万+，但实际常用仅50-70个，**工作流稳定性**比技能数量更关键。
- **下一代竞争焦点**：从"卷模型/技能数量"转向"卷流程编排"，通过Meta Skill实现技能的**有序组合与成本优化**。

## 原文 / 逐字稿

两天前，我在朋友圈分享了把Superpowers这个20万的GitHub项目做成垂直Agent的方法。

没多久就收到一句吐槽，这14个Skill组合起来太啰嗦了，还烧Token。

确实这是我这段时间一直在想解决问题，

好的Skill很多，但很多时候都是让Agent去盲选调用顺序。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5202f7271d2be57238d70a6a8d94d23e?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=gg5h%2BVPsFKxAyyacU9K4a5%2Fs0fo%3D)

Superpowers三个月前还是10万star，现在又翻倍了

虽然它在Readme里面塞了一个基本工作流，但是我并不是每一次调用都需要那么多skill的。

想来想去，还是每个人按照自己的习惯，安排一套这个skill的调用顺序最合适。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffa3647b7e4e9923099cc413a5bacdd6b?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iv1%2BY6acritvOY2Q4FwZCWeghNI%3D)

而且把Skills定好调用顺序之后，我还可以把其他框架上跟它重叠但不重复的技能纳入到这个工作流里面。

比方说我就很喜欢在开发流程的最后一句触发compound里面的持续学习。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc8827978ab81e5ff9706daa679f6b395?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=PJRUboykpkjKzXT0sIU%2F9xsjfkY%3D)

这个问题可以被具体化成，

到底该怎么用这一组Skill？

一组Skill就像一个百宝工具箱。你知道我知道大家都知道里面有好东西，但每次执行的时候，还是得判断今天该用哪个，顺序是什么，要不要全塞进上下文，哪些步骤可以跳过等等等等。

更麻烦的是，每读一个Skill的说明烧的都是我的TOKEN啊，Agent自己不心疼，我心疼。

这种麻烦在最近狂用Codex的/goal命令的时候达到了顶点，我的周额度居然在周五就没了，重生之72小时我成古法手写程序猿了属于是。

这两天在GitHub上大搜特搜省TOKEN还不降模型智商和体验的项目，

Bad case是这个，说是会给Claude Code剩下65%的TOKEN，结果给我Claude干成呆瓜了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb7215e4c9a3803d4fac67327c242872f?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wMq4dj6WpZkUmtzkfsROt%2FGYZwg%3D)

还有一种新玩法是从Skills的组织入手的，

叫做，OpenSquilla

他把多个Skills组织抽象成了Meta Skill。

普通Skill解决的是，我会什么。

Meta Skill解决的是，现在这个任务，我该怎么把这些能力串起来。先做哪一步，后做哪一步，哪一步依赖前一步，哪一步没完成就别往下跑。

不过这个项目跟OpenClaw比star差了快两百倍，所以我们还是先来看看纸面实力，在PinchBench
1.2.1上，三个模型混着用的OpenSquilla跟Claude Opus 4.7版的OpenClaw得分几乎一样，但Token少了将近一半，成本不到1/9。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faacb70ebce18571ae43415a0303113b9?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JpWap%2BEFnn%2BJVZmofIlyZO3JSBM%3D)

超光速看了一下项目代码，一个很突出的差异点是，OpenSquilla的Meta Skill会让我们多写一份SKILL.md。

这份文件不是一段提示词。

它是在用YAML定义Meta Skill的步骤、顺序和依赖。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F47742dd6982f911d53820402a0c99a7a?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JKIvH31Vc9GLH545irHyAmIYhLs%3D)

看到depends\_on: [classify]了吧，

翻译成人话，就是先给输入做分类，是bug，提问，还是其他情况。

没分完类，就不准往下走。

看到的时候我第一反应是，这不就是写了一套rules吗？

区别在硬约束，

rules靠模型自觉，上下文一长，模型就可能突破约束。MetaSkill不一样，它会在Runtime层先检查一遍。步骤顺序对不对，依赖有没有闭环，权限够不够。

通不过校验，0次API调用，一分钱都花不着。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb6432f1c2df4d22b19c8736b58e99a73?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1Hrn5ciEDDA7UDIg2iktT59AcNU%3D)

为了测试我故意写了一个坏依赖，depends\_on: [missing\_step]，指向一个不存在的步骤。真就直接在Plan
Validation阶段拦截了，连LLM调用都没发出去。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F12e0ff939eef09acbf81464c1c6a3ef7?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=y5rGdy4Ce1aoJn0jgcJDDt2wrxs%3D)

以前我们是靠写Rules让模型遵守约定。

现在变成了先用代码转一圈看看，这条工作流本身成立吗？

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa68f18a311f07785174bfa70ad411819?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=EFxaAtsOaZ2Df%2BEHtd1xt%2F%2BC704%3D)

那我直接上手把把Superpowers底下Skills组合做成Meta Skill，

brainstorm负责想需求，write\_plan负责写计划，verify负责检查风险，作为我日常的固定搭配流程。

打包成一个Meta Skill后就不需要Agent每次来考虑这次需不需要，一套流程定下来，跟着规定走，不能遗漏也不能跳步。

用同一个提示语任务测了三轮，提示语都是搜索3个2026年AI agent跑生产环境的风险，再写一段给工程经理看的总结。

能看出来有没有Meta Skill差距还是蛮大的，

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F147cac84a3248b096c62e7ddc658d6ff?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yIr6YOQgHtrHKyWPtW4ROowJ%2FPo%3D)

同样是成功跑完了内容，Meta Skill把输入TOKEN就压到67%。

每一步思考过程减少了，也不再把Token消耗在迁移途中的说明上，

用人话说的话，它用更长的前置运行时间，换来更少的重复上下文消耗。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5b07b7a88db8c70a07a94c9525c59729?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xBmF3ZcHLkgVsTTujRdxEv0jHe4%3D)

对于模型切换 ，OpenSquilla支持多家模型，自带了一个本地小模型，我发的请求在要发给干活的大模型之前会先做个分类是简单还是复杂任务。

不过这个模型切换只能在是在新开session或者新建立对话情况下才实现。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa5934df0ebc01c12ece2a5e0e8713abd?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zzr1pTHMga7sOwUL4OmPsoonGvk%3D)

我觉得还是为了切起来够稳定，

如果在同一个Session中频繁换模型，很容易就会出现上下文缓存，工具格式和日志混乱等等问题。主要是我心痛我Claude的一小时缓存。

还有，我留意到一个细节，

OpenSquilla用子Agent去理解和压缩上下文，也就是说在一个上下文是
400K左右的模型，到了300多接近400K的时候，还是能够能记住我之前说的点。提示语长这样，

```
我：设计一个 AI Agent 的测试计划，包含安装流程、功能测试、失败场景、评分标准和结论。输出为结构化 Markdown。  
🦐：生成的文件已准备就绪：ai-agent-test-plan.md ✅  
我：Search the web for the latest AI agent frameworks news in 2026, fetch 3 pages, then write a structured reportcomparing them in a table. Include pros/cons and pricing.  
🦐：（自动触发 web_search → web_fetch × 3 → 生成报告）输出：一份包含 8 个框架的对比分析报告Claude Agent SDK、OpenAI Agents SDK、Google ADK、LangGraph、CrewAI、Smolagents、PydanticAI、AutoGen含 Executive Summary、Key Findings、对比表、协议矩阵、局限性分析
```

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F58060d654b73090e65ead239f55c03bd?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=d9WCqQSGfwMnIppipcjtlGuQ138%3D)

同一个对话里，从你是谁到写一份8个框架的调研报告，全跑通没有忘记上下文。并且在话题结束，给出一份巨巨巨详细的花销明细。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F99d17094fef2445ee2301fd48f8d815d?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=bWZFLlVsqV1Tw5E%2FbsJXYp1PrnA%3D)

从自我介绍到8框架竞品报告，

同一会话花了7美分都花在哪了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe77e491331be4c5cc8ca373aa0e4bdeb?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qUqgBwZ1cAMBQUbDwi%2FtOtyyJpk%3D)

OpenSquilla把这一切都摊开了。

每个Session的Token数和成本精确到小数点后四位。这一轮测下来，只能说星不可貌相啊，全是狠活。

过去半年，

Agent是先卷模型，再卷MCP，接着卷Skill。

Skill都卷到Clawhub上有6w多了，

正常一个Agent也就常用的也就50个70个。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F88ba188fea386b5108093c90a0449ba7?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=L4XUxJ68T4q0JxRSRrX6gk6Ta2M%3D)

可能挑了很久，终于选了一个Skill带回家，

但过几天，新的又来了，旧Skills也就被忘了。但Agent每轮都还是会读旧Skills的说明书，

对我来说过多的Skills只是散落在仓库里的文件，但Agent会因为Skills里内置的各种规则误导，

规则加太少，Agent容易失去了方向，

规则加太多，Agent就左脑打右脑了。

真正拉开差距的，从来都不是谁的Skill更多，

这跟一周能不能烧掉一亿token一样没有意义。

能不能把Skill串成一条稳定的工作流，

别让Agent在完全没有限制的空间里临场发挥。

我们真正需要的是让它知道,

第一步做什么，要不要继续。

哪一步没必要，能不能省略。

这一步的问题，要怎么定位。

每次对话的下一次都能跑更稳定，

把好的步骤做的更好，

坏的Bug也不再发生。

@ 作者 / 卡尔

---

最后，感谢你看到这里👏如果喜欢这篇文章，不妨顺手给我们*点赞｜在看｜转发｜评论 📣*

如果想要第一时间收到推送，不妨给我个星标🌟

如果你有更有趣的玩法，欢迎在评论区聊聊🤝

更多的内容正在不断填坑中……

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8664692eb89ed1eb18a14b5345b1044a?Expires=1783831558&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ENgzIoDypNiRO%2BLtBm3prlYQAyo%3D)
