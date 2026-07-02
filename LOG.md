# CHANGELOG / 学习开发记录

## 2026-06-15

### 项目启动

- [x] 确定项目定位：Self-hosted Personal Knowledge Platform
- [x] 参考项目：Khoj、Open WebUI、Dify
- [x] 确认方向：不走 SaaS，走开源自部署路线
- [x] 业务场景对齐：企业知识问答 / 设备故障诊断 Agent
- [x] 技术栈确认：FastAPI + LangChain + LangGraph + Qdrant + PostgreSQL + Redis
- [x] Git 初始化 + GitHub 仓库连接

---

## 学习记录

（待补充）

---

## 开发记录

### 2026-06-16

- [x] 目录结构和核心接口定义评审
- [x] GitHub: https://github.com/Roxie-Deng/mindstream

### 2026-07-02

- [x] FastAPI 项目骨架初始化
- [x] 使用 `uv + pyproject.toml`（不用 requirements.txt）
- [x] `/health` 和 `/api/v1/health` 接口验证通过

**启动命令：**
```bash
cd mindstream
uv run uvicorn app.main:app --reload --port 8000
```

**验证：**
```bash
curl --noproxy '*' http://localhost:8000/health
# -> {"status":"healthy"}
```