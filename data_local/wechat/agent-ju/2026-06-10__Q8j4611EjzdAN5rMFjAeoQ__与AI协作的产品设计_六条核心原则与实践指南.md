---
title: "与AI协作的产品设计：六条核心原则与实践指南"
channel: wechat
src_id: agent-ju
item_id: Q8j4611EjzdAN5rMFjAeoQ
source_url: https://mp.weixin.qq.com/s/Q8j4611EjzdAN5rMFjAeoQ
note_id: 1913131213141624016
task_id: 6a333acf015d31e802628718
task_elapsed: 40
fetched_at: 2026-06-18T00:25:39.605094+00:00
summary_len: 1413
body_len: 2682
---

# 与AI协作的产品设计：六条核心原则与实践指南

> 原文: https://mp.weixin.qq.com/s/Q8j4611EjzdAN5rMFjAeoQ

## AI 总结

### **📌 前言：AI时代的产品设计挑战**

团队在与AI协作开发产品的实践中发现，AI虽能显著提升生产力，但**人的判断与决策仍是核心瓶颈**。通过总结实践中的经验教训，形成六条关键原则，可作为与AI协作进行产品设计（PD）时的指导框架。

### **🔍 六条核心原则深度解析**

#### **1. AI是人的放大器，优点和缺点都放大，人的判断仍是核心**
- **核心逻辑**：AI会同步放大清晰意图与模糊决策，需以人的判断把控方向。
- **实践案例**：某复杂功能在AI加持下2天完成开发，但因前期未明确核心任务，导致用户使用时无法理解操作逻辑。
- **关键问题**：*"在进入开发之前，这个功能的最主要任务想清楚了吗？"*

#### **2. AI擅长加法，人要做减法**
- **核心逻辑**：AI可快速生成大量功能或元素，但易导致信息过载；人需通过减法聚焦核心价值。
- **实践案例**：AI为页面设计10个按钮，用户因信息混乱无法聚焦；进一步增加说明文字后，问题加剧。
- **关键问题**：*"如果一个页面砍到只剩一个按钮，它是什么？"*

#### **3. AI擅长大路货，人要提供独特品味，并沉淀成可复用的context**
- **核心逻辑**：AI倾向于整合现有竞品优点，产出同质化方案；人需注入独特设计品味，并将其转化为可复用的规则或文档。
- **实践案例**：AI参考所有竞品设计的界面功能全面但平庸，用户反馈"无感"。
- **关键问题**：*"你是否觉得这个地方的品味「非他不可」？是否能把这个品味收束成一个skill或一个md文件？"*

#### **4. AI擅长做半成品，人要打磨到80分才交付**
- **核心逻辑**：AI可快速产出基础可用的方案，但细节需人工优化；交付前需达到80分标准以确保用户体验。
- **实践案例**：AI生成的页面框架合理，但存在多处细节问题，直接交付导致用户注意力分散。
- **关键问题**：*"这个功能达到80分了吗？如果只有60分，目前的状态提供足够高的价值了吗？"*（注：模型类交付物可能例外）

#### **5. AI擅长表面功夫，只有人才能共情**
- **核心逻辑**：AI可实现视觉效果与交互设计，但难以捕捉用户深层情感需求；需通过人类共情能力提升产品感染力。
- **实践案例**：某页面动效炫酷但缺乏情感共鸣，而优秀设计即使仅含一句话也能打动用户。
- **关键问题**：*"用户看到这个页面的第一感受是？"*

#### **6. AI可以无限生成，人要守住一致性**
- **核心逻辑**：AI可生成多样化设计，但需保持产品体验的一致性，避免用户重复学习成本。
- **实践案例**：同一"打开文件"功能在产品三个位置的右键菜单设计不同，导致用户需适应三次。
- **关键问题**：*"用户使用产品时，是进入心流还是在不断思考？"*

### **📝 补充细节**
- **原则应用场景**：可将六条原则发送给协作的AI助手（如Cola或个人Agent），作为产品设计的约束条件。
- **PD文档本身即产品**：产品设计文档需自身符合上述原则，确保逻辑清晰、价值聚焦、体验一致。
- **工具与协作**：案例中提及的AI模型包括Fable 5（原则整理）和Nano Banana Pro（插图设计）。

## 原文 / 逐字稿

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F96d1c87a0a86d11dddfca00ae0dd25f4?Expires=1784334339&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=s8PtXQlsgTXJceGegmZMZC6KYhw%3D)

最近几个月，我们团队都在跟 AI 一起做产品。

AI 可以极大提提到我们的生产力，但我们最终发现生产力的瓶颈在我们自己。

在这几个月的实践中我们踩了很多坑，也沉淀下来一些原则或者说教训。

可以在和 AI 做 PD 设计的时候，把这些发给自己的 Cola 或 你自己的 Agent 作为原则

1. **AI 是人的放大器，优点和缺点都放大，人的判断仍是核心。**

   AI 放大清晰的意图同时也放大糊涂。

   例：开发一个复杂的功能，有了 AI 加持后，开发速度很快，只用了两天。上线后，用户看到界面却不知道怎么用。

   问：在进入开发之前，这个功能的最主要任务，想清楚了吗？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F995fca64a423fc1ae93ff3799ad30a64?Expires=1784334339&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=PxpF00mXB2juKabEuAaV0%2FhYjXk%3D)
2. **AI 擅长加法，人要做减法。**

   AI 产出没有沉没成本，人砍起来要狠。

   例：AI 可以给页面瞬间加10个按钮，但用户看到这么多按钮，却感觉很凌乱，注意力不够，接下来 AI 可能会给每个按钮增加一个说明，在错误的道路上越走越远。

   问：如果一个页面砍到只剩一个按钮，它是什么？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3c5f1ffa7b36472e0feb0decbcbf6de2?Expires=1784334339&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=V%2BRZUVJVQOHBh%2BvkNn%2F6E11AZDg%3D)
3. **AI 擅长大路货，人要提供独特品味，并沉淀成可复用的 context。**

   例：AI 设计了一个功能，这个功能参考了市面上的所有竞品，吸取了所有优点，结果是做出了一个世界上最平庸的界面。用户用完的感受是：无感。

   问：你是否觉得这个地方的品味「非他不可」？是否能把这个品味收束成一个 skill 或一个 md 文件？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6d98dfecedf38d7a8bec6b5c703b2324?Expires=1784334339&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WyZPWUeEmMSBkpcQmClHzrhA6GM%3D)
4. **AI 擅长做的半成品，人要打磨到 80 分才交付。**

   例：AI 做了一个页面，看起来很合理，但有很多细节问题，这时候交付给用户，反而会让用户的注意力分散。打磨的过程中，需要人给出自己的感受，而每一步提升，AI
   所提供的提升都边际递减。

   问：这个功能达到80分了吗？如果只有60分，目前的状态提供足够高的价值了吗？（如果交付物是模型本身时，价值可能是足够的）

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9406969189c99b5b10cddad1149a95a7?Expires=1784334339&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZEmen%2Bt23lxg4avpY84NAOlgIz4%3D)
5. **AI 擅长表面功夫，只有人才能共情。**

   我们都说一页一个 CTA，这只是表象，要洞察用户此刻的感受。

   例：vibe coding
   的页面看起来什么都不缺，动效也很炫酷，读起来就是不打动人，好的东西，哪怕页面只有一句话也能打动人，真正稀缺的是有人替用户感受过那一刻。

   问：用户看到这个页面的第一感受是？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdb577e2df2f4159a5cf64d0a38bf6b06?Expires=1784334339&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vrt3SWUGecEwziixkmiLWP1jnrs%3D)
6. **AI 可以无限生成，人要守住一致性**。

   同一个东西对应同一种 UI，本质是给用户熟悉感，用户不该把一个功能学三次。

   例：同一个"打开文件"，在产品的三个位置右键菜单竟然各不相同，用户需要适应三次。

   问：用户使用产品时，是进入心流还是在不断思考？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdc93a00141272fe881c1250463fac849?Expires=1784334339&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=L%2Bt1NPf1%2FHlK2YLrDF9HwZxe3y0%3D)

最后，请不要忘记，PD 文档本身也是产品，你这次的产品设计符合以上六条原则吗？

---

故事口述：橘子

原则整理：Cola （模型 Fable 5）

插图设计：Cola （模型 Nano Banana Pro）
