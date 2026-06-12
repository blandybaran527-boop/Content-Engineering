---
title: "2026年高考数学全国一卷AI模型能力测评报告"
channel: wechat
src_id: aiwarts
item_id: 6BhJ9NW3sxeC-Ceg2Hnn5w
source_url: https://mp.weixin.qq.com/s/6BhJ9NW3sxeC-Ceg2Hnn5w
note_id: 1912593483236571264
task_id: 6a2b968fd3d5e89d4f9d60c5
task_elapsed: 40
fetched_at: 2026-06-12T05:19:07.532197+00:00
summary_len: 2427
body_len: 6974
---

# 2026年高考数学全国一卷AI模型能力测评报告

> 原文: https://mp.weixin.qq.com/s/6BhJ9NW3sxeC-Ceg2Hnn5w

## AI 总结

### **📌 测评背景与试卷概况**

**高考数学卷难度反馈**
- **社交媒体反响**：#数学一卷喜提大专# 话题阅读量达1.5亿，讨论量2.5万，考生普遍反映难度过高。
- **典型评价**：考生称"第五题就不会写"，部分考生调侃"逐梦大专"，反映试卷区分度显著。

**试卷结构与题型**
- **总分**：150分，共19题（8单选+3多选+3填空+5解答题）。
- **压轴题示例**：第19题（17分）涉及函数定义域、集合运算及奇偶性证明，要求多步骤逻辑推导。

### **🔬 测评方案设计**

**参与模型与测试规则**
- **13个AI模型**：包括Claude Opus 4.8 Max、GPT 5.5 Thinking、Gemini 3.1 Pro Thinking、Deepseek-v4 Pro等主流大模型。
- **核心规则**：
  - 统一使用2026数学全国一卷，关闭联网与外部工具调用
  - 采用LaTeX格式输入（经Mathpix转换+人工核验）
  - 严格遵循高考评分标准，按步骤给分

**测评流程优化**
- **多模态支持**：因模型上下文窗口扩大（较去年翻倍），保留第15题图像题测试
- **提示语标准化**：要求模型按高考答题规范展示完整过程，包括推理步骤、计算过程及最终答案

### **📊 AI模型得分排名与能力分析**

**总分排名（满分150分）**

| 排名 | 模型名称          | 总分 | 梯队划分       | 能力特征                     |
|------|-------------------|------|----------------|------------------------------|
| 1    | GPT-5.5           | 144  | **第一梯队**   | 难题攻坚能力强，稳定性优异   |
| 1    | Deepseek_v4       | 144  | **第一梯队**   | 计算精度高，步骤完整性突出   |
| 3    | Gemini            | 142  | **第一梯队**   | 逻辑推理严密，细节处理到位   |
| 3    | Opus 4.8          | 142  | **第一梯队**   | 综合能力均衡，复杂题处理优秀 |
| 5    | Kimi 2.6          | 139  | 第二梯队       | 大题思路清晰，小题偶有失误   |
| 6    | Sonnet 4.6        | 134  | 第三梯队       | 基础题稳定，难题突破不足     |
| 7    | GLM 5.1           | 131  | 第三梯队       | 中等难度题得分率高           |
| 7    | Doubao（豆包）    | 131  | 第三梯队       | 本土化题目适应性较好         |
| 9    | Qwen 3.7          | 130  | 第三梯队       | 上下文记忆较弱，易漏条件     |
| 10   | Minimax M3        | 129  | 第三梯队       | 计算步骤偶有跳跃             |
| 11   | Yuanbao（元宝）   | 118  | 第四梯队       | 基础分稳定，高分题失分明显   |
| 12   | Mimo-2.5-pro      | 102  | 第五梯队       | 仅掌握基础题型               |
| 13   | Grok              | 99   | 第五梯队       | 思路不完整，计算错误率高     |

### **❌ 典型错题深度复盘**

**第6题：输入误差导致的理解偏差**
- **题目特征**：函数最值问题，因LaTeX格式转换可能产生符号识别错误（如"aˣ+a"误读）
- **错误表现**：约50%模型受输入偏差影响，但部分模型通过逻辑推理自动修正至正确答案
- **启示**：模型对符号输入的容错性存在显著差异，格式标准化至关重要

**第11题：多选题的边界条件判断失误**
- **正确答案**：ABD（三个弦长相等的强条件判断）
- **错误模式**：所有模型均错选C选项（误将"弦长和=3"的弱条件纳入）
- **原因分析**：过度泛化导致边界条件判断失误，反映逻辑严谨性仍需提升

### **⚠️ 模型常见问题与限制**

**核心能力短板**
1. **上下文记忆**：Qwen等模型存在"做到后面漏条件"现象，尤其在多步骤解答题中
2. **格式理解**：LaTeX转换中符号、上下标丢失导致后续推理全链错误
3. **输出规范**：部分模型未按要求展示完整证明过程，仅给出结论

**异常行为记录**
- Sonnet 4.6尝试联网搜索答案
- Deepseek-v4 Pro出现中途拒绝答题情况
- Opus 4.8因思考过程过长导致超时未完成

### **💡 关键洞察**
1. **能力分层显著**：头部模型（GPT-5.5/Deepseek）已达"清北水平"，而尾部模型（Grok/Mimo）仅相当于基础达标水平
2. **失分点高度集中**：多选题（边界条件判断）和长解答题（步骤完整性）是主要拉分环节
3. **人机差异明显**：AI模型擅长复杂计算但易在"常识性严谨性"上翻车，与人类考生"粗心"表现类似
4. **技术瓶颈待突破**：输入容错性、上下文一致性和指令遵循度仍是下一代模型需重点优化方向

## 原文 / 逐字稿

又到了一年一度的高考，

先祝考生们考的都对！这种时候就适合来考AI，一开始我觉得要是全员满分的话，那我这标题应该直接是AI已经攻略高考了才对，没想到还是有被拉开差距。

先来看看试卷，今年的全国一卷难度高到考完就逐梦大专。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F63658c7d5ae45cd4a2bc16f74a8bcb3e?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=emMNxd77tJSyssJ2CI2JanC%2Ba1s%3D)

那还说啥了，直接上做题规则，

这次参加考试的有13个模型，Claude Opus 4.8 Max, Claude Sonnet 4.6 Thinking, GPT 5.5 Thinking,
Gemini 3.1 Pro Thinking, Qwen 3.7 Plus Thinking, MiniMax M3, Kimi 2.6 Thinking,
Mimo-2.5-pro, Deepseek-v4 Pro, GLM 5.1, Grok, 豆包 Thinking,
元宝Thinking（一口气全念对要很好的肺活量）

为了公平性，我采用了同一张卷子，2026数学全国一卷，

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F03aa55340b078137c78a85e6b7176dc3?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yg1AAxHc%2F4IQGuEUIRkWESH4yCo%3D)

记分方法就跟高考判分的保持一致，不管是网页版还是API都关掉联网，

跟去年最大的不同，今年大部分的模型上下文都翻了一番，基本都支持多模态了，所以第15题图像题照样保留。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4bd245387fe4a5181cf1c48983c46fd5?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7vBeR%2B%2FaODEk6L13PQ0xktLSjyI%3D)

同时因为读取PDF会比读取markdown化的考卷要更耗额度，我的两个Claude都没考完额度就没了，所以我们统一用mathpix把PDF转成了LaTeX格式，每一道转化的题都会单独人工再看两次。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb6d1a224957e82f175d2e236ad35acdf?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hmdxJ%2BgBgkunVwH%2BmKmDtZbviEg%3D)

LaTeX的好处就是能保证每家模型都可以读取到一样的信息，

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0bdd2437c60c998d48bfb7fb67724918?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vG9a3vOYg%2FFqEyJI4jTbOHFRYJA%3D)

每个模型都会在一个新对话里收到一个提示语，中间我们不干涉不对话如果失败直接新对话重新跑。

```
# 测试提示语请使用你当前可用的最高推理能力，像一名中国高考数学考生一样，在不联网、不查资料、不使用代码、不调用外部工具的情况下，独立完成下面这套高考数学试卷。你的目标是尽最大努力获得尽可能高的分数。请按照高考数学答题标准作答，展示完整、清晰、可评分的解题过程。  
作答规则：1. 请按照题目顺序从第一题做到最后一题，不要跳题，不要中途停止。2. 每道题都必须作答。即使不确定，也要给出你认为最合理的答案，并说明不确定点。3. 选择题：请写出推理过程，并明确给出最终选项。4. 填空题：请写出推理过程，并明确给出最终填空答案。5. 解答题：请按照高考答题格式分步骤作答，必要时分小问回答。6. 请完整展示关键步骤，包括公式选择、代数变形、计算过程、分类讨论、函数分析、几何推理和结论判断。7. 不要编造题目没有给出的条件，不要跳过图形、表格或题干中的限制条件。8. 每道题结束后，请进行简短检查，确认计算、符号、定义域、取值范围、单位和最终答案形式是否合理。9. 最后请给出“整套试卷答案汇总”，只列每道题的最终答案，方便评分。    
请严格使用以下输出格式：第 1 题：解题过程：……检查：……最终答案：第 2 题：解题过程：……检查：……最终答案：……  
整套试卷答案汇总：1. 2. 3. ……
```

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbbd33785e4ddf8b95447ba8dc7e38068?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TTa65Wh8Yi%2Fo5NLJG2jJeYTYa90%3D)

开考开考！收卷收卷！改卷改卷！最终得分表出炉！来看看模型们的精确选项。

模型总体得分是这样的，

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Febc999f919e4e410f11bc2aa55083d96?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=m0QNhseQEnd7lwk7YtKy4PPvKQ0%3D)

模型具体选项也是这样的，

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb641c5340fd8288963ecd612de08284c?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=9RhCWkIfKkiqFmjhpQ1tfKFWric%3D)

来看看最终分数吧！

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa682ef1b348abc64c49f1a34d7cd9a5e?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=LoTj45HBgnxPKoznfCePPpWVB%2BM%3D)

马上来个真题复盘，

第6题是这套卷里最有节目效果的一题。

起初测试发现了一半左右的模型都错了，还以为是世纪难题。后来发现，问题出在输入环节。

网上存在不同版本的题目，在读取LaTeX 输入的过程中，也被识别错误。

所以有的模型就被这个错误输入成功带偏，通过自己的理解，自动fallback到了一个同题型下的正确答案。有些也有给出根据错误输入从而没有答案的正确回答。为了答题一致性，我们将有合理答案的都作为对的最终采纳。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F360b847ec300a0f7dc50a3b1bbd7998e?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=B3QsqFDLomeCpQ04jZuFYT6vLE0%3D)

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F399233b74567f9176bdc11fc0d0f6380?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=v48nnPo2z0WK5zWIh8bIFOtyMO0%3D)

最终复核后的结果，

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3fe1ee6e3aa35199057e4e6353ad7fc9?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=PITyBHIQEtyghbMrIlTKqYUd9%2BA%3D)

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe3a83d738766ec2e1875f8975fd467fb?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1ck8Um17I9n7RZKlcOKyWj104F8%3D)

第11题是这套卷里最选择困难的一题。

并不是模型完全不会做的题，而是看着好像不难，就最后多一步非把自己送走的多选题。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff7a144adee972888c1b6dcd6483ad002?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=f4pPjxo4zzp%2FwnuojABDEyggeng%3D)

答案是ABD，

但是所有模型居然没有一个完全答对，我看了一下，在过程里已经接近正确了，但为了保险过度泛化了，把诱导项也一起选上了。

用人话来说，

B选项要求三个弦长完全相等，这是一个强条件，最后只剩三条直线；C选项只要求三个弦长的和等于 3，这是一个弱条件，看起来会留下连续一族直线。

模型 ABD 的正确方向摸到了，但又把 C 这个“看起来也成立”的边界项塞了进去导致结果错误。

本来以为现在大模型的得分都那么高了，跑起来一定不会有什么问题吧，实际上过程非常磕磕绊绊。

首先就是上下文窗口以及记忆，

像Qwen和以下的梯队的模型，做到后面就开始漏条件，甚至反过来问我思路和想法，忽略前面说过的考场要求。甚至是没有理解题目规则。比如题目要求证明，它只给了结论。题目要求完整作答的，它也只写了思路。

然后就是API传输和输出限制，

Opus 4.8 开了最高权限导致思考的过程太慢。Context被截断，rate
limited，或者一次回答装不下等等等等都发生过，导致最终超时了来不及写完或者只留下了一堆没有结果的草稿(Thinking memory)让我验收。

但但但但但！最离谱的还是考场离谱行为，Sonnet 4.6尝试直接搜答案还有Deepseek直接拒绝完成都是真实存在的，刚开始就想走人了。

根据每个模型的得分，我还给他们做了一个评级系统，

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F91a6cad9cf25c6625e6b7b52ba69f99c?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Ih5fn0UUxfOtn0ED0i5e8mkAWb8%3D)

PS：叠个甲，纯娱乐分层，因为只有数学单科成绩

最终得分上，AI和AI之间的差距，也就是和我和清北之间的距离差不多嘛。

第一梯队 GPT 5.5, Deepseek-v4 Pro, Gemini 3.1 Pro 以及 Opus
4.8。强的不止会做难题，并且整体也是稳定的学霸，该拿的分都拿到了也没有特别的错误。

而只差些微分数的Kimi 2.6属于第二顶尖。不是能力不够，大题也能做出来，只是会在选择题、多选题或者填空完整度这种的小地方导致失分，才没进第一梯队。

第三梯队也是大多数，包含了 Sonnet 4.6，GLM 5.1，豆包，Qwen 3.7 Plus，以及MiniMax
M3。也算是模型的平均线了，当前还没有那么稳，会在不同细节上丢分。不是不会，只是粗心，或者关键步骤没有收住。

元宝118，独树一档，能做不少题，在稳住了百分的情况下也会有明显失分。

Mimo 和 Grok 就是这次发现最需要进步的模型了，更像普通考场发挥。有思路，有想法，但也就一些基础分了。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F670b8e3ba44083b02a995c8b6964be87?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yJpxWk5B0OiEm6EkSyTypnGbU8c%3D)

批完卷子之后，

发现不是只有低分选手会翻车，就算是144分的清北种子模型也都会被多选题中的制定条件坑一把。

除了多选，长解答题是真正拉开差距的地方。

能不能读好完整条件，算好所有公式，条件步奏有没有记住，直到出最后的具体答案。

很多模型有思路，也能写方向，

但在严格评分里就是拿不到分。

最后还有一个很关键的问题，就是题目理解。

很多时候模型一开始就没稳稳接住。

读题就读错了，图没看清楚，直接往反方向飞奔。

又或者从LaTeX里抽出来的时候符号，条件，上下标丢了一点，

后面再怎么推都推不对了。

![Image](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1fc505eedbe44687de915eb68239b705?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vGWGgYz5FJw7Y4GdZL8TA008%2BmM%3D)

所以这次测下来的感觉就是，

AI确实很强，高考题能难倒它们的不多，

有些模型已经不像是在做题，

更像是老叟戏顽童。

但它们也不是完全不会翻车。

会看错图，会漏选项，会写到一半开始意会，

也会在长题最后一步突然卡个十几分钟。

今年在高考期间都不让用AI了，

我们在测试的过程中反复尝试了好多遍。

不过这个系列可能还是会一年一度做下去的。

这次高考数学题还是挺难的，

让我限时马上去做估计也是够呛，

但还是可以带着AI跟大家一起考一份试卷，

看下难度，还是很有意思的，

希望明年AI考生的数量再多一点。

@ 作者 / 卡尔 & yc星辰

---

最后，感谢你看到这里👏如果喜欢这篇文章，不妨顺手给我们*点赞｜在看｜转发｜评论 📣*

如果想要第一时间收到推送，不妨给我个星标🌟

如果你有更有趣的玩法，欢迎在评论区聊聊🤝

更多的内容正在不断填坑中……

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8664692eb89ed1eb18a14b5345b1044a?Expires=1783833545&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4YIKYx9ZR%2FZS7j3hlQ452ZZwPi0%3D)
