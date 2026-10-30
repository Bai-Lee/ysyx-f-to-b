# 第三方内容、任务原文与许可范围

本仓库保留 F～B 研究成果，并明确区分独立实现、课程任务原文与外部依赖。根目录 MIT 授权只覆盖原创贡献，不重新授权第三方内容。上游作者、版权和许可声明应一并保留。

| 内容 | 来源及处理 |
|---|---|
| `requirements/original/`、各阶段 `sources/`、任务索引中的原文及所引用的 `assets/` 插图/公式 | 来自一生一芯官方文档及原文所引用课程；页面 URL、版本、采集时间和原始 HTML SHA-256 保留。权利归原作者；未识别到统一的再发布许可证，不能把公开可访问解释为 MIT 授权。需要其他用途时请向原权利人确认。 |
| `D/nemu_overlay/`、NEMU 安装/修改副本、`C/C5/ref/` 等框架派生部分 | NEMU 来源和本地修改；原许可为 MulanPSL-2.0，文本见 `LICENSES/NEMU-MulanPSL-2.0.txt`。 |
| AM 平台适配、klib 派生部分、AM 测试/基准衍生内容 | AbstractMachine 与 AM Kernels；保留上游 MIT 版权许可，见 `LICENSES/AbstractMachine-MIT.txt` 与 `LICENSES/AM-Kernels.txt`。 |
| RT-Thread 适配文件 | 对应 RT-Thread AM；其 Apache-2.0 原文见 `LICENSES/RT-Thread-Apache-2.0.txt`。未把整个 OS 二进制当作本项目原创成果。 |
| Nangate45 Liberty 和单元模型 | 保留随原工程收集的许可及 Si2 条款，见 `LICENSES/Nangate-Open-Cell-Library.txt`、`B/models/nangate45/LICENSE`。这些教学模型不构成可制造工艺。 |
| ICsprout55 派生分析和旧阶段网表/图示 | 原 PDK 仓库许可见 `LICENSES/ICsprout55.txt`；未附带整个 PDK 或工具分发。 |
| 课程 SoC、RocketChip 及其他完整外部仓库 | 优先保留固定来源和修改脚本；完整外部工作副本不作为原创内容复制。RocketChip 子依赖的相关许可原文在 `LICENSES/`。 |
| HDLBits、NJU、Linux/Missing Semester 等任务题干 | 属于各原作者；任务来源与链接随文本保留，不并入原创代码 MIT 范围。 |

任务文本是用户已有研究归档的来源快照，可能经过 HTML→Markdown 的格式转换和失效离线链接修复。未把本项目答案改写进题干，也未把来源哈希宣称为上游签名。线上页面后续可能变更。

历史练习夹具中的 `example.invalid` 地址是测试数据。上游许可、工具横幅中的作者名/公开联系方式保留用于归属说明。公开快照不携带真实私钥或访问令牌；代码中的私钥检测字符串、Java 临时信任库示例口令等并非有效的用户凭据。

更完整的原始依赖列表见 [THIRD_PARTY_SOURCES.md](THIRD_PARTY_SOURCES.md)。该表描述原私人资料归档，列出的完整第三方仓库不表示全部随本次公开仓库分发。

