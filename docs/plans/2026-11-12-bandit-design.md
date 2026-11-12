# Bandit 文档验证设计

用户已确认采用完整链路方案。目标仓库 openlibing-test/flask，使用现有干净检出及独立 validation/bandit-docs 分支，不修改默认分支。

参考文档固定提交 69df05f3c175d0e10710df253ba9931d5dda431f 的 GitHub 全量扫描示例。锁定 Python 3.12、bandit[sarif]==1.9.4，执行原文全仓扫描命令；0/1 按非门禁处理，其他退出码失败。

在扫描后通过组织 Secret PRIVATE_ACTIONS_READ_TOKEN 检出私有上传插件，固定 source-platform-detection 对应提交 05d5ea9e9f9a76497022ccab322f6dc22d827820。先校验 SARIF，再以 beta 环境执行 OIDC、OBS 与回调。检出不持久化凭证，插件目录不进入扫描。

采用分支 push 首次触发，保留 workflow_dispatch。归档原始和上传后报告、工具版本、退出码和统计。分别判断扫描、报告、上传、回调，不把绿色运行视作 UI 验收。替代方案是仅扫描，但不能验证文档端到端可靠性，因此未采用。
