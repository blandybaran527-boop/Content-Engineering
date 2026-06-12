---
title: "与AI协作的产品设计六原则：实践指南与核心洞察"
channel: wechat
src_id: agent-ju
item_id: Q8j4611EjzdAN5rMFjAeoQ
source_url: https://mp.weixin.qq.com/s/Q8j4611EjzdAN5rMFjAeoQ
note_id: 1912593559472240768
task_id: 6a2b96d6d3d5e89d4f9d6328
task_elapsed: 20
fetched_at: 2026-06-12T05:19:48.397018+00:00
summary_len: 1429
body_len: 2672
---

# 与AI协作的产品设计六原则：实践指南与核心洞察

> 原文: https://mp.weixin.qq.com/s/Q8j4611EjzdAN5rMFjAeoQ

## AI 总结

### **📌 前言：AI时代的产品设计范式**

团队在近几个月与AI协作开发产品的实践中发现，**AI虽能显著提升生产力，但真正的瓶颈在于人类自身的决策与判断**。基于实践经验沉淀的六条原则，可作为与AI协作进行产品设计（PD）时的核心指导框架，建议作为提示词提供给协作工具（如Cola或个人Agent）。

### **🔍 核心原则深度解析**

#### **1. AI是人的放大器，优点和缺点都放大，人的判断仍是核心**
- **核心逻辑**：AI会同时放大清晰的目标与模糊的需求，人类需把控方向正确性。
- **实践案例**：某复杂功能在AI辅助下2天完成开发，但因未明确核心任务，用户使用时完全无法理解操作逻辑。
- **关键问题**：*"在进入开发之前，这个功能的最主要任务，想清楚了吗？"*

#### **2. AI擅长加法，人要做减法**
- **核心逻辑**：AI可无成本生成大量方案，但过度堆砌会导致体验混乱，需人类进行取舍与聚焦。
- **实践案例**：AI为页面设计10个功能按钮，用户因信息过载无法决策；AI进一步为每个按钮添加说明，陷入"错误迭代"循环。
- **关键问题**：*"如果一个页面砍到只剩一个按钮，它是什么？"*

#### **3. AI擅长大路货，人要提供独特品味，并沉淀成可复用的context**
- **核心逻辑**：AI倾向于整合现有方案生成平庸结果，需人类注入独特性并固化为可复用的设计规范。
- **实践案例**：AI参考所有竞品设计的界面功能全面但缺乏记忆点，用户反馈"无感"。
- **关键问题**：*"你是否觉得这个地方的品味「非他不可」？是否能把这个品味收束成一个skill或一个md文件？"*

#### **4. AI擅长做半成品，人要打磨到80分才交付**
- **核心逻辑**：AI可快速产出基础方案，但细节打磨需人类完成，且AI的边际效益随优化深度递减。
- **实践案例**：AI生成的页面框架合理但存在多处细节缺陷，直接交付导致用户注意力分散。
- **关键问题**：*"这个功能达到80分了吗？如果只有60分，目前的状态提供足够高的价值了吗？"*（注：模型类交付物可能例外）

#### **5. AI擅长表面功夫，只有人才能共情**
- **核心逻辑**：AI可实现视觉与交互的形式优化，但用户情感共鸣需人类基于真实体验洞察。
- **实践案例**：某页面（vibe coding）动效炫酷但缺乏情感触动，而优秀设计仅需一句话即可打动用户。
- **关键问题**：*"用户看到这个页面的第一感受是？"*

#### **6. AI可以无限生成，人要守住一致性**
- **核心逻辑**：AI易产生多样化方案，需人类确保产品体验的统一性，降低用户认知成本。
- **实践案例**：产品中"打开文件"功能在三个位置的右键菜单设计不同，导致用户需重复学习。
- **关键问题**：*"用户使用产品时，是进入心流还是在不断思考？"*

### **📝 补充细节**
- **原则应用场景**：六条原则不仅适用于功能设计，也可作为PD文档本身的评估标准（"你这次的产品设计符合以上六条原则吗？"）。
- **协作模式**：本文案例中，原则由模型Cola（Fable 5）整理，插图由Cola（Nano Banana Pro）设计，体现了"人类定义原则+AI执行落地"的协作范式。

## 原文 / 逐字稿

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F96d1c87a0a86d11dddfca00ae0dd25f4?Expires=1783833588&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=QaAN1W4SrtzEt48Xs25Y0rt3q7U%3D)

最近几个月，我们团队都在跟 AI 一起做产品。

AI 可以极大提提到我们的生产力，但我们最终发现生产力的瓶颈在我们自己。

在这几个月的实践中我们踩了很多坑，也沉淀下来一些原则或者说教训。

可以在和 AI 做 PD 设计的时候，把这些发给自己的 Cola 或 你自己的 Agent 作为原则

1. **AI 是人的放大器，优点和缺点都放大，人的判断仍是核心。**

   AI 放大清晰的意图同时也放大糊涂。

   例：开发一个复杂的功能，有了 AI 加持后，开发速度很快，只用了两天。上线后，用户看到界面却不知道怎么用。

   问：在进入开发之前，这个功能的最主要任务，想清楚了吗？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F995fca64a423fc1ae93ff3799ad30a64?Expires=1783833588&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jRhg2R0mIYhd1X1Tjcu%2B5wMnrwI%3D)
2. **AI 擅长加法，人要做减法。**

   AI 产出没有沉没成本，人砍起来要狠。

   例：AI 可以给页面瞬间加10个按钮，但用户看到这么多按钮，却感觉很凌乱，注意力不够，接下来 AI 可能会给每个按钮增加一个说明，在错误的道路上越走越远。

   问：如果一个页面砍到只剩一个按钮，它是什么？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3c5f1ffa7b36472e0feb0decbcbf6de2?Expires=1783833588&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=AqH8PDuAMTjb3mywG0wmCU3Nsj0%3D)
3. **AI 擅长大路货，人要提供独特品味，并沉淀成可复用的 context。**

   例：AI 设计了一个功能，这个功能参考了市面上的所有竞品，吸取了所有优点，结果是做出了一个世界上最平庸的界面。用户用完的感受是：无感。

   问：你是否觉得这个地方的品味「非他不可」？是否能把这个品味收束成一个 skill 或一个 md 文件？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6d98dfecedf38d7a8bec6b5c703b2324?Expires=1783833588&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=02aZSJMv985wqsq6%2BFFu91oqKFw%3D)
4. **AI 擅长做的半成品，人要打磨到 80 分才交付。**

   例：AI 做了一个页面，看起来很合理，但有很多细节问题，这时候交付给用户，反而会让用户的注意力分散。打磨的过程中，需要人给出自己的感受，而每一步提升，AI
   所提供的提升都边际递减。

   问：这个功能达到80分了吗？如果只有60分，目前的状态提供足够高的价值了吗？（如果交付物是模型本身时，价值可能是足够的）

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9406969189c99b5b10cddad1149a95a7?Expires=1783833588&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=HrL0nUigAEwXgcWTC1CsawvmoMk%3D)
5. **AI 擅长表面功夫，只有人才能共情。**

   我们都说一页一个 CTA，这只是表象，要洞察用户此刻的感受。

   例：vibe coding
   的页面看起来什么都不缺，动效也很炫酷，读起来就是不打动人，好的东西，哪怕页面只有一句话也能打动人，真正稀缺的是有人替用户感受过那一刻。

   问：用户看到这个页面的第一感受是？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdb577e2df2f4159a5cf64d0a38bf6b06?Expires=1783833588&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FIRkWxwonh8Y4MiGCzPvtWL1p40%3D)
6. **AI 可以无限生成，人要守住一致性**。

   同一个东西对应同一种 UI，本质是给用户熟悉感，用户不该把一个功能学三次。

   例：同一个"打开文件"，在产品的三个位置右键菜单竟然各不相同，用户需要适应三次。

   问：用户使用产品时，是进入心流还是在不断思考？

   ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdc93a00141272fe881c1250463fac849?Expires=1783833588&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=XrhCn7IvuKP9mXwnSnBxbzC0tKo%3D)

最后，请不要忘记，PD 文档本身也是产品，你这次的产品设计符合以上六条原则吗？

---

故事口述：橘子

原则整理：Cola （模型 Fable 5）

插图设计：Cola （模型 Nano Banana Pro）
