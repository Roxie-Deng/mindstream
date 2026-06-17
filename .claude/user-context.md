---
name: user-context
description: 用户背景、目标岗位、项目背景
type: user
---

## 基本信息

- 目标岗位：成都 AI 应用开发工程师
- 技术栈：FastAPI / LangChain / LangGraph / PostgreSQL / Redis / Qdrant / Next.js
- 现状：简历需要 AI 项目经验，需要能够回答面试问题

---

## 项目背景

- 项目名：MindStream
- 定位：Self-hosted Personal Knowledge Platform（可扩展到企业知识助手）
- 核心价值：RAG + LangGraph 工作流，模拟企业故障诊断 Agent 场景
- 参考：Khoj、Open WebUI、Dify

---

## 协作方式

- 每次只推进一个模块：需求分析 → 模块设计 → 数据库设计 → API设计 → 代码实现
- 每次完成后输出：设计思路 + 技术选型 + 面试问题 + 项目文档 + 面试笔记
- 不生成整个项目，先讨论后实现

---

## 决策

- 多租户现在不做，只留 `user_id INT DEFAULT 1` 字段
- 单用户起步，快速出活
- password 暂不留