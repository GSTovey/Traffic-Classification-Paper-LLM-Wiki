# MinerU 批量 PDF 解析脚本

## 1. 脚本用途

调用 MinerU 官方精准解析 API，将 PDF 批量转换为结构化 Markdown 文件。适用于 Obsidian 论文知识库的 PDF 入库流程。

## 2. 目录说明

| 目录 | 用途 |
|---|---|
| `00-inbox/PDFs/` | 放置待解析的 PDF 文件 |
| `01-mineru-output/` | MinerU API 返回的原始解压结果（含图片、表格等资源） |
| `02-parsed-markdown/` | 整理后的 Markdown 文件，一篇 PDF 对应一个 `.md` |
| `03-paper-notes/` | 由 Claudian 生成的结构化论文笔记 |
| `99-logs/` | 脚本运行日志 |
| `scripts/` | 脚本文件目录 |

## 3. 安装依赖

```bash
pip install -r scripts/requirements.txt
```

## 4. 配置 MINERU_API_TOKEN

**重要：Token 只能通过环境变量配置，不要写入任何文件。**

### macOS / Linux

```bash
export MINERU_API_TOKEN="你的MinerU新Token"
```

永久生效（写入 shell 配置文件）：

```bash
echo 'export MINERU_API_TOKEN="你的MinerU新Token"' >> ~/.zshrc
source ~/.zshrc
```

### Windows PowerShell

```powershell
setx MINERU_API_TOKEN "你的MinerU新Token"
```

配置后需**重启终端**生效。

## 5. 运行脚本

### 处理默认目录下的所有 PDF

```bash
python scripts/mineru_batch_parse.py
```

### 处理指定目录

```bash
python scripts/mineru_batch_parse.py --input "00-inbox/PDFs" --output "01-mineru-output" --parsed "02-parsed-markdown"
```

### 启用 OCR

```bash
python scripts/mineru_batch_parse.py --ocr
```

### 只解析指定页码范围

```bash
python scripts/mineru_batch_parse.py --page-ranges "1-8"
```

### 强制重新解析已处理的 PDF

```bash
python scripts/mineru_batch_parse.py --force
```

### 完整示例

```bash
python scripts/mineru_batch_parse.py \
  --input "00-inbox/PDFs" \
  --output "01-mineru-output" \
  --parsed "02-parsed-markdown" \
  --ocr \
  --page-ranges "1-10" \
  --batch-size 5
```

## 6. OCR 何时开启

默认情况下 OCR 是关闭的（`is_ocr = false`）。以下情况建议开启：

- PDF 是扫描件（图片格式，没有文字层）；
- PDF 中包含大量手写内容；
- 默认解析结果中文字缺失严重。

使用 `--ocr` 参数开启。

## 7. page-ranges 使用说明

`--page-ranges` 用于限制解析的页码范围，格式：

| 格式 | 含义 |
|---|---|
| `1-5` | 第 1 页到第 5 页 |
| `2,4-6` | 第 2 页和第 4 到 6 页 |
| `1-8` | 第 1 页到第 8 页 |

适用于：

- 论文太长，只需要解析正文部分（跳过参考文献和附录）；
- 每次只解析几页做快速预览；
- 控制 API 用量。

## 8. 安全注意事项

**绝对不要把 Token 写入以下位置：**

- Vault 中的任何 Markdown 文件
- 脚本源代码
- 聊天记录
- Git 仓库
- 配置文件（如 `.env`、`config.json`）

Token 只能通过操作系统环境变量 `MINERU_API_TOKEN` 配置。脚本运行时会从环境变量读取，不会打印完整 Token。

## 9. 常见问题

**Q: 脚本提示 "MINERU_API_TOKEN is not set"**
A: 请先配置环境变量，参考上方第 4 节。

**Q: PDF 上传失败**
A: 检查网络连接，确认 Token 有效，确认 PDF 文件未损坏。

**Q: 解析结果中找不到 full.md**
A: 可能是 PDF 内容过于特殊导致解析失败，查看 `01-mineru-output/` 中对应目录的原始内容，检查 `99-logs/` 中的日志。
