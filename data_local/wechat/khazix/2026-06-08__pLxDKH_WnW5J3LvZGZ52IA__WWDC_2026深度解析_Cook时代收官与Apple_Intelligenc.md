---
title: "WWDC 2026深度解析：Cook时代收官与Apple Intelligence战略落地"
channel: wechat
src_id: khazix
item_id: pLxDKH_WnW5J3LvZGZ52IA
source_url: https://mp.weixin.qq.com/s/pLxDKH_WnW5J3LvZGZ52IA
note_id: 1912601647970583096
task_id: 6a2bb4434f25f709ed3d3f64
task_elapsed: 60
fetched_at: 2026-06-12T07:26:07.854990+00:00
summary_len: 3316
body_len: 17276
---

# WWDC 2026深度解析：Cook时代收官与Apple Intelligence战略落地

> 原文: https://mp.weixin.qq.com/s/pLxDKH_WnW5J3LvZGZ52IA

## AI 总结

### **👋 Cook时代收官（背景）**

**历史性时刻**
- **告别舞台**：2026年WWDC是Tim Cook作为苹果CEO的最后一次发布会，其将于**2026年9月1日**正式卸任，由硬件工程高级副总裁**John Ternus**接任。
- **发布会基调**：整体延续苹果"不惊不喜，稳稳当当"的风格，核心主题围绕**AI技术落地**，但中国区用户面临**功能可用性限制**。

### **🔧 Apple Intelligence新架构（底层技术）**

#### **1. 与Google Gemini深度合作**
- **技术架构**：基于**Apple Foundation Models**与**Google Gemini Models**联合开发5个AI模型，实现端侧与云端协同运行。
- **云端基础设施**：采用**Private Cloud Compute**架构，运行于苹果自研芯片，基于iOS裁剪的专用操作系统，核心承诺：**端到端加密、数据即处理即删除、工程师不可访问**。
- **战略逻辑**：苹果承认在大模型基础能力上落后第一梯队，选择"购买优质底座+系统集成优化"的务实路线。

#### **2. 双端侧模型配置**

| 模型名称 | 参数规模 | 支持设备 | 核心能力 |
| :------- | :------- | :------- | :------- |
| **AFM 3 Core** | 3B（小模型） | 所有支持Apple Intelligence设备 | 基础AI功能 |
| **AFM 3 Core Advanced** | 20B（MoE模型） | iPhone 17 Pro/Pro Max/Air、M4+ iPad（≥12GB内存）、M3+ Mac（≥12GB内存） | **语音交互、高精度听写** |

#### **3. 系统编排器（System Orchestrator）**

作为Apple Intelligence的调度中心，协调四大系统级能力：
- **个人上下文理解**：通过Spotlight语义索引整合设备内容（照片、邮件、备忘录等）
- **广泛世界知识**：联网搜索+Private Cloud Compute生成回答
- **App Actions**：通过App Intents框架调用第三方应用功能
- **屏幕感知**：结合当前屏幕内容提供上下文相关回答

#### **4. 隐私保护策略**
- **核心主张**："AI中的隐私是不可谈判的"（We believe privacy in AI is non-negotiable）
- **技术实现**：端侧处理+Private Cloud Compute，数据不存储、不可访问，支持外部专家审计

### **🗣️ Siri AI（核心应用）**

#### **1. 核心能力升级**

基于Apple Intelligence架构实现五大场景突破：
- **多任务连续对话**：演唱会查询→购票提醒→播放歌曲的连贯执行
- **上下文融合**：照片识别地点→关联联系人地址→规划导航路线
- **媒体智能管理**：按时间/人物筛选照片→自动添加至共享相册
- **复杂任务处理**：世界杯观赛派对规划→生成菜单→群发邀请
- **跨文件分析**：Mac端Spotlight集成，支持多格式文件对比分析+邮件生成

#### **2. 新语音体验**
- **自然语调**：支持设备（AFM 3 Core Advanced）具备更自然的语音表现力和语调变化
- **自定义设置**：可调节语音风格、表现力和语速

#### **3. 全系统听写升级**
- **精准度提升**：拼写、标点和大小写识别更准确
- **全场景支持**：内建于系统键盘，适用于所有App

#### **4. 视觉智能（Visual Intelligence）**
- **相机Siri模式**：实时分析拍摄内容，支持账单分账、随身行李尺寸判断等场景
- **信息提取**：结合产品信息与个人数据提供决策支持

#### **5. 写作工具集成**
- **全场景文本生成**：任何输入框可用自然语言描述生成文本
- **风格适配**：根据联系人沟通历史调整邮件/消息语气
- **自动校对**：全系统实时拼写和语法检查

#### **6. 跨平台扩展**
- **独立App**：首次推出Siri独立应用，保存对话历史并支持跨设备同步
- **多系统覆盖**：扩展至watchOS（直接语音交互）和visionOS（3D可视化界面）
- **语言支持**：初期仅支持英语，欧盟和中国区暂不可用

### **📱 APP智能化（场景落地）**

#### **1. Safari浏览器**
- **智能标签页整理**：按主题自动分组标签页
- **Notify Me**：自然语言设置网页变化监控（商品补货、报名开放等）
- **Describe an Extension**：自然语言生成自定义扩展

#### **2. 密码App**
- **自动密码更新**：Apple Intelligence+Safari协同完成网站登录与密码修改

#### **3. 信息与邮件**
- **上下文建议**：自动推荐创建提醒、搜索照片等操作
- **智能行动建议**：基于邮件内容推荐第三方App操作

#### **4. 日历与电话**
- **自然语言创建事件**：自动识别联系人、地点并填充详情
- **Call Context**：调用相关App信息（如航空公司确认码）辅助通话

#### **5. Home与快捷指令**
- **家庭监控智能化**：合并摄像头通知、自然语言搜索录像
- **AI生成工作流**：自然语言描述创建自动化流程（如离开公司时发送ETA）

### **🎨 创意与影像（AI增强）**

#### **1. Image Playground升级**
- **风格扩展**：支持写实风格生成，基于Gemini模型提升质量
- **交互优化**：照片库人物生成、触摸手势编辑、多画幅支持

#### **2. Photos AI编辑三件套**
- **Cleanup**：增强干扰物去除能力，复杂场景填充更真实
- **Extend**：扩展图片边界，调整画幅时保留关键内容
- **Spatial Reframing**：拍完后重新调整构图，模拟相机移动效果

### **🛠️ 开发者工具（生态建设）**
- **Xcode增强**：一键本地化、模拟器交互、多AI模型选择（含Gemini）
- **Foundation Models Framework**：支持图像输入，扩展自定义Skills
- **Core AI Framework**：全新框架，支持在Apple Silicon上运行第三方模型

### **✨ 体验升级（系统优化）**
- **Liquid Glass调整**：优化模糊算法，新增透明度滑块
- **性能提升**：App启动速度+30%，照片显示速度+70%，隔空投送速度+80%
- **搜索重建**：实时索引、邮件排名优化
- **跨平台功能**：iCloud共享相册支持Android/Windows，AirPods自定义EQ

### **📝 补充细节**
- **国区限制**：Siri AI及其他Apple Intelligence功能因监管要求暂不可用，具体时间未知
- **Agent能力缺失**：Siri AI演示未展示自主规划、多步任务执行等高级Agent功能
- **无障碍支持**：VoiceOver环境描述增强、Magnifier与Siri集成、Voice Control自然语言交互
- **Cook时代遗产**：以乔布斯"向疯狂家伙致敬"的名言收尾，标志苹果进入新管理层

## 原文 / 逐字稿

刚刚，苹果的WWDC 2026结束了。

这是Tim Cook作为CEO最后一次站在WWDC的舞台上了，9月1号，他就会把位置交给硬件工程高级副总裁John
Ternus，所以今年这场，多少带了点告别的意思。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff8bf8d154bf91bbfff9f7948dc83ccdb?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=pwSYsIX4CaeqT%2BHx3Pa5KMR7dbM%3D)

但发布会本身，坦率的讲，还是那个苹果。

不惊不喜，稳稳当当。

整场下来最大的主题就一个，还是AI，比如跟Gemini的合作终于落地了，比如Siri终于有了个AI的后缀，比如各种IOS的APP，也都往AI化的方向一步步集成。

不过苹果还是那个苹果，动作慢的可怜，并且最难崩的依然是国区几乎都不支持。

原话是：

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff32bf2369c735d21bc56f73510fd3677?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=irsXpFW%2FhOKA%2BougrECpWbCPNWQ%3D)

不过，这些功能的更新还是值得一看的，以及国内到底苹果会跟谁合作，还是一个意思的话题。

我也通宵给大家蹲完，然后整理完了。

希望对大家有用。

**一. Apple Intelligence新架构**

先说底层，因为后面所有AI相关的东西都建立在这套新架构上。

1. 跟Google Gemini的深度合作

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F14ff924905755f4afe04ef7e54847bf7?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FNIqqoiLukVwZg7GA5ODuCkk6p0%3D)

这次苹果也终于官宣了。

Apple Foundation Models的新一代是跟Google合作，基于Gemini家族一起来做的，搞了5个模型，然后苹果把这些模型适配到了端侧运行和Private Cloud Compute服务器上运行。

Private Cloud Compute就是苹果专门为AI搭建的一套云计算基础设施，跑在苹果自研芯片上，用的是一个从iOS裁剪出来的专用操作系统。核心承诺是，你的数据端到端加密，只用于处理你的请求，处理完立刻删除，不存储、不留痕，连苹果自己的工程师也看不到你的数据。

再细节的参数啥的就没说了，反正就是苹果承认了自己在大模型基础能力上追不上第一梯队，选择花钱买他们认为对普通消费者来说最好的底座，然后在上面做自己擅长的系统集成和体验设计。

策略上说得通，面子上。。。

面子有啥用你说对吧。

2. 双端侧模型

苹果今年的端侧模型分了两档。

所有支持Apple Intelligence的设备都有一个基础版端侧模型。但在能力强一点的的Apple设备上，比如iPhone 17 Pro、iPhone 17
Pro Max、iPhone Air、M4 及以上且至少 12GB 统一内存的 iPad、M3 及以上且至少 12GB 统一内存的
Mac，苹果额外部署了一个更强的第二版。

这两个端侧模型分别是：

AFM 3 Core，一个3B的小模型。

**AFM 3 Core Advanced，20B的MoE模型。**

这个更强的模型多出来的核心能力是**语音和更高精度的听写等功能**，它能听懂语音也能生成语音。

所以像Siri更有表现力的新声音、更精准的全系统听写这些功能，都只有跑得动第二版模型的设备才能用。

3. 系统架构

有了模型之后，对模型的调度还是需要一些设计的。

苹果做了一个叫系统编排器（System Orchestrator）的东西，它是整个Apple Intelligence的调度中心，负责协调四大系统级能。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fba17206da8ce7f85d2197e78e811de04?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wjGmHx0r7uWQfOWmNzYVcl7N%2FLQ%3D)

**人上下文理解**。你设备上所有的内容，照片、邮件、备忘录、消息，都通过Spotlight的语义索引被组织起来了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4faf119612bd92b0ddd32160119c793e?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=41%2FrHz1qNtMK4zQZXV%2FtayGkhsU%3D)

**广泛世界知识**。比如你问世界杯赛程是什么，系统编排器会让Apple Intelligence联网去搜索，然后通过Private Cloud
Compute来生成回答。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fedc0cad8503da018e47b094759c8c4d1?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1B2qA1N7KCnr%2FC3RyfwyP%2BNjvP4%3D)

**App Actions**。这是让Siri能动手做事的关键。系统编排器知道你手机上每个App能做什么（通过App
Intents框架），当你说发消息给某某的时候，它会调用Messages来执行。理论上，任何适配了App Intents的第三方App都能被Siri调用。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd22521685c0e9a8299c5e9723f0552ac?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7e5GR6N1tn2J5PnUZUMVH6WFDqU%3D)

**屏幕感知**。系统编排器能看到你当前屏幕上显示的内容。比如你正在Safari里看一篇文章，这时候问Siri一个问题，它能结合你正在看的内容来给出更相关的回答。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F63f501d7e62abfc2f0232b9e7c3d02ab?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xlkQGz2O40wanXWMQFcvMJj1LuM%3D)

这四个能力组合在一起，就是苹果所说的以你为中心的AI，也是硬件跟AI结合的一个比较完整的方案。

4. 隐私

他们的原话是：

We believe privacy in AI is non-negotiable.

我们认为，AI中的隐私是不可谈判的。

苹果的态度是，很多AI厂商在嘴上说隐私，但默认情况下都在保留你的个人交互数据，把保护隐私的责任推给用户。

苹果的方案就是前面说的端侧处理+Private Cloud Compute，数据不存储、不可访问，只用于执行请求，外部专家可以随时审计。

**二. Siri AI**

今天真正的重头戏，也是苹果最大的发布了。。。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbb668f9f3c78754b051102d082f7d288?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=R5CK8VhiFoD97PFsohyS8KM8zhA%3D)

给新版Siri正式命名为**Siri AI**。

1. 核心能力升级

Siri AI基于整套新的Apple Intelligence架构，集成了上面提到的很多的新能力。

苹果的说法是，Siri现在是一个“有了质的飞跃”的助手。

然后基于这次的新Siri AI，他们做了一些演示。

**演示一，问答+提醒+音乐。**

问“旧金山的某位歌手演唱会什么时候”→ Siri给出答案（7月26号）→ 追问怎么买票 → Siri说要抽签 → “抽签开始的时候提醒我”→ 设好提醒 →
“放一首她的新单曲”

**演示二，屏幕感知+个人上下文+路线规划**

看到一张照片问“这是哪”→ Siri识别出圣克鲁兹海岸的天然桥州立海滩 → “我朋友Jeff最近搬到附近了，他新家在哪”→
Siri从消息记录里找到Jeff发过的地址 → “给我导航到那个拱门，中间停一下Jeff家”→ Siri规划路线

**演示三，照片筛选+共享**

“给我看上周在沙斯塔山的照片”→ Siri搜索照片 → “只把有Bryce、Madison和Quinn的照片加到家庭共享相册”→ 完成

**演示四，对话式体验**

查世界杯开幕周末赛程 → “我想为巴西vs摩洛哥那场办个观赛派对，给我两个国家的经典菜”→ Siri给出菜品（还带图片）→
“Maria最近提到的那个甜点是什么”→ Siri搜索消息找到椰子饼干→ “把这些整合成一个菜单”→ Siri生成创意菜单 → “发消息给Gold
Chasers群组问他们要不要来，附上菜单”→ 发送

**演示五，Mac上的对话式Siri**

Siri也集成进了Spotlight。

在Spotlight里输入问题就能启动跟Siri的对话，窗口可以拖拽和调整大小。

演示了让Siri分析多个不同格式的文件比较三个棚子的报价，然后结合儿子之前发的消息里提到的电路问题来做推荐，最后让Siri直接起草一封邮件给选中的供应商。

大概就是这样。

我的感受是，怎么说呢。

2026年了，Siri
AI的演示核心还是问答、搜索个人信息、发消息、设提醒这些事。对话式体验确实比以前强了不少，能连续聊、能带上下文了，但说实话，这些demo跟现在的ChatGPT、Claude比，谈不上什么惊喜。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9c9e7a070c00d0f2bd963635548a08ca?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=IB7mos2kTO%2FMrmmL%2FdjkLDDlBN4%3D)

最关键的是，没有看到真正的Agent能力。也没有看到Siri自主规划、自主执行多步任务、自主调用多个App完成一个复杂目标的场景。

苹果说了App Actions，但演示里最复杂的也就是搜索照片→筛选→加到共享相册这种程度。

这块确实是有一点失望。

### 2. 新语音体验

在支持第二个强端侧模型的设备上，Siri有了全新的语音。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3af7f7db0f178a1205ab78031c478205?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=TJjp7Q0wFgsmEAenoOpuYuuOOEQ%3D)

更有表现力，语调变化更自然。

苹果还让你可以自定义Siri的语音风格，调表现力和语速，更亲切更好玩一点。

### 3. 全系统听写升级

同样需要第二档端侧模型，新的听写引擎在拼写、标点和大小写上都更精准了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0212acfc89778a59cf3bfdfb13ae1c72?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=pZQpgc7vLaLBTYJpRNLrLilUlpM%3D)

因为它是内建在系统键盘里的，所以不管你在哪个App里，只要调出键盘就能用。发布会上提到的场景是“在地铁上用语音发消息”和“边想边说地用日记App记录”，都是日常会用到的，这个我觉得还是比较刚需的，好评。

### 4. 视觉智能

iPhone上，Visual Intelligence（视觉智能）集成进了相机App，新增了一个Siri模式。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1b4a667b2390cf7b30489abf56c8135f?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zNj6eXtfqXWkIHK8rhpaWChW%2F4E%3D)

按快门键让Siri看到你看到的东西，然后给你有用的回应，可以下拉查看详细信息、问后续问题。

比如苹果演示的，对着账单拍，选择你点的菜，用Apple Cash跟朋友分账。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fa8c58979c3575d3345b477a363698b1c?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=VGDO936B76yq8mI8PK1eoiha020%3D)

或者看着一个背包问“这个能当我9月航班的随身行李吗”，Siri结合产品信息和个人航班信息回答。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fdef2921ba7d84c48a5c6f0d39f3d3ccd?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yKYu%2BSu0QYXktwgaGfoCm2iznUg%3D)

### 5. 写作工具 + Siri集成

写作工具现在更深度地跟Siri结合了，你可以在任何能打字的地方用自然语言描述让Siri从头生成文本。

在邮件和信息里，Siri还能根据你跟特定联系人的沟通风格来调整语气。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff54fe72dfe7eb99c8f1e5e6efb1a4d04?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ahK0T6Cc33XaVWZc5hduKXStjf8%3D)

另外，Apple Intelligence现在全系统自动校对了，你在任何App里打字，它都会自动检查拼写和语法，不用你手动触发，大多数第三方App也支持。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F32186fb675a523d1fe117ea99669e0cb?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4SXoyBgdfSZhaEGup2X47pr3oEw%3D)

### 6. Siri独立App + 跨平台

苹果给Siri做了一个**独立的App**，这是第一次。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F24cec9a3ab06d6285087761d8462527a?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MFb8A6uH0xeFBDwqWsqZslS1lUk%3D)

现在有了独立App之后，你所有跟Siri的对话都会被保存在这里，可以随时回看。

最重要的是跨平台同步，你在iPhone上跟Siri聊了一个话题，打开iPad上的Siri App可以看到这段对话，继续往下聊，在Mac上也一样。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff36672b0ebbad618569e665722dd27e8?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ubzCFDQSL4JL8u%2FOsyoW2Gm29p4%3D)

对话历史通过iCloud加密同步，苹果看不到你的对话内容。

Siri AI还扩展到了watchOS（手腕上直接问）和visionOS（3D可视化的Siri，放在你空间里的任何位置，看着它说话就行，不用说「hey
Siri」）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Feb3f663796565f1f3638b957870867f5?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=LYKLnTFFWjp%2B84rdY2uw9hGMjWc%3D)

然后新版的Siri，目前只支持英语，后续会扩展其他的语言，欧盟和中国都目前不可用，可用时间未知。

**三. APP智能化**

反而是我今天觉得比较惊喜的部分。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F975863fb4ac7e68735fd4bbae92d1a04?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jV2OkvuXzDJ4h5AHuTT2BLqmPqQ%3D)

让AI渗透进所有人的生活中，确实还是得从老的APP改造入口，是最能进日常场景的。

1. Safari

三个新功能。

**智能标签页整理**，Safari用Apple
Intelligence分析你打开的每个页面，自动按主题分组。你浏览的时候，相关新标签页会自动归到对应主题下，可以一键关掉整个主题或者存为标签页组。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F907610e1bd997d0a5a255737b62bddff?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=QluQXk8COFji2QOhD63uy61vW20%3D)

**Notify
Me**，你可以用自然语言告诉Safari你在等什么变化（比如某个商品补货、某个报名开放），然后关掉那个标签页，Safari会自动监控，变化发生时推送通知。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe1c756ed09d01999778fbceefe83501a?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=h2eTsOnuvH%2Fb1lZirP%2FhX9V8ptY%3D)

这个功能太实用了，不知道执行效果怎么样，但思路是对的。

**Describe an
Extension**，用自然语言描述你想要什么，Safari帮你生成一个自定义扩展来调整网页内容，比如在工具栏加一个按钮来保存和评分你试过的食谱。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F76eb0dfac0e6e6d1177adc00de6f8a44?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=tA9Q7f1UgvgLBCkCdSZu9%2FSVuC0%3D)

还有一条，Safari所有智能功能都不追踪你的浏览数据，不跟任何人分享，包括苹果自己，然后稍微内涵了一下友商。。。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fde512a4f0631a8486798e5bc35755ae8?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GIVw4pTAi0BDhL2dNqZZaNyyKLQ%3D)

“不像某些浏览器”。

### 2. 密码App

密码App现在已经能提醒你弱密码和泄露密码了。

新功能是，它现在能自动帮你更新密码，背后是Apple Intelligence和Safari配合，自动导航到对应网站、登录、改密码。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7b6053e9c21ac7aac3bd463c0d4c23f0?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=zFjugfYPiC3%2FfY7gI4%2BACQBZS1A%3D)

一个“agentic”的动作，难得见到苹果用这个词。。。

### 3. 短信

Messages现在能理解对话上下文，提供一键建议。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe496cb8d1bb577259ffdac0304460fba?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=AXwDfGGmN%2B26N7WJtbzLGx%2FW234%3D)

比如有人提到某个事，Messages会建议你创建提醒或备忘录，有人问你要照片，Messages帮你根据关键词、地点和人名搜索最合适的照片。

### 4. 邮件

邮件也有了更智能的上下文建议，让你快速用喜欢的App（包括第三方App）采取行动。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F64e4dd592f00cf1ab3aedfa96975ae9a?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=A3RIwMSWlgrUphmPI7oN1IYAMUU%3D)

### 5. 日历

可以用自然语言添加事件了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9e2674e20a6042c34328bba2eec7c888?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=9cL3olbIhpSCiFa%2BZQcx1QW%2BWXU%3D)

你打字的时候，日历会自动识别联系人、地点，填上标题。

编辑也更智能，比如把“每周”改成“每两周”，日历自动调频率。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F54d896a03377d4f54242e6bd01e1fd55?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=a3dvgPR4u6tEuO6cddgI%2BcCFibc%3D)

### 6. 电话

苹果把这个电话的功能叫**Call Context**。

这个是我的刚需。

打电话给商家的时候，电话App可以主动从你其他App里找相关信息。比如你打电话给航空公司改机票，它能自动从邮件里找到你的确认码。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F603fcdde0422b26a0c23d5396fef1f98?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=BeMh7gYIvoLOAgyNZgX1ZdH8zNU%3D)

而且全部端侧运行，看的是你打给谁。

但是咱就是说，新AI上国内的时候，咱能不能把那些恶心的营销电话也都用AI处理一下。。。

### 7. Home

家庭App可以支持用Apple Intelligence理解摄像头通知，把相关的通知合并成一个持续更新的活动通知。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc1bf66f75c2213f464ec21374ba670de?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nZG58NTBd%2BwHPAsHEauVbtVI6x4%3D)

还能分析录像片段，生成描述，支持用自然语言搜索录像内容（比如搜快递），支持4K分辨率回放。

### 8. 快捷指令

这个更新也挺好的，类似飞书的AI生成工作流。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F807ce85e22d7d1689852412173e13944?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GG7f%2BWyjRNGh%2ByQ9wBI1DU4d3dw%3D)

快捷指令现在支持用自然语言描述你想要的自动化，Apple Intelligence帮你组装所有步骤。

演示里的例子是，“当我离开公司时，发消息告诉佩德罗我在路上，附上到家的预计时间”→ 快捷指令自动创建了一个自动化，检测离开公司地址 → 用地图计算到家时间 →
用信息App发送。

还能追加描述来调整，比如自动播放最爱的播客。

**四. 创意与影像**

这块苹果也用AI雕了一些有意思的花。

1. Image Playground大升级

Image Playground这次大幅升级了一下。

核心变化，支持写实风格了，之前只能生成那种卡通/插画风格，现在用Private Cloud
Compute上的跟Gemini搞的新生成模型，可以做高质量的各种风格图片。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F55e4d3a63f4e3ada0840e483ac89f3aa?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=f1I4UtU%2Bqt3YoWxnH2RE%2B8eShjI%3D)

毕竟你都用Gemini了，生图再不迭代一下，那就真说不过去了。

你可以用照片库里的人来生成图片，用自然语言描述修改，用触摸手势圈选对象来移动/缩放/修改。

还能选择不同的画幅，生成联系人海报和锁屏壁纸。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F94c553ca9ff17717060968a5faa58e21?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4rtXDPiFAc6IrZW8mDOirwZMPhk%3D)

同时，给开发者也开放了Image Playground API。

### 2. Photos AI编辑三件套

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F879c7b9fbf451e74ac1d237154cc3b0f?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=c9JCuGWAoX518a4yM1v9aAsfGnE%3D)

**Cleanup升级**，去除干扰物的效果更好了，复杂场景下的填充更真实。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F87ad15daffef1d6b297fde44b44df1c1?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=xwjJhjPB5DXXtQFg8YQWmcWsWqE%3D)

**Extend**，扩展图片边界，给主体更多空间，或者调整画幅时不用裁掉重要内容。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F13e9fd1d0d1ca9126f64ce7ef29c9560?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1p3q55Mcf1Pt78gNmfKiPp%2FVC7k%3D)

**Spatial
Reframing（空间重构）**，这个是今年Photos里最酷的新功能。你可以在拍完之后重新调整照片的构图，就像你在拍照那个瞬间移动了相机一样。

它用的是端侧的空间模型做实时预览，然后用Private Cloud
Compute上的生成模型来填充透视变化产生的新区域。只生成空白区域的内容，原始照片的部分保持不变。

演示效果确实不错，而且这个功能基于Apple Vision Pro积累的空间理解技术，对老照片和其他相机拍的照片也能用。

**五. 开发者工具**

1. Xcode

苹果说Xcode是做agentic coding最好的地方。。。

我一直不知道该从哪开始吐槽起。。。

反正这次也做了一些更新，也基本围绕的着AI。

比如它现在能一键把你的整个App本地化成其他语言，能跟模拟器里的虚拟设备直接交互（以前只能看代码），还支持自定义skills来扩展助手的能力。

然后呢Xcode的代码助手现在**可以选择不同的AI模型**了，包括Google的Gemini。。。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbcdf7bd11a26b64032501f5e774caa06?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wsZ%2FWWf9nSyIX0ojPRt%2F2WkZ9Mg%3D)

我朋友当时就吐槽了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F27ad0556925e59c39c0a324b81277ae3?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cCsscrE61SwT9HQr0N4iHwVqw8o%3D)

你还可以把它跟Figma和GitHub这样的外部工具连起来，让代码助手能够参考设计稿和代码仓库。

测试方面，苹果推出了全新的**Device Hub**，把所有模拟设备和真实设备统一到一个界面里。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcc191787e2fca6eff0444596fdafc3be?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=460hJQnCeHuB%2FquMzAwKDhiUK7c%3D)

你可以在里面模拟多点触控操作，一键切换App的深色/浅色模式，还能动态调整App的窗口大小来测试不同屏幕尺寸下的表现。

2. Foundation Models Framework

开发者可以在App里用Apple的端侧模型，今年新增了图像输入（之前只有文本），支持自定义Skills扩展模型能力，还能用同一套Swift
API调用服务器端的模型。

### 3. Core AI Framework

全新框架，可以在所有苹果平台上用Apple
Silicon的全部算力来本地运行其他模型。这个对开发者来说可能是最实际的，意味着你可以把自己的模型或者第三方模型直接跑在设备上。

**六. 体验升级**

就是一些偏系统偏设计的了，跟AI关系不大了。

1. Liquid Glass优化

去年WWDC最爆的就是Liquid Glass这套全新设计语言。

好看是真好看，但争议也不小。

苹果今年也说去年太激进了，所以在IOS27上，底层优化了Liquid Glass的模糊算法，对复杂背景的弥散效果好多了。

也加了一个**透明度滑块**，现在，你可以自己调Liquid Glass的透明度。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc04be950a6ac9aad32fc8611e44b9fcf?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hFVduRjbz6ptycfIG9xEJKNBNG4%3D)

macOS上还做了几个调整，工具栏更统一了，侧边栏延伸到窗口边缘，侧边栏图标恢复了彩色，所有窗口统一了更紧凑的圆角，App图标也迭代了一版，在图标内部加了多层Liquid
Glass折射效果。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2e613e3b07315a4969fe66e877b69a34?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=AFJaiKnhAQ8tXUs%2B8MhVf2h3b6I%3D)

2. 性能提升

常规操作，比如iPhone和iPad上App启动速度快了**30%，新拍的照片在图库里出现的速度快了****70%，隔空投送传文件速度快了****80%，iPad接外部硬盘浏览和传输文件速度快了****5倍。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9d0aac8331a2cd1209e91b92d5fb6a1b?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=3aU35O0reFaUT%2FvOyZZtGBpTMqI%3D)

**3. 搜索基础设施重建**

**苹果重建了聚焦搜索、照片和邮件背后的搜索索引，让它更稳定、更全面。**

**新内容几乎实时入索引，邮件搜索还加了全新的排名系统，置顶结果更准了。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F12be9f2213a7dec0042771aba8e14bd6?Expires=1783841166&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=70UDAK3AjThmNZxUFJxNGIYR1vE%3D)

**4. 其他小更新**

****照片，iCloud共享相册终于支持Android和Windows用户加入了，还支持全分辨率共享。****

****AirPods，支持自定义EQ了。****

****Apple Vision Pro，全景照片可以变成有深度的空间场景。****

****地图，Flyover大幅升级，航拍影像+视觉智能模型，建筑细节和树木形态都清晰得多。****

****网络切换，iPhone更智能地判断什么时候该从Wi-Fi切回蜂窝（终于不用手动去控制中心关Wi-Fi了）。****

****信息App，低带宽环境下发大文件不会卡住对话了，会显示发送进度。****

****无障碍，苹果官网上列了不少Apple Intelligence在无障碍方面的集成。****

****VoiceOver现在能更丰富地描述周围环境和屏幕内容，Magnifier可以放大后直接问Siri，Voice
Control更灵活了，可以用自然语言跟App交互。****

****这块发布会上没提，但确实是AI落地到实际场景里的好例子。****

**写在最后**

今天WWDC算是平稳结束了。

这也是Cook最后主持的一届WWDC了。

苹果，这个伟大的企业，终于要交接到了下一棒人手中去。

最后，我想用我特别特别喜欢的乔布斯的一段词结尾：

*"***向那些疯狂的家伙们致敬。**

*他们特立独行。*

*他们桀骜不驯。*

*他们惹事生非。*

*他们格格不入。*

*他们用与众不同的眼光看待事物。*

*他们不喜欢墨守成规。*

*他们也不安于现状。*

*你可以认同他们，反对他们，*

*颂扬或是诋毁他们。*

*但唯独不能漠视他们。*

*因为他们改变了寻常事物。*

*他们推动人类向前迈进。*

*或许他们是别人眼里的疯子，*

*但他们却是我们眼中的天才。*

*因为只有那些疯狂到**以为自己能够改变世界的人，*

*才能真正改变世界。"*

******以上，既然看到这里了，如果觉得不错，随手点个赞、在看、转发三连吧，如果想第一时间收到推送，也可以给我个星标⭐～谢谢你看我的文章，我们，下次再见。******

>/ 作者：卡兹克、chiyo

>/ 投稿或爆料，请联系邮箱：wzglyay@virxact.com
