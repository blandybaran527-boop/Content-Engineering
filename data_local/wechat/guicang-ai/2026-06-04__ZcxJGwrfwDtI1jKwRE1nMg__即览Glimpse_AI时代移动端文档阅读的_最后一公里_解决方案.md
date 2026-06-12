---
title: "即览Glimpse：AI时代移动端文档阅读的「最后一公里」解决方案"
channel: wechat
src_id: guicang-ai
item_id: ZcxJGwrfwDtI1jKwRE1nMg
source_url: https://mp.weixin.qq.com/s/ZcxJGwrfwDtI1jKwRE1nMg
note_id: 1912585720084184816
task_id: 6a2b7a5158fc21add351adab
task_elapsed: 40
fetched_at: 2026-06-12T03:18:27.981283+00:00
summary_len: 1855
body_len: 7834
---

# 即览Glimpse：AI时代移动端文档阅读的「最后一公里」解决方案

> 原文: https://mp.weixin.qq.com/s/ZcxJGwrfwDtI1jKwRE1nMg

## AI 总结

### **📱 产品概述：解决移动端文档阅读痛点**

**核心功能**  
- **产品定位**：手机上的 Markdown/HTML 阅读器，专注解决 AI 生成内容在移动端的查看难题。  
- **支持格式**：.md、.markdown、.html、.htm、.txt 及网页资源打包 ZIP。  
- **核心特性**：本地渲染、本地保存，无需上传文件或注册账号。  
- **获取方式**：提供 TestFlight 测试名额（8000个）。

### **🔄 AI时代的内容格式变革**

#### **(一) Markdown：AI交互的「谢林点」数据层**
- **定义**：Schelling point（谢林点）——无人强制但自然形成的共识选择。  
- **AI适配性**：  
  | 优势 | 具体说明 |  
  |------|----------|  
  | **轻量** | 纯文本格式，模型读写效率高 |  
  | **结构化** | 支持标题、列表、表格、代码块等多层级表达 |  
  | **开放性** | 无复杂格式封装，人、AI、工具均可直接处理，版本管理清晰 |  
- **应用案例**：CodePilot 以 Markdown 文件作为记忆系统，实现「人-AI-工具」协同。

#### **(二) HTML：AI内容的视觉展示层**
- **核心价值**：作为 Markdown 的互补格式，解决长文本可读性问题。  
- **展示优势**：  
  | 维度 | HTML特性 |  
  |------|----------|  
  | **信息密度** | 支持排版、图表、交互，提升内容消费体验 |  
  | **视觉层级** | 通过颜色、空间布局强化信息传递效率 |  
  | **兼容性** | 无需依赖特定软件，打开即可查看 |  
- **典型案例**：开源 PPT Skill 生成网页形式演示文稿，25天获1万 Star，验证 HTML 在展示场景的实用性。

### **📱 移动端阅读的「链路断裂」问题**

现有工具在移动端处理 Markdown/HTML 的局限性：  
| 工具类型 | 核心问题 |  
|----------|----------|  
| **即时通讯（如微信）** | 优先级为聊天/转发，非专业阅读，易出现格式错乱或无法打开 |  
| **浏览器** | 设计目标为「链接-网页」场景，本地文件处理流程繁琐 |  
| **编辑器/笔记工具** | 侧重编辑功能，需导入/建库/注册，不适合临时查看 |  
| **安全风险** | HTML 文件可能含脚本，默认执行存在隐患 |

### **✨ 即览Glimpse的核心功能设计**

#### **(一) 三大核心能力**
1. **打开**：支持从微信、文件 App 或系统分享面板直接调用，自动识别并解压 ZIP 资源包。  
2. **阅读优化**：  
   - **Markdown**：支持字号/行距调整、长表格横向滚动、目录跳转、Obsidian 语法兼容（任务列表、Callout 等）。  
   - **HTML**：本地 WebView 渲染，默认关闭动态脚本（可手动开启），支持缩放、横竖屏切换及设备模式切换。  
3. **管理**：自动保存历史记录，支持收藏，重复导入不生成冗余文件。

#### **(二) 产品边界**
- **不支持功能**：云同步、账号系统、编辑功能、AI 集成。  
- **设计理念**：先做精「打开-阅读」核心场景，再扩展其他能力。

### **🔗 产品定位：AI内容生产链路的关键补充**

即览在 AI 工作流中的角色：  
1. **上游**：衔接 CodePilot（Markdown 数据层）与 PPT Skill（HTML 展示层）的内容生产环节。  
2. **下游**：解决移动端「生成-传输-阅读」链路中的断点，实现内容消费的「最后一公里」闭环。

### **🚩 未来挑战与扩展方向**
1. **文件管理**：整合分散在手机、网盘、聊天记录中的 Markdown/HTML 文件。  
2. **分享机制**：优化 HTML 内容的跨设备分发（如免部署链接生成）。  
3. **跨设备协同**：实现手机与电脑间的阅读进度同步，平衡隐私与便利性。

## 原文 / 逐字稿

之前预告过的那个「手机上的 Markdown / HTML 阅读器」做完了,叫 即览。

它解决的是一个很小、但最近越来越烦的问题

别人从微信、文件 App 或群里发你一份 AI 报告、网页 PPT、Markdown
文档,手机上点开不是空白,就是源码,要么样式全坏,要么根本不知道该用什么打开。

.md、.markdown、.html、.htm、.txt,还有打包好的网页 ZIP,都可以直接用即览在 iPhone 和 iPad 上打开。

本地渲染,本地保存,不需要上传,也不需要注册账号

文末有 TestFlight,想试可以直接申请,我开了 8000 个名额。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe7cb49fa59bdec5965addd3d6ec1b7d2?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FJHg8zYEENRkghBnMw09yyUipbw%3D)

但我做即览,不只是因为缺一个阅读器。

更直接的原因是:这段时间我越来越明显地感觉到,在 AI 参与内容生产之后,我们交换内容的格式正在变。

很多文本内容开始落到 Markdown,很多展示内容开始落到 HTML。

即览只是这个变化走到手机端时,掉出来的一个小工具。

## Markdown 不只是文本格式,它正在变成 AI 的数据层

前几天看到 Obsidian 作者的一句话,我觉得很准:.md 正在成为 AI 文件交互里的一个 Schelling point。

**Schelling point**:可以翻译成"谢林点",意思是没有人强制规定,但大家会自然聚到同一个选择上。

Markdown 现在就有点像这样。

没人规定 AI 应该用 Markdown,标准委员会也没有出来宣布过什么。

但在真实使用里,不管是人写给 AI,还是 AI 写给人,最后经常都会落到 .md 文件上。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F679702355f310cc89cfc43b765e8b2d9?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=CZJlF%2FRBxaY3wP2gJ7xknnE3uIk%3D)

原因也很朴素。

**轻量**:它是纯文本,模型读写都轻。

**结构**:它有足够的结构,标题、列表、表格、代码块、链接都能表达。

**开放**:它又不会像 .docx 那样被包进一层复杂格式里。人可以直接打开,AI 也可以直接处理,版本管理和 diff 都干净。

它更像是 AI 工作流里的底层数据

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F014765c2867730591e9fbe460e66d8d8?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=z6HKUzHzXICj80YVF3YSM6Qnd%2BM%3D)

我在 CodePilot 里就是这么用的。

它没有特别复杂的 memory 机制,很多记忆其实就是一组 Markdown 文件。

AI 往里写,AI 从里读,我自己也能打开改。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0f13fb478ec49ec887e21af1ad875a1a?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=BC6XHSS2zjtOrP6ZWlQrtJ2MytE%3D)

更进一步,CodePilot 里的 widget 也可以把这些本地 Markdown 和 memory 当作数据来源。

文件变了,组件展示也跟着变。

这时候 Markdown 就不只是"拿来读的一篇文章"了。它变成了一种很轻的本地数据层:人能看,AI 能读,工具也能基于它生成新的界面和交互。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F594091bf8f3b678b455006d726352cb7?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=yK73BTAHRoQDHYO6mtKPStKG7j8%3D)

这也是为什么我觉得,最近很多人继续卷 Markdown 编辑器,方向可能有点窄。

真正有意思的不是再做一个更漂亮的编辑框,而是把 Markdown 当成数据,去构建新的阅读、管理和人机交互方式。

## HTML 正在变成 AI 内容的展示层

另一端是 HTML。这个趋势最近也越来越明显。

上个月我开源了一个 PPT Skill,生成的就是网页形式的演示文稿。

它 25 天到 1 万 star,后来我在线下答辩、展会和分享里,也反复见到有人用它做出来的 PPT。

这件事让我确认了一点:很多场景里,大家要的并不是一个标准的 .pptx 文件,而是一个能拿上去讲、能被人看懂、能快速分享的展示物。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5820d83e83763095db456cbbd0a23c5e?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Tb66JIFQS5gU0N0mTKo3hVyaP5M%3D)

刚好 Claude Code 团队最近也在讲同一件事。

他们有篇文章专门写为什么越来越多输出开始用 HTML,而不是 Markdown。

理由很直接:HTML 信息密度更高,更容易做视觉层级,更适合展示图表、布局、交互,也更容易被别人打开和阅读。

这跟我自己的体验很接近。

Markdown 适合沉淀内容,但它一长就难读。几千字、几万字的报告堆在一个 .md 文件里,哪怕结构是对的,人也很难真的读进去。

HTML 反过来。它可以用排版、空间、颜色、图表和交互,把信息组织得更像一个"可以被消费的东西"。它不是更适合存事实,而是更适合让人理解事实。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F554955f581525dab2568b31e8d1f964e?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=4VVzzx%2FJV0IltxtXWwnb5BDr%2Bds%3D)

Markdown 是数据层,HTML 是展示层

底层内容用 Markdown 留着,干净、可读、可版本管理。

需要给人看、给人讲、对外分享时,再渲染成 HTML。

这不是某种宏大的新标准,更像是 AI 工作流里自然长出来的一种分工。

## 但这条链路在手机上断了

内容有了,文件也发出来了,问题出在最后一步:人经常是在手机上打开它。

桌面端还好。你有浏览器,有编辑器,实在不行还有 VS Code。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F201188bd18dd04368e78582d343ebd4f?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=e7aO8tjLuSUWRdQNA0jYY8I0Bvc%3D)

但手机不是这样。

尤其是你在微信里收到一份 AI 生成的报告、一个网页 PPT、一个 Markdown 文档时,常见体验就是点不开、显示源码、样式坏掉,或者要在几个 App
之间来回跳。这件事很小,但非常烦。

微信这种 IM,本质上不是文件阅读器。

它的优先级是聊天、预览和转发,不是认真打开一个 Markdown 或 HTML 文件。

浏览器也不是为这个场景设计的。

浏览器默认处理的是"你给我一个链接,我帮你打开网页"。

但别人发给你的往往是一个本地文件,不是一个链接。你当然可以绕来绕去把 HTML 丢给浏览器,但整个链路又长又别扭。

很多 Markdown 工具也偏编辑、偏笔记,不一定适合临时打开别人发来的文件。

更不用说有些工具会要求你导入、同步、建库、注册账号。

HTML 还多一层安全问题:一个陌生文件里可能带脚本,你不一定希望它默认执行。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F43d7f69fa85b85bc9579ad5312e6ed1c?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jwgo31zNAxe6GrpjUXKS3z2ndao%3D)

在手机上,把 AI 工作流里常见的这些文件,安全、顺手地打开

这就是即览。

## 即览做得很窄:打开、读、收着

即览没有做成编辑器,也没有接 AI,顺便我必须得吹一下 CodeX 画的这个 App 图标,太可爱了。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F64ade1a31827562ba4c9c8578d69250e?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=MNCdCfpMEFvfz3iKu0V0tW6DO5M%3D)

我一开始就想得很清楚,它只做三件事:打开、读、收着。

收到文件时,从微信、文件 App 或系统分享面板里选择即览,就能打开。支持 .md、.markdown、.html、.htm、.txt,也支持网页资源打包成的
.zip。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc489c43313fee8aa258192836f2f301d?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=8zIfgR7Nz5c%2BQKYk23sDm45noqQ%3D)

所有文件都在本地处理,不上传,不注册账号

读 Markdown 的时候,我主要按长文阅读去调。

1

字号、行距、背景可以改

2

长表格可以横向滚动

3

有标题结构的文档可以用目录跳转

4

常见的 Obsidian 写法,比如任务列表、Callout、脚注、Frontmatter、标签,也尽量兼容

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0da61229d1b9da09258ae69b4dd7d075?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FHoYoNu8TQxwqwJf7FLF6n1d4ek%3D)

也支持夜间模式和颜色主题的切换。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7d2b82cd44c6cbd3f2b54340d7f0ed9a?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2npk7IqCCK9gpHA0FAQ3FnDexT0%3D)

读 HTML 的时候,我更在意"可控"。

它用系统 WebView 本地渲染,支持缩放、横竖屏切换,也可以在手机模式和桌面模式之间切。

动态脚本默认关闭。陌生 HTML 里到底有没有脚本,你通常是不知道的。所以即览默认不把执行脚本作为前提;遇到确实需要 JS 才能看的页面,再手动打开。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F91d6c43d26432864d38315068cb5a521?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Pcy1RuAkjg21fUyvwsphMAieA%2B0%3D)

ZIP 也是为真实场景做的。

很多 AI 导出的网页不是单个 HTML,而是 index.html 加一个 assets 文件夹。

即览会解压后自动找入口,本地图片和 CSS 也能正常加载,不至于样式全丢、图片全裂。

打开过的文件会自动留在本地历史里。下次想回看,进 App 就能找到。

重复导入同一个文件不会堆出两份,重要的也可以收藏。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Feb73b72d6bf99063e3ea6a5e8cb8444a?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=mZ71RZ1RK11MPGckWecBTAuHPn8%3D)

这就是它现在的边界。

它不做云同步,不做账号,不做编辑,也不接 AI。

不是因为这些功能不重要,而是因为一个查看器先应该把"打开并读完"这件事做干净。

## 即览接在前两件事后面

现在回头看,即览不是一个孤立的小工具。

上个月我做 PPT Skill,是因为我相信 HTML 会成为 AI 生成演示内容时很自然的一种形态。

它不一定取代 PowerPoint,但在"快速生成一个能讲的东西"这件事上,HTML 足够轻、足够开放,也足够适合模型直接生成。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F84360f28853f5bdbf87d74548c37aeac?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=HFfcpX%2FOqOu5h0Pfg6cIolfppNA%3D)

我做 CodePilot,是因为我相信 Markdown 会成为 AI 协作里很自然的数据和记忆载体。

它不是最漂亮的格式,但它最容易被人、模型和工具同时使用。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9ad1879bb5f5cd67a3db323d8a1ea234?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=91%2FC5umhWKVMIS%2BhGIPATeLkJ6w%3D)

即览接的是第三步:

这些格式不能只停在"生成出来"那里,还得让人真的能打开、能读、能收起来

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F698584d1d58a3cf5f71347468c767b79?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=2aFDFF6cdJG47gyt5T5pRSH5fhA%3D)

前两件事偏生产,即览偏消费。

AI 已经能生成 Markdown,也能生成 HTML。

但如果这些文件一到手机上就断掉,那前面的生成体验再顺,也没有真正落到人手里。

即览补的就是这个最后一公里。

## 但这件事还远没结束

即览现在补的只是最浅的一层:收到一个文件,把它打开。

再往后,其实还有几个问题没有解决。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F34c1989717d366db422d4bddef08c919?Expires=1783826307&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=R5%2BY31shfMBi37Il%2Bo4YzgSmn4o%3D)

•

管理:很多人的手机、网盘、聊天记录和各种 App 缓存里,已经散落着大量 Markdown 和 HTML
文件。它们不是没有价值,只是太分散,找不到,也管不起来。

•

分享:即览解决的是"别人发给我,我怎么看"。但反过来,"我做了一份
HTML,怎么让别人顺手打开",仍然麻烦。发文件,对方未必打得开;发链接,又需要自己找地方部署。

•

跨设备:手机上读了一半,回电脑接着看;电脑上生成了一份报告,推到手机上读,这都很自然。但一旦做同步,就会碰到账号、云端、隐私和复杂度。

即览现在还很小,小到我不太想把它包装成一个大产品。

但它正好卡在我自己每天都会遇到的缝里:

AI 把内容生成出来了,可我只是想在手机上好好看一眼。

你也经常被 Markdown、HTML、网页 PPT 这些文件硌到的话,可以试试。

TestFlight:https://testflight.apple.com/join/sv7KTqn9

也欢迎聊聊你们怎么看这件事:在 AI 参与之后,文档、展示和阅读到底会变成什么样。

✦
