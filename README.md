<div id="readme-top" align="center">
  <h1 align="center">ComfyUI_JR_VoxCPM2</h1>

  <p align="center">
    <b>English</b> | <a href="./docs/README_zh.md">中文</a>
  </p>

  <p align="center">
    Enhanced ComfyUI nodes for <strong>VoxCPM2</strong> — tokenizer-free, diffusion autoregressive Text-to-Speech.
    <br>Preserves the original VoxCPM2 feature set while adding <strong>reusable voice preset libraries</strong> and <strong>fully automated multi-speaker audiobook / dialogue generation</strong>.
    <br /><br />
    <a href="https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/issues">Report Bug</a>
    ·
    <a href="https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/issues">Request Feature</a>
  </p>
</div>

<div align="center">

[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Forks][forks-shield]][forks-url]

</div>

<br>

## About

[VoxCPM2](https://github.com/OpenBMB/VoxCPM) is a tokenizer-free Text-to-Speech model trained on over 2 million hours of multilingual speech data. Built on a MiniCPM-4 backbone with AudioVAE V2, it outputs **48kHz studio-quality audio** and supports **30 languages** with no language tag needed.

**ComfyUI_JR_VoxCPM2** is an enhanced fork built on top of the original ComfyUI VoxCPM2 implementation. It is designed to **preserve the original upstream inference capabilities** while extending the project with a more production-friendly workflow for:

- **Reusable voice preset / voice library management**
- **Fully automated multi-speaker long-form audiobook generation**
- **Multi-character dialogue / novel narration workflows**
- **Better non-CUDA startup compatibility for AMD and Intel XPU users**

This means you still keep the original core VoxCPM2 experience — including text-to-speech, voice design, controllable cloning, ultimate cloning, ASR-assisted workflows, denoising, LoRA loading, and optional training — while gaining a new JR workflow layer focused on **voice asset reuse** and **automatic speaker-tag-based generation**.

---

## What This Fork Adds

### 1. Fully Automated Multi-Speaker Audiobook / Dialogue Generation
This fork is built to generate **multi-character voice novels, drama scripts, and audiobook narration** directly inside ComfyUI.

Key workflow goals:

- Parse speaker-tagged scripts such as:
  - `[Narrator]: The rain fell softly over the old town.`
  - `[Alice]: Are you really leaving tonight?`
  - `[Bob]: I have no choice.`
- Map each speaker to a reusable preset
- Generate each line independently for better stability
- Merge all generated lines in order
- Produce final long-form dialogue or narration audio automatically

This is the primary differentiator of the JR fork.

### 2. Reusable Voice Preset Library
Instead of repeatedly reloading and re-entering the same reference audio and transcript, this fork adds a reusable **voice preset system**:

- Save a speaker preset once
- Store reference audio and metadata on disk
- Reload presets across workflows
- Reuse narrator / character voices consistently
- Build your own structured local voice library for long-form projects

### 3. Better AMD / Intel XPU Compatibility
The original training path is CUDA-oriented. In this fork, the **LoRA training pipeline is treated as an optional path**.

- If your backend is **CUDA**, you can use the full training-related functionality
- If your backend is **AMD** or **Intel XPU / other non-CUDA backends**, the training-specific path is bypassed
- The rest of the plugin can still load and remain usable for inference-related features

This is an important improvement for heterogeneous GPU environments, because non-CUDA users can still use the main TTS, cloning, and JR long-form generation features instead of having the whole plugin fail during startup.

---

## Key Features

### Original VoxCPM2 Features Preserved
- **30-Language Multilingual TTS** — Input text in any supported language, no language tag needed
- **Voice Design** — Generate a novel voice from a natural-language description alone
- **Controllable Voice Cloning** — Clone a voice from a short reference clip, with optional style guidance
- **Ultimate Cloning** — Provide reference audio + transcript for maximum fidelity
- **48kHz Studio-Quality Output** — Accepts 16kHz reference audio and outputs 48kHz audio
- **LoRA Loading for Inference** — Load fine-tuned LoRA checkpoints for voice styles
- **ASR Auto-Transcription** — Auto-transcribe reference audio using SenseVoiceSmall
- **Reference Audio Denoiser** — Optional ZipEnhancer denoising for cleaner cloning
- **Loudness Normalization** — Auto-normalize loudness when denoiser is active
- **Torch Compile** — Optional `torch.compile` optimization
- **Automatic Model Management** — Models are downloaded and managed by ComfyUI
- **Audio Duration Validation** — Rejects overly long reference audio to protect generation quality

### JR Fork Enhancements
- **Voice Preset Save / Load Workflow**
- **Persistent On-Disk Voice Library**
- **Multi-Speaker Script Parsing**
- **Speaker-to-Preset Mapping**
- **Per-Line Generation for Stability**
- **Automatic Audio Merge for Long-Form Output**
- **Narrator Fallback for Missing Speakers**
- **Long-Form Audiobook / Dialogue Workflow Design**
- **Graceful Non-CUDA Compatibility Path**

---

## Installation

### Via ComfyUI Manager
Search for `ComfyUI_JR_VoxCPM2` and click **Install**.

### Manual

1. Clone into your `ComfyUI/custom_nodes/` directory:
   ```sh
   git clone https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2.git
   ```

2. Install dependencies:
   ```sh
   cd ComfyUI_JR_VoxCPM2
   pip install -r requirements.txt
   ```

> **Python 3.13+ on Windows:** If `pip install` fails on `editdistance` with a `pdm.backend` import error or C4819 encoding warning, run:
> ```sh
> pip install pdm-backend
> set CL=/utf-8
> # or in PowerShell:
> $env:CL="/utf-8"
> pip install -r requirements.txt
> ```

3. Restart ComfyUI.

Nodes will appear under the relevant audio / JR categories depending on the branch version.

---

## CUDA / AMD / Intel XPU Notes

### CUDA
CUDA is the **full-featured path**:
- Inference
- Voice cloning
- Voice design
- JR multi-speaker generation
- LoRA loading
- LoRA training

### AMD / Intel XPU / Other Non-CUDA Backends
On non-CUDA devices, this fork is designed to keep the **inference path usable** even when the training stack is not available.

Supported goal on non-CUDA backends:
- TTS
- Voice design
- Voice cloning
- Ultimate cloning
- ASR-assisted workflows
- Denoiser-assisted cloning (if dependency/backend path is available)
- JR voice preset workflows
- JR multi-speaker audiobook / dialogue generation

Current limitation:
- **Training LoRA is CUDA-only / CUDA-oriented**
- If the current backend is not CUDA, the plugin should bypass or disable the training-related path instead of breaking startup

In practical terms, this fork improves the non-CUDA experience by allowing the plugin to remain usable for its main generation workflows, whereas a strict CUDA-only initialization path can otherwise prevent the whole plugin from loading.

---

## Models

The model is downloaded automatically on first use to:

```text
ComfyUI/models/tts/VoxCPM/
```

| Model | Parameters | Sample Rate | Description | Hugging Face |
|:---|:---:|:---:|:---|:---|
| **VoxCPM2** | 2B | 48kHz | 30-language TTS, voice design, controllable cloning, ultimate cloning | [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) |

---

## Nodes

## Original / Core Nodes

### VoxCPM2 TTS
Text-to-speech with optional voice design. No reference audio needed.

### VoxCPM2 Voice Clone
Voice cloning with controllable and ultimate modes.

### VoxCPM2 Training Nodes
Training-related nodes remain available as part of the preserved upstream capability, but are intended for **CUDA environments**.

---

## JR Nodes

### JR VoxCPM2 Loader
Creates a reusable session / model handle for downstream JR workflows.

### JR VoxCPM2 Voice Preset
Create, update, load, inspect, and delete persistent voice presets.

Typical use cases:
- Save narrator voice once
- Save each character voice once
- Reuse them across many chapters / episodes / workflows

### JR VoxCPM2 Generate
Single-speaker generation using:
- preset-based workflow
- reference-audio clone workflow
- voice-design workflow
- raw text TTS workflow

### JR VoxCPM2 Script Parse
Parses multi-speaker scripts into normalized speaker/text segments.

Supported examples:
```text
[Narrator]: The night was silent.
[Alice]: Did you hear that?
[Bob]: Stay behind me.
```

```text
【Narrator】The night was silent.
【Alice】Did you hear that?
【Bob】Stay behind me.
```

```text
Narrator: The night was silent.
Alice: Did you hear that?
Bob: Stay behind me.
```

### JR VoxCPM2 Multi-Talk Generate
The main JR node for long-form content.

It can:
- parse a script
- resolve speaker mappings
- generate each line independently
- apply narrator fallback when needed
- merge outputs into a final long-form audio result

This node is intended for:
- multi-character audio novels
- visual novel dubbing
- roleplay dialogue generation
- narrated story content
- chapter-based audiobook production

### JR VoxCPM2 Preset List
Lists available presets stored on disk.

### JR VoxCPM2 Audio Merge
Merges multiple generated audio segments with configurable silence gaps.

---

## Usage

## A. Standard TTS / Voice Design
1. Add the **VoxCPM2 TTS** node
2. Enter your `text`
3. Optionally enter `voice_description`
4. Run the workflow

Example descriptions:
- `A young woman, gentle and sweet voice`
- `An old man with a gravelly, slow voice`
- `A calm female narrator for long-form storytelling`

---

## B. Voice Cloning
1. Add the **VoxCPM2 Voice Clone** node
2. Connect `reference_audio`
3. Enter target `text`
4. Optionally provide `prompt_text` for ultimate cloning
5. Optionally enable `enable_asr` if transcript is not available

For best results:
- use clean reference audio
- keep it around 5–15 seconds
- provide accurate transcript for highest fidelity

---

## C. Voice Preset Workflow
1. Create a preset from reference audio
2. Save the preset with a character / narrator name
3. Reuse that preset in later workflows
4. Build a voice library for recurring characters

Suggested preset examples:
- `Narrator_Female_01`
- `Hero_Male_01`
- `Villain_Female_01`
- `Old_Master_01`

---

## D. Multi-Speaker Audiobook / Dialogue Workflow
1. Create presets for narrator and characters
2. Prepare a speaker-tagged script
3. Map each speaker name to a preset
4. Run **JR VoxCPM2 Multi-Talk Generate**
5. Get merged long-form output audio

Example:
```text
[Narrator]: The rain had not stopped for three days.
[Alice]: I don't like this place.
[Bob]: We leave at dawn.
[Narrator]: Neither of them slept that night.
```

Recommended use cases:
- chapter narration
- multi-role fiction
- audio drama prototyping
- game dialogue voice generation

---

## LoRA Support

### Inference
1. Place `.safetensors` LoRA files in:
   ```text
   ComfyUI/models/loras/
   ```
2. Select your LoRA from the `lora_name` dropdown where supported

### Training
Training-related functionality is **preserved from the original project**, but in this fork it is handled as an **optional CUDA-only path**.

That means:
- **CUDA users** can use the training pipeline
- **AMD / Intel XPU / non-CUDA users** can still use the rest of the plugin without training support blocking startup

This design keeps the project practical on mixed hardware environments while still preserving the upstream training capability for compatible CUDA setups.

**[Click here for the LoRA Training Guide](docs/readme-lora-training.md)**

---

## Tips for Best Results

### Voice Cloning
- Use **clean, high-quality reference audio**
- 5–15 seconds is usually ideal
- For highest fidelity, provide an accurate transcript
- Good punctuation helps preserve intonation

### Voice Presets
- Save stable narrator voices as presets
- Save recurring character voices once and reuse them
- Keep preset names consistent across chapters

### Multi-Speaker Long-Form Generation
- Keep one line or one sentence per speaker entry for better stability
- Use a narrator preset as fallback for unknown speakers
- Generate line-by-line rather than passing huge monolithic paragraphs when possible
- For long chapters, split content into sections for easier reruns and recovery

### Generation Quality
- **`cfg_value`**: Higher = more prompt adherence, lower = more natural variation
- **`inference_timesteps`**: 5–10 for speed, 15–25 for quality
- **`normalize_text`**: Leave ON for most normal text input

---

## Supported Languages (30)

Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Lao, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese

Chinese dialect coverage includes:
Sichuan, Cantonese, Wu, Northeastern, Henan, Shaanxi, Shandong, Tianjin, Southern Min

---

## Limitations

- Voice design and style control may vary between runs
- Quality may vary by language and reference quality
- Very long or highly expressive passages can still be less stable than short controlled segments
- Multi-speaker long-form generation is best handled line-by-line or section-by-section
- LoRA training remains intended for CUDA-compatible environments
- Non-CUDA environments target **inference compatibility first**
- Do not use this project for impersonation, fraud, deception, or disinformation; AI-generated content should be clearly labeled

---

## License

The VoxCPM model and its components are subject to the [Apache-2.0 License](https://github.com/OpenBMB/VoxCPM/blob/main/LICENSE) provided by OpenBMB.

Please also respect the license terms of:
- the original upstream ComfyUI VoxCPM2 implementation
- any added dependencies
- any model weights or LoRA assets you use with this workflow

---

## Acknowledgments

- The original upstream **ComfyUI VoxCPM2** authors and contributors
- **[@wildminder](https://github.com/wildminder)** for the original [ComfyUI-VoxCPM](https://github.com/wildminder/ComfyUI-VoxCPM) foundation
- **OpenBMB & ModelBest** for creating and open-sourcing [VoxCPM](https://github.com/OpenBMB/VoxCPM)
- **The ComfyUI team** for their extensible platform

---

## Project Positioning

**ComfyUI_JR_VoxCPM2** is not intended to replace the original project direction.  
Its purpose is to **preserve the original VoxCPM2 features** while adding a stronger workflow layer for:

- reusable voice libraries
- automated multi-character generation
- audiobook / dialogue pipelines
- better practical support for non-CUDA inference environments

If you want the original single-speaker and cloning features, they remain here.  
If you want automated multi-speaker voice novel generation, this fork is built specifically for that.

<!-- MARKDOWN LINKS & IMAGES -->
[stars-shield]: https://img.shields.io/github/stars/Goldlionren/ComfyUI_JR_VoxCPM2.svg?style=for-the-badge
[stars-url]: https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/stargazers
[issues-shield]: https://img.shields.io/github/issues/Goldlionren/ComfyUI_JR_VoxCPM2.svg?style=for-the-badge
[issues-url]: https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/issues
[forks-shield]: https://img.shields.io/github/forks/Goldlionren/ComfyUI_JR_VoxCPM2.svg?style=for-the-badge
[forks-url]: https://github.com/Goldlionren/ComfyUI_JR_VoxCPM2/network/members
