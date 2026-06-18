# 古诗生成模型原理可视化

项目来自于复旦大学《人工智能导论》PJ：手搓Transformer.

## 题目背景

古诗生成不仅需要保证语句通顺，还需要考虑换行、分句、声调、押韵和主题等形式约束。

## 文件说明

- `modified.py`：大视频，展示Transformer基础内容。
- `update.py`：三个短视频，展示对原始架构做的改进。

视频链接：[video_link](https://reurl.cc/YDgZ7O)

可渲染的场景如下：

| 文件 | 场景名称 | 内容 |
| --- | --- | --- |
| `modified.py` | `ChinesePoemEmbedding` | Transformer 注意力机制与残差连接 |
| `update.py` | `FormWeightedLoss` | 格式加权损失 |
| `update.py` | `ProsodyEmbeddingAndLoss` | 声调、押韵 embedding 与辅助任务 |
| `update.py` | `ThemeLoRA` | 主题 embedding 与 LoRA |

## 环境准备

首先需要有 Python 环境，随后可以按照 Manim Community官网的命令安装 Manim。

Manim 渲染还需要系统中安装 FFmpeg。代码使用了 LaTeX 公式，因此也需要安装 LaTeX 环境。

部分画面使用 `Source Han Serif SC`、`CMU Serif` 和 `Menlo` 字体。如果机器缺少相应字体，可以安装字体，或在代码中替换为已有字体。

## 使用方式

在项目根目录执行以下命令即可渲染对应场景：

```bash
# Transformer 注意力机制完整动画
manim -pqh modified.py ChinesePoemEmbedding

# 格式加权损失
manim -pqh update.py FormWeightedLoss

# 声调与押韵辅助任务
manim -pqh update.py ProsodyEmbeddingAndLoss

# 主题 LoRA
manim -pqh update.py ThemeLoRA
```

其中：

- `-p`：渲染完成后自动预览
- `-qh`：以高质量渲染 (quality high)；调试时可改为 `-ql` 以加快速度(quality low)

渲染结果默认保存在 `media/` 目录中。