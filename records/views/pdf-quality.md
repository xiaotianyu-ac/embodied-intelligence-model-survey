# PDF 质量检查 / PDF quality review

检查日期：2026-09-11。两份 PDF 均由本仓库规范 Markdown 与三个 SVG 图直接构建。下面的摘要仅涉及文档完整性和版面检查，不代表复现了所引用论文的机器人实验。
Reviewed on 2026-09-11. Both PDFs were built from the canonical Markdown and the three SVG figures in this repository. This record covers document integrity and layout, not experimental reproduction of cited robotics results.

| 检查项 / Check | 中文 / Chinese | English |
|---|---:|---:|
| 页数 / Pages | 27 | 31 |
| 来源定义完整保留 / Source definitions retained | 155 / 155 | 155 / 155 |
| 内部引用链接 / Internal citation links | 382 | 382 |
| 外部链接注释 / External link annotations | 178 | 176 |
| PDF 章节书签 / PDF outline entries | 59 | 59 |
| 空白页 / Blank pages | 0 | 0 |
| 缺失来源编号 / Missing source numbers | 0 | 0 |
| 越界字符 / Out-of-bounds characters | 0 | 0 |
| 文本替换字符 / Unicode replacement characters | 0 | 0 |

## 可视检查 / Visual inspection

全部 58 页均以 60 dpi 渲染后逐页查看缩略图。另以 125 dpi 查看中文第 1、2、13、17、18、21、27 页，英文第 1、2、5、16、21、22、31 页，覆盖标题、正文、产品对照表、模型索引、全部三张图及参考来源。未发现文字裁切、重叠、缺字方框或表格标题失踪。英文首列表头和普通长词的末字母孤行已通过调整通用列宽修复。
Every page was rendered at 60 dpi and reviewed in contact sheets. The Chinese pages 1, 2, 13, 17, 18, 21 and 27, and English pages 1, 2, 5, 16, 21, 22 and 31 were also inspected at 125 dpi. No clipping, overlapping text, missing-glyph boxes or missing table headers were observed. Column allocation was adjusted to prevent isolated final letters in ordinary English table labels.

| 图 / Figure | Chinese PDF page | English PDF page |
|---|---:|---:|
| Closed-loop model roles — architecture.svg | 2 | 2 |
| Training paths and framework reuse — learning-paths.svg | 17 | 21 |
| Model relationships — model-relations.svg | 18 | 22 |

PDF 保留可点击引用和章节书签；Markdown 相对文件链接映射到本仓库的 GitHub 文件页。图示是矢量图，代码块保留其原有内容。长表可跨页并重复表头。临时逐页 PNG 和缩略图不纳入仓库。
The PDFs preserve clickable references and section bookmarks. Relative Markdown file links resolve to the corresponding GitHub files. Diagrams remain vectors; code blocks retain their own content. Long tables repeat their headers across pages. Temporary page renders and contact sheets are excluded from the repository.

## 源稿与成品绑定 / Source and artifact binding

### 中文 / Chinese

- Markdown: [survey-report.md](../artifacts/survey-report.md)
- Markdown SHA256: `6ae814379dcf65a493d38559120d6acde4a305537e5420a194a2308469316a0c`
- PDF: [embodied-intelligence-model-survey.pdf](../../reports/embodied-intelligence-model-survey.pdf)
- PDF SHA256: `c22b3dd4fb7cbae31a90ca6dc2d7c8fca7f60fadf2481ca3bd45b8624663b780`

### English

- Markdown: [survey-report-en.md](../artifacts/survey-report-en.md)
- Markdown SHA256: `40eea57d8f4b8d4a12983918272058fb86f6d8f10196e3d1f529158e3289b7a1`
- PDF: [embodied-intelligence-model-survey-en.pdf](../../reports/embodied-intelligence-model-survey-en.pdf)
- PDF SHA256: `cf8a4310eedeb84c0ca41fb7cc44e7910f0a12349520d4402d7ac825efe46408`

## 复现文档构建 / Reproduce the document build

在仓库根目录运行，Python 环境需安装 ReportLab；可选 svglib，用于扩展 SVG 元素支持。默认会检测 macOS Arial Unicode 字体；其他系统需用 `--font` 提供可嵌入的中文 TrueType 字体。字体不同可能导致分页不同。
Run from the repository root with ReportLab installed. svglib is optional and extends SVG support. The builder detects Arial Unicode on macOS; on other systems, supply an embeddable CJK TrueType font with `--font`. Different fonts may change pagination.

```sh
python3 scripts/assemble.py
python3 scripts/build_reports.py --font /path/to/cjk-font.ttf
```

可用 Poppler 重新渲染，输出到仓库以外的临时目录。检查链接与引用应结合 PDF 解析和人工阅读；“零越界”检测不能替代可视检查。
Poppler can render the files again into a temporary directory outside the repository. Link/reference inspection should combine PDF parsing with visual review; a zero-overflow check is not a substitute for viewing the pages.

```sh
mkdir -p /tmp/embodied-survey-pdf-qa
pdftoppm -png -r 60 reports/embodied-intelligence-model-survey.pdf /tmp/embodied-survey-pdf-qa/zh
pdftoppm -png -r 60 reports/embodied-intelligence-model-survey-en.pdf /tmp/embodied-survey-pdf-qa/en
```

重新构建 PDF 可能改变创建时间与文件摘要；本记录绑定的是上述 SHA256 对应的交付成品。
A rebuild can change PDF metadata and file hashes. This record is bound to the release artifacts identified by the SHA256 values above.
