<div id="readme-top" align="center">
  <h1 align="center">ComfyUI_JR_VoxCPM2</h1>

  <p align="center">
    <a href="../README.md">English</a> | <b>中文</b>
  </p>

  <p align="center">
    基于 <strong>VoxCPM2</strong> 的增强版 ComfyUI 自定义节点。
    <br>在保留原版 VoxCPM2 功能的基础上，新增 <strong>可复用声模预设库</strong> 与 <strong>全自动多人语音小说 / 多角色对话生成</strong> 工作流。
    <br /><br />
    <a href="https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/issues">提交 Bug</a>
    ·
    <a href="https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/issues">功能建议</a>
  </p>
</div>

<div align="center">

[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Forks][forks-shield]][forks-url]

</div>

<br>

## 项目简介

[VoxCPM2](https://github.com/OpenBMB/VoxCPM) 是一个 tokenizer-free 的文本转语音模型，基于超过 200 万小时多语言语音数据训练，构建于 MiniCPM-4 backbone 与 AudioVAE V2 之上，支持 **30 种语言**，无需语言标签，并可输出 **48kHz 录音室级音频**。

**ComfyUI_JR_VoxCPM2** 是在原始 ComfyUI VoxCPM2 实现基础上的增强分支，目标是在**保留原作者原有推理功能**的前提下，增加更适合生产化与长文本项目的工作流能力，包括：

- **可复用的声模预设 / 语音库管理**
- **全自动多人长篇语音小说生成**
- **多角色对白 / 小说旁白工作流**
- **更好的 AMD 与 Intel XPU 非 CUDA 启动兼容性**

也就是说，你依然可以使用原版核心能力，包括文本转语音、声音设计、可控克隆、Ultimate Cloning、ASR 辅助流程、降噪、LoRA 加载以及可选训练；同时又可以获得一层新的 JR 工作流增强，重点面向 **语音资产复用** 与 **基于角色标签的自动化多角色生成**。

---

## 本分支新增内容

### 1. 全自动多人语音小说 / 多角色对话生成
这个分支的核心定位，就是在 ComfyUI 内直接完成 **多角色有声小说、广播剧脚本、长篇旁白内容** 的自动生成。

目标工作流包括：

- 解析带角色标签的脚本，例如：
  - `[旁白]: 雨已经下了三天。`
  - `[Alice]: 你今晚真的要走吗？`
  - `[Bob]: 我没有别的选择。`
- 将每个角色映射到可复用的声模预设
- 每一句独立生成，提高长文本稳定性
- 按顺序自动合并全部音频
- 最终输出完整的长篇对白或旁白音频

这是 JR 分支与原版最重要的差异点。

### 2. 可复用声模预设库
相比每次都重复输入参考音频和参考文本，这个分支增加了 **Voice Preset / 声模预设系统**：

- 一个角色声音只需保存一次
- 参考音频与元数据可落盘保存
- 后续流程中可直接加载
- 适合固定旁白、主角、配角长期复用
- 可逐步建立自己的本地语音角色库

### 3. 更好的 AMD / Intel XPU 兼容性
原始训练路径本质上是偏 CUDA 的。这个分支将 **LoRA Training 设计为可选路径**。

- 当后端为 **CUDA** 时，可以使用完整训练能力
- 当后端为 **AMD**、**Intel XPU** 或其他非 CUDA 后端时，会跳过训练相关路径
- 其余推理相关功能仍然可以正常加载并使用

这意味着在异构 GPU 环境下，非 CUDA 用户仍然可以使用主要功能，例如 TTS、声音克隆、预设声模、多人小说生成等，而不是像严格 CUDA 初始化路径那样，因训练模块不兼容导致整个插件无法启动。

---

## 主要特性

### 保留原版 VoxCPM2 功能
- **30 语言多语种 TTS** — 输入支持语言即可生成，无需手动指定语言标签
- **声音设计** — 仅通过自然语言描述生成新声音
- **可控语音克隆** — 用短参考音频克隆说话人声音，并可附加风格控制
- **Ultimate Cloning** — 提供参考音频与逐字稿，获得更高保真度
- **48kHz 高质量输出** — 输入 16kHz 参考音频，也可输出 48kHz 音频
- **LoRA 推理加载** — 支持加载微调 LoRA 模型做推理
- **ASR 自动转写** — 使用 SenseVoiceSmall 自动识别参考音频文本
- **参考音频降噪** — 可选 ZipEnhancer 对参考音频降噪
- **响度归一化** — 降噪开启时自动做响度标准化
- **Torch Compile** — 可选 `torch.compile` 优化
- **自动模型管理** — 由 ComfyUI 自动下载和管理模型
- **参考音频时长校验** — 避免过长参考音频影响生成质量

### JR 分支增强功能
- **声模预设保存 / 读取工作流**
- **持久化本地语音库**
- **多角色脚本解析**
- **角色到预设的映射机制**
- **逐句生成以提升稳定性**
- **长篇音频自动合并输出**
- **缺失角色时可回退到旁白**
- **面向小说 / 对话的长文本工作流**
- **非 CUDA 环境更平滑的兼容路径**

---

## 安装方式

### 通过 ComfyUI Manager
搜索 `ComfyUI_JR_VoxCPM2`，点击 **Install**。

### 手动安装

1. 克隆到 `ComfyUI/custom_nodes/` 目录：
   ```sh
   git clone https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2.git
   ```

2. 安装依赖：
   ```sh
   cd ComfyUI_JR_VoxCPM2
   pip install -r requirements.txt
   ```

> **Windows + Python 3.13+：** 如果 `pip install` 在 `editdistance` 处报 `pdm.backend` 或 C4819 编码错误，可执行：
> ```sh
> pip install pdm-backend
> set CL=/utf-8
> # 或 PowerShell：
> $env:CL="/utf-8"
> pip install -r requirements.txt
> ```

3. 重启 ComfyUI。

节点会出现在对应的 audio / JR 分类下，具体以分支版本为准。

---

## CUDA / AMD / Intel XPU 说明

### CUDA
CUDA 是 **全功能路径**，可使用：
- 推理
- 声音克隆
- 声音设计
- JR 多角色生成
- LoRA 加载
- LoRA 训练

### AMD / Intel XPU / 其他非 CUDA 后端
在非 CUDA 环境下，这个分支的目标是：即使训练栈不可用，也要保证**推理路径可用**。

非 CUDA 后端可用目标包括：
- TTS
- 声音设计
- 声音克隆
- Ultimate Cloning
- ASR 辅助流程
- 降噪辅助克隆（取决于依赖与后端支持情况）
- JR 声模预设工作流
- JR 多人语音小说 / 对话生成

当前限制：
- **LoRA Training 仍是 CUDA-only / 偏 CUDA 的能力**
- 若当前设备不是 CUDA，插件应跳过或禁用训练相关路径，而不是导致整体启动失败

实际意义上，这个分支改善了非 CUDA 用户体验：即便不能训练 LoRA，依然可以正常使用插件的主要生成功能。

---

## 模型

模型首次使用时会自动下载到：

```text
ComfyUI/models/tts/VoxCPM/
```

| 模型 | 参数量 | 采样率 | 说明 | Hugging Face |
|:---|:---:|:---:|:---|:---|
| **VoxCPM2** | 2B | 48kHz | 30 语言 TTS、声音设计、可控克隆、Ultimate Cloning | [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) |

---

## 节点说明

## 原版 / 核心节点

### VoxCPM2 TTS
标准文本转语音，可选声音设计，不需要参考音频。

### VoxCPM2 Voice Clone
语音克隆节点，支持可控克隆与 Ultimate Cloning。

### VoxCPM2 Training Nodes
训练相关节点仍然保留，属于原始项目能力的一部分，但主要面向 **CUDA 环境**。

---

## JR 节点

### JR VoxCPM2 Loader
创建可复用 session / 模型句柄，供下游 JR 工作流复用。

### JR VoxCPM2 Voice Preset
用于创建、更新、读取、查看、删除持久化声模预设。

典型用途：
- 把旁白声音保存一次
- 把每个角色声音保存一次
- 后续多个章节 / 多个流程反复复用

### JR VoxCPM2 Generate
支持以下模式的单角色生成：
- 基于 preset 的生成
- 基于参考音频克隆的生成
- 基于 voice design 的生成
- 原始文本 TTS 生成

### JR VoxCPM2 Script Parse
将多人脚本解析成标准化 speaker/text 结构。

支持格式示例：
```text
[旁白]: 夜色安静得可怕。
[Alice]: 你听到了吗？
[Bob]: 站在我后面。
```

```text
【旁白】夜色安静得可怕。
【Alice】你听到了吗？
【Bob】站在我后面。
```

```text
旁白: 夜色安静得可怕。
Alice: 你听到了吗？
Bob: 站在我后面。
```

### JR VoxCPM2 Multi-Talk Generate
这是 JR 分支面向长文本的核心节点。

它可以：
- 解析脚本
- 匹配角色映射
- 按句逐条生成
- 缺失角色时回退到旁白
- 最终自动合并成长篇音频结果

适用场景：
- 多角色有声小说
- 视觉小说配音
- 角色扮演对话生成
- 旁白式故事内容
- 分章节有声书制作

### JR VoxCPM2 Preset List
列出磁盘上已保存的所有声模预设。

### JR VoxCPM2 Audio Merge
将多个音频片段按设定静音间隔合并。

---

## 使用方式

## A. 标准 TTS / 声音设计
1. 添加 **VoxCPM2 TTS** 节点
2. 输入 `text`
3. 可选填写 `voice_description`
4. 运行工作流

示例描述：
- `A young woman, gentle and sweet voice`
- `An old man with a gravelly, slow voice`
- `A calm female narrator for long-form storytelling`

---

## B. 语音克隆
1. 添加 **VoxCPM2 Voice Clone** 节点
2. 接入 `reference_audio`
3. 输入目标 `text`
4. 如需最高保真，可填写 `prompt_text`
5. 若没有逐字稿，也可以启用 `enable_asr`

建议：
- 使用干净高质量参考音频
- 长度尽量控制在 5–15 秒
- 提供准确 transcript 可提升保真度

---

## C. 声模预设工作流
1. 用参考音频创建 preset
2. 给 preset 起一个角色名或旁白名
3. 在后续流程中重复使用
4. 逐步构建自己的角色语音库

推荐命名示例：
- `Narrator_Female_01`
- `Hero_Male_01`
- `Villain_Female_01`
- `Old_Master_01`

---

## D. 多人语音小说 / 对话工作流
1. 先为旁白和角色分别建立 preset
2. 准备带角色标签的脚本
3. 将 speaker 名称映射到对应 preset
4. 运行 **JR VoxCPM2 Multi-Talk Generate**
5. 获得自动合并后的长篇音频结果

示例：
```text
[旁白]: 雨已经连续下了三天。
[Alice]: 我不喜欢这里。
[Bob]: 我们天亮就走。
[旁白]: 那一夜，他们谁都没有睡着。
```

推荐用途：
- 章节旁白
- 多角色小说
- 广播剧原型
- 游戏对白语音生成

---

## LoRA 支持

### 推理
1. 将 `.safetensors` LoRA 文件放入：
   ```text
   ComfyUI/models/loras/
   ```
2. 在支持的节点里从 `lora_name` 下拉菜单中选择

### 训练
训练相关能力 **保留自原始项目**，但在本分支中被处理为 **可选的 CUDA-only 路径**。

这意味着：
- **CUDA 用户** 可以继续使用训练管线
- **AMD / Intel XPU / 非 CUDA 用户** 即便不能训练，也不会因为训练路径而导致整个插件无法使用

这种设计更适合混合硬件环境，同时也保留了原始项目在兼容 CUDA 环境下的训练能力。

**[点击查看 LoRA Training Guide](readme-lora-training.md)**

---

## 最佳实践建议

### 语音克隆
- 尽量使用 **干净、高质量参考音频**
- 5–15 秒通常比较理想
- 若追求最高保真，尽量提供准确逐字稿
- 合理标点有助于模型还原语气语调

### 声模预设
- 把稳定旁白角色保存成 preset
- 固定角色只建一次，后续反复复用
- 章节之间保持统一命名

### 多角色长文本生成
- 尽量一行一个角色、一句一句生成，稳定性更高
- 对未知角色可设置 narrator fallback
- 不建议把整章超长段落一次性塞进单条生成
- 对长章节建议拆段，方便重试和恢复

### 生成质量
- **`cfg_value`**：更高更贴近提示，更低更自然
- **`inference_timesteps`**：5–10 偏快，15–25 偏高质量
- **`normalize_text`**：普通文本通常保持开启即可

---

## 支持语言（30 种）

Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Lao, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese

中文方言覆盖包括：
四川话、粤语、吴语、东北话、河南话、陕西话、山东话、天津话、闽南语

---

## 已知限制

- 声音设计与风格控制结果在不同生成之间可能存在波动
- 不同语言、不同参考音频质量下，效果会有所差异
- 超长文本或情绪特别强烈的内容仍可能不如短句稳定
- 多角色长文本更适合按句或按段处理
- LoRA 训练仍主要面向 CUDA 兼容环境
- 非 CUDA 环境当前优先目标是 **保证推理兼容性**
- 严禁将本项目用于冒充、欺诈、误导或虚假信息传播，AI 生成内容应明确标注

---

## 许可说明

VoxCPM 模型及其组成部分遵循 OpenBMB 提供的 [Apache-2.0 License](https://github.com/OpenBMB/VoxCPM/blob/main/LICENSE)。

同时请遵守以下部分各自的许可协议：
- 原始上游 ComfyUI VoxCPM2 项目
- 本项目引入的依赖项
- 你使用的模型权重与 LoRA 资产

---

## 致谢

- 原始上游 **ComfyUI VoxCPM2** 项目的作者与贡献者
- **[@wildminder](https://github.com/wildminder)** 提供了 [ComfyUI-VoxCPM](https://github.com/wildminder/ComfyUI-VoxCPM) 这一基础实现
- **OpenBMB & ModelBest** 开源了 [VoxCPM](https://github.com/OpenBMB/VoxCPM)
- **ComfyUI 团队** 提供了强大而可扩展的平台

---

## 项目定位

**ComfyUI_JR_VoxCPM2** 并不是为了否定或替代原始项目方向。  
它的目标是在**保留原始 VoxCPM2 功能**的前提下，增加更强的工作流能力，尤其面向：

- 可复用语音库
- 自动化多角色生成
- 有声小说 / 对话流水线
- 更实用的非 CUDA 推理兼容性

如果你只需要原版单角色 TTS 与克隆能力，这里依然保留。  
如果你需要自动化多角色有声小说生成，这个分支就是专门为此而做的。

<!-- MARKDOWN LINKS & IMAGES -->
[stars-shield]: https://img.shields.io/github/stars/Goldlionren/ComfyUI_JR_VoxCPM2.svg?style=for-the-badge
[stars-url]: https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/stargazers
[issues-shield]: https://img.shields.io/github/issues/Goldlionren/ComfyUI_JR_VoxCPM2.svg?style=for-the-badge
[issues-url]: https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/issues
[forks-shield]: https://img.shields.io/github/forks/Goldlionren/ComfyUI_JR_VoxCPM2.svg?style=for-the-badge
[forks-url]: https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/network/members
