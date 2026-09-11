# 具身智能模型技术进展与关系综述

[English](README.en.md) · 证据核验截至 **2026-09-11**

系统梳理机器人操作、VLA、世界模型、语义规划、导航与全身控制，拆解典型模型的输入、架构、动作表示、训练、数据、推理闭环、贡献与局限。收录 **77 张模型/版本/方法卡、80 条模型关系、155 条去重来源、11 家机构的产品进展**。卡片数包含版本、方法和组件，不等于独立基础模型数量。

- **[中文完整报告](records/artifacts/survey-report.md)** · [中文 PDF](reports/embodied-intelligence-model-survey.pdf)
- **[English full report](records/artifacts/survey-report-en.md)** · [English PDF](reports/embodied-intelligence-model-survey-en.pdf)
- [逐模型拆解 Atlas](records/artifacts/model-atlas.md) · [模型对比 CSV](records/artifacts/model-matrix.csv)
- [模型关系详解](records/artifacts/model-relations.md) · [关系数据 JSON](records/artifacts/relationship-graph.json)
- [数据与采集接口](records/artifacts/data-matrix.csv) · [基准比较](records/artifacts/benchmark-matrix.csv) · [产品矩阵](records/artifacts/product-matrix.csv)
- [评测设计](records/artifacts/evaluation-plan.md) · [来源台账](records/artifacts/sources.json) · [BibTeX](records/artifacts/references.bib)
- [范围与覆盖](records/views/coverage-map.md) · [证据审计](records/views/evidence-audit.md) · [全部文件](CONTENTS.md)

![具身智能闭环中的模型角色](figures/architecture.svg)

## 如何理解模型之间的关系

具身智能是感知、任务推理、动作生成、环境预测和稳定控制的协同。报告区分明确复用、版本演进、方法组合和分析性互补；**箭头不默认表示权重继承，最新版本也不默认优于所有任务中的旧方法**。

代表线索包括 ACT/DP、RT/RT-X、Octo、OpenVLA/OFT、π0至π0.7、GR00T N1至N1.7、Gemini Robotics 2系列、SmolVLA、RDT、两篇不同的UniVLA、X-VLA、LingBot-VLA 2.0、GO-1、MolmoAct2、小米Robotics-0、SayCan/PaLM-E/VoxPoser、R3M/VC-1、PerAct/RVT、Dreamer、Genie、V-JEPA、Cosmos、GAIA、HumanPlus、SONIC、ViNT/NoMaD、GOAT与Helix等。

五个未来挑战：跨本体动作与接触表示；长期记忆与失败恢复；可用于行动决策的世界模型；实时性、能耗与控制可靠性；可审计的持续学习。每项给出缺口、研究方向和验收指标。

## 仓库结构

```text
intent/                 范围、研究协议、更新工作流
records/research/       四组专题源稿、来源、模型与关系
records/artifacts/      规范中英报告、Atlas、结构化比较数据
records/views/          覆盖、证据、不确定性与审阅结论
records/runs/           检索记录、校验记录和文件清单
figures/                可编辑SVG模型角色图与关系图
reports/                中英文PDF
scripts/                整编、PDF构建、内容验证和清单核对
```

## 本地重建

Python 3.10+，安装 `requirements.txt` 后，在仓库根目录执行：

```bash
python scripts/assemble.py
python scripts/build_reports.py
python scripts/validate.py
python scripts/build_manifest.py
python scripts/check_manifest.py
```

PDF中文字体默认检测macOS Arial Unicode，其他系统通过构建脚本指定支持中文的TrueType字体。修改后需重新检查PDF分页、图表和中文显示；清单仅在完成校验后更新。`assemble.py`会从专题源稿生成规范报告，直接改生成文件会在下次整编时被覆盖。

## 证据与复用边界

这是技术范围综述和工程分析，未复现机器人训练、实测硬件或核验所有厂商现场运行。评测协议不同的分数不统一排名；官方演示、客户试点、交付计划与持续运营分别处理。完整性指研究范围内的层次覆盖，不声称穷尽全部论文。代码、模型卡、权重、训练数据和许可证是不同的开放维度。

组织方式延续 [agent-memory-survey](https://github.com/xiaotianyu-ac/agent-memory-survey)，来源框架说明见 [ATTRIBUTION](ATTRIBUTION.md)。第三方论文、代码、权重与数据仍归各自权利人；本仓库提供原始链接与分析，不分发这些原始资产。
