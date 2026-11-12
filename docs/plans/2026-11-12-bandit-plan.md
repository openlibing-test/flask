# Bandit Documentation Verification Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在 Flask 实测文档 GitHub 全量扫描及私有上传链路，保存可复核证据。

**Architecture:** 复用当前干净检出，在独立验证分支新增单个工作流和报告校验脚本。固定文档、Bandit 和插件版本，扫描后再检出私有插件。

**Tech Stack:** GitHub Actions, Python 3.12, Bandit 1.9.4, SARIF 2.1.0, GitHub CLI.

---

### Task 1: Configure workflow

Create `.github/workflows/bandit-scan.yml` and `.github/bandit/verify-sarif.py`. Install documented Bandit extra, execute documented scan and record exit status; verify report structure, tool identity and repository source locations. Use secret-backed private checkout after scanning and upload with beta environment. Archive evidence even on failure.

### Task 2: Execute verification

Check Python syntax, YAML parsing and `git diff --check`. Commit only intended files, push validation branch, wait for the resulting Actions run. Inspect step conclusions and full upload logs. Correct implementation errors and rerun if necessary.

### Task 3: Report evidence

Download run metadata, logs and artifacts into `validation-results/flask-bandit/`. Audit result counts, paths and source snippets. Write verification report with exact run/commit links, documented deviations, confirmed documentation issues and untested boundaries. No platform UI claim without UI evidence.
