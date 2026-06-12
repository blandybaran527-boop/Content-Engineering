---
title: "Google Gemini 3.5 Live Translate：实时语音翻译技术的革命性突破"
channel: wechat
src_id: xinzhiyuan
item_id: tjYhnNtzAU-GrfE8bki7GA
source_url: https://mp.weixin.qq.com/s/tjYhnNtzAU-GrfE8bki7GA
note_id: 1912590921288054912
task_id: 6a2b8d3dd3d5e89d4f9d0b20
task_elapsed: 40
fetched_at: 2026-06-12T04:39:02.167817+00:00
summary_len: 2169
body_len: 4641
---

# Google Gemini 3.5 Live Translate：实时语音翻译技术的革命性突破

> 原文: https://mp.weixin.qq.com/s/tjYhnNtzAU-GrfE8bki7GA

## AI 总结

### **🚀 产品发布核心概况**

**发布主体与定位**
- **发布方**：Google DeepMind，由首席科学家Jeff Dean亲自官宣。
- **产品定位**：最新**语音对语音实时翻译模型**，旨在打破传统翻译的"等待式"交互模式。
- **核心价值**：实现"边听边说"的自然对话体验，将实时同传从"等你说完再翻"推进到"边听边说"。

### **🔍 技术特性与创新点**

#### **(一) 核心功能突破**
- **实时流式翻译**：说话人开始讲话时立即启动翻译，无需等待整句完成，**延迟仅几秒**。
- **70+语言支持**：覆盖超过70种语言，支持全自动语言识别，中途切换语言无需手动设置。
- **语气与节奏保留**：能维持原说话人的**语速、音高和语调**，实现情感化语音输出（如着急、慢条斯理的语气复刻）。

#### **(二) 技术实现原理**
- **模型基础**：基于**Gemini 3 Pro**打造，支持**128K token音频上下文窗口**（输入）和**64K token输出**。
- **决策机制**：通过**毫秒级决策**平衡翻译速度与质量，同步接收上下文并输出翻译语音。
- **抗干扰能力**：在嘈杂环境（菜市场、机场、马路边）仍可正常使用。

#### **(三) 与传统翻译技术对比**

| 维度                | 传统翻译技术               | Gemini 3.5 Live Translate       |
| :------------------ | :------------------------- | :------------------------------ |
| **交互模式**        | "对讲机式"等待整句完成     | 边听边译，实时流式输出          |
| **延迟**            | 整句结束后翻译（较长）     | 仅落后说话人几秒                |
| **语音自然度**      | 机械音，无情感起伏         | 保留语速、音高、语调            |
| **多语言支持**      | 有限语言，需手动切换       | 70+语言，全自动识别切换         |
| **上下文理解**      | 单句独立翻译               | 128K token上下文窗口，连贯理解  |

### **📱 应用场景与发布渠道**

#### **(一) 目标用户与场景**
- **普通用户**：日常跨语言交流（如旅游、国际社交）。
- **企业用户**：跨国会议（Google Meet支持2000+语言组合）、跨境服务（如Grab司机与乘客沟通）。
- **开发者**：通过API集成到视频配音、多语直播、跨语言客服、在线课堂等场景。

#### **(二) 发布渠道与 availability**

| 用户类型   | 发布渠道                          | 状态                  |
| :--------- | :-------------------------------- | :-------------------- |
| **开发者** | Gemini Live API + Google AI Studio | 公开预览（已上线）    |
| **企业**   | Google Meet                       | 私人预览（本月启动）  |
| **普通用户**| Google Translate（iOS/Android）   | 全球上线（实时翻译功能）|

#### **(三) 特色功能细节**
- **Android聆听模式**：手机贴耳即可从听筒输出译音，保护隐私。
- **Grab合作案例**：每月处理超1000万通司机-乘客语音电话，解决"你在哪""我马上到"等高频沟通问题。

### **📜 技术演进与行业影响**

#### **(一) Google语音翻译技术20年发展**
- **起点**：20年前作为文字翻译小实验启动。
- **规模**：目前每月为数十亿用户翻译**超一万亿个单词**。
- **里程碑**：从文字翻译→图像翻译（菜单等）→实时语音翻译，实现全场景覆盖。

#### **(二) 行业价值与挑战**
- **价值**：将专业同声传译（曾需提前备稿，时薪数千）转化为普惠功能。
- **当前限制**：仅支持音频输入；重口音、快速语言切换、多人抢话、长时间停顿可能影响稳定性。

### **📝 补充细节**
- **模型评测指标**：核心关注**翻译质量、延迟、语音自然度**三大维度。
- **合作伙伴生态**：已接入Agora、Fishjam、LiveKit等平台，提供实时媒体流基础设施支持（采集、传输、回声消除）。
- **企业级应用扩展**：Google Meet从原支持5种语言扩展至70+，单场会议支持2000+语言组合。

## 原文 / 逐字稿

### 图片

### **新智元报道**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3b253ef41422b4d012484a3c9cacf4e7?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=W6wU0Bsxucg2v8B9XDqBmM9OxIw%3D)

##### **【新智元导读】Google 发布 Gemini 3.5 Live Translate，把实时同传从「等你说完再翻」推进到「边听边说」，70+语言、几秒延迟、语气保留。**

一句话还没说完，译音已经响在你耳边——而且是对方的语速、对方的语调，只慢几秒。

刚刚，Google 甩出了 Gemini 3.5 Live Translate。

这是它最新的语音对语音翻译模型，一句话概括：把「等你说完再翻」的老规矩，直接掀了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F938c878eb46cf97fbb1da7e4284c8327?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=dMRkWJaVN142cR8pfD%2FQOKQhLfk%3D)

Google DeepMind 首席科学家 Jeff Dean 亲自发帖官宣，字里行间透着一股「二十年磨一剑」的底气：

语音翻译是 Google 跑得最久的机器学习项目之一，而这一次，它终于跑进了耳机。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6910bef4bf39a6e76d51fb8c033cfe11?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=EFffKPiCFHN2ldJvTGwhX5sXnt8%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdf9d89c9b2ec34282d3fc8aa39faec00?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2uejaXkAsnmfKPWF3w5v2nS1yC4%3D)

**把「对讲机」式翻译给掀了**

过去的翻译机大家都熟。

你说一句，它憋着，等你把话说完，再吭哧吭哧翻给对方。

一来一回，节奏全断，俩人像在打对讲机。

更要命的是，真实对话从来不是规规矩矩的你一句我一句——人会抢话、会犹豫、会说半截改口。

Gemini 3.5 Live Translate 不这么干。它边听边译，话音未落，译音先到。

这背后是一套相当微妙的平衡术：多等一会儿，上下文听得更全，翻得更准；立刻开口，能紧紧跟住说话人，但可能猜错后半句。

模型就在这两头之间逐字逐句地反复拿捏，最终交出的效果是——输出连贯、没有尴尬的卡顿，全程只落后说话人几秒。

更绝的是声音本身。

它能保留你的语速、音高和语调——译出来的不是冷冰冰的机器音，是带着你说话味儿的声音。你着急，译音也跟着急；你慢条斯理，译音也悠着来。

DeepMind 同步放出的模型卡透了点底：这个模型基于 Gemini 3 Pro 打造，能吃进最长 128K token
的音频上下文，评测就盯着三个指标死磕——翻译质量、延迟、语音自然度。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F056b333a9588a649739245186a8d89bd?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TqLOxHm9Z9QzPrt2vBc9pxCe1S0%3D)

换句话说，Google 给它定的 KPI 不是「翻得对」，而是「聊得顺」。

它能一口气认 70 多种语言，而且全自动识别，你中途换种语言它也能跟上，不用手动设置。环境吵也不怕，菜市场、机场、马路边都能用。

**![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F779d8ee2aa3c7221f0c1e639f63215ab?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IHw8Ms%2BJ5oKXR237TNV2yC2l%2Baw%3D)**

**开发者、企业、普通人，一个不落**

这次 Google 玩得很狠，三条线同时铺开。

* 开发者，通过 Gemini Live API 和 Google AI Studio 公测，今天就能上手；
* 企业，本月起在 Google Meet 私测；
* 普通人，Google Translate 的安卓和 iOS 版全球上线——点开 App 左下角的「实时翻译」，接上任意一副耳机就能用。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd9e6649d3279aa74d3f8a8fee80f8c46?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=F1yx%2B50mgjSqYmGE3Xh7YXiEcsY%3D)

最让打工人有感的是 Google Meet。以前它的语音翻译只支持 5 种语言，而且只能在英语和其他语言之间打转。

现在一口气干到 70+，单场会议能撑起 2000 多种语言组合——英语、普通话、瑞典语满桌子飞，谁说什么对方都能秒懂。

安卓还藏了个细节：「聆听模式」。把手机像打电话一样贴到耳边，译音直接从听筒里钻进来，旁人听不到。

跟个西语导游团、临时没带耳机，掏出手机往耳边一贴就能救急。

**![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F779d8ee2aa3c7221f0c1e639f63215ab?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IHw8Ms%2BJ5oKXR237TNV2yC2l%2Baw%3D)**

**每月一千万通电话**

光说参数太虚，看个真实场景。

Google 找了东南亚的 Grab 来试。司机说本地话，乘客听到的是自己的母语，接驾常用的那几句「你在哪」、「我马上到」不再鸡同鸭讲。

要知道，Grab 用户每月要打超过 1000 万次语音电话——这不是发布会上的 Demo，是真要塞进千万次日常对话里跑的活儿。

除了 Grab，CJ ENM、LiveKit 这些公司也提前上手试过，反馈都指向同一点：**质量、准确度、低延迟。**

开发者这边也省了大力气。

Agora、Fishjam、LiveKit 一票平台已经接入 Gemini Live
API，把最难啃的实时媒体流基础设施全包圆了——采集、传输、回声消除这些脏活累活有人扛，开发者只管做体验。

视频配音、多语直播、跨语言客服、在线课堂，全是现成的落点。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdf9d89c9b2ec34282d3fc8aa39faec00?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2uejaXkAsnmfKPWF3w5v2nS1yC4%3D)

**二十年长跑，跑进耳机里**

往回看一步，你会发现这事儿 Google 憋了很久。

20 年前，Google 翻译只是一个开创性的小实验，想把语言这门科学，变成人和人连接的魔法。

如今每个月，它要为数十亿用户翻译超过一万亿个单词。

从「把文字翻成文字」，到「拍张照翻菜单」，再到今天「把你说的话实时变成另一种语言的声音」，这条路走了整整二十年。

当然，话别说太满。

谷歌官方自己也标了限制：目前只吃音频输入；遇上重口音、快速来回切语言、好几个人抢着说、或者长时间停顿，声音复刻还可能不稳。

它不是终点，但是一个相当能打的起点。

方向已经很清楚了。同声传译曾经是顶尖译员才扛得下来的活儿，一小时几千块，还得提前一周备稿。

现在，它正变成耳机里一个默默运转的功能，随叫随到。

当语言不再是墙，剩下的，就只有人和人想不想聊了。

参考资料：

https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/

https://deepmind.google/models/model-cards/gemini-3-5-audio/

https://ai.google.dev/gemini-api/docs/live-api/live-translate

https://x.com/JeffDean/status/2064400689825288351

编辑：所罗门

**秒追ASI**

**⭐****点赞、转发、在看一键三连****⭐**

**点亮星标，锁定新智元极速推送！**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4d80689a0a4e5d39176224ba829acc3e?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kGQp5tc0SgP1vNxdMx0wy8YoWew%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3e90be2e63fb4d08bc7ed8d3c073cfe7?Expires=1783831142&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SB4tE0y%2BXiyuLW5DUD4J2YgpTb0%3D)
