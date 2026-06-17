# MINDSTREAM - Personal Knowledge Assistant

## 项目目标

**业务背景**：企业做 Agent 的核心需求是「知识传承 + 问题诊断」——老员工的经验无法传递给新人，导致设备故障只能依赖老师傅。企业希望通过 RAG/Agent 沉淀专家经验，让新员工能快速定位问题，而不是事事问人。

**个人场景映射**：个人知识管理本质上是同一问题——你的笔记就是「个人经验」，面试问答就是「故障诊断」，RAG+Agent 工作流就是「知识传承 + 推理输出」。

**技术目标**：掌握 RAG + LangGraph + Agent 开发，命中成都 AI 应用开发工程师岗位。

---

## 业务场景

```
设备故障 / 问题现象
      ↓
   Agent 分析
      ↓
  选择工具检索
      ↓
  推理 + 生成
      ↓
排查步骤 + 参考文档 + 历史案例
```

例如：员工输入「设备报警 E203」→ Agent 输出「可能原因、排查步骤、参考手册章节」

这个场景的核心不是「聊天」，而是：
- **知识检索**：从大量文档中找到相关内容
- **意图理解**：分析用户想知道什么
- **结构化输出**：给步骤、给原因、给参考，而不是泛泛回答

---

## 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| 后端框架 | FastAPI | 已有基础 |
| RAG 框架 | LangChain + LangGraph | JD 明确要求，重点学 |
| 向量数据库 | Qdrant | 比 pgvector 更专业 |
| 关系数据库 | PostgreSQL | 文档元数据、用户数据 |
| 缓存 | Redis | 会话缓存、Query Cache |
| 文件存储 | 本地文件系统 | 简化替代 MinIO |
| 文档解析 | LangChain Document Loaders | PDF/Markdown/TXT |
| AI 模型 | Gemini / Qwen / GPT | 多模型切换 |
| 前端 | React + TypeScript + Next.js | 有 React 基础 |

---

## 核心功能

### 1. 知识库管理
- **挂载本地目录**（同步，不是上传）
- 文档解析（PDF/Markdown/TXT）
- 文档切分（chunking）
- Embedding 入库 Qdrant
- 目录状态查看、重新索引

### 2. RAG 问答
- 语义检索 Qdrant
- 结合上下文生成回答
- 引用来源标注
- Redis Query Cache（同问题直接返回）

### 3. 问题诊断模式（企业场景模拟）
```
输入问题现象 → Agent 分析意图 → 检索相关文档 → 生成结构化回答
```
- 不是泛泛回答，而是：可能原因 + 排查步骤 + 参考文档
- 模拟企业故障诊断 Agent 的工作方式

### 4. 多模型调度
- Gemini / Qwen / GPT 接口封装
- 模型切换开关

### 5. LangGraph 工作流
```
Question → Parse Intent → Retrieve → Generate → Review → Output
```
- Parse Intent：分析用户想知道什么（问答/摘要/诊断）
- Retrieve：检索相关 chunks
- Generate：生成回答
- Review：检查回答质量、引用是否正确
- Output：返回结构化结果

---

## 项目定位

**当前场景**：
```
Personal Knowledge Platform
自部署个人知识平台
```
用个人笔记管理验证 RAG + LangGraph 架构。

**可扩展场景**：
```
Enterprise Knowledge Assistant     → 企业知识问答（员工查手册）
Equipment Troubleshooting Assistant → 设备故障诊断（工人查错）
Internal Technical Support Agent   → 内部技术助手（IT 问答）
```

架构设计预留扩展能力，当前实现个人场景，但对接真实企业需求。

---

## 环境区分

### 开发环境（dev）
- 代码改动自动重载（mount 源码 volume）
- 本地模型调用（Ollama / API 模拟）
- 调试日志全开
- PostgreSQL/Redis/Qdrant 用 docker compose 开发服务
- 前端 dev server 热重载

### 生产环境（prod）
- 镜像构建后运行（`docker compose up -d`）
- 必须配置 `.env` 读取 API Key（不硬编码）
- PostgreSQL/Redis/Qdrant 持久化 volume
- 前端 `next build && next start`
- 健康检查、优雅关闭

```
.env 文件（不提交）
├── DATABASE_URL
├── REDIS_URL
├── QDRANT_URL
├── GEMINI_API_KEY
├── QWEN_API_KEY
├── OPENAI_API_KEY
└── MODEL_PROVIDER=gemini
```

---

## 部署方式

用户 clone 后：

```bash
git clone mindstream
cd mindstream

# 1. 配置 API Key
cp .env.example .env
vim .env  # 填入 API Key

# 2. 挂载本地知识库目录（可选）
# 编辑 docker-compose.yml 的 volumes

# 3. 启动
docker compose up -d
```

访问 `http://localhost:3000`

---

## 架构图

```
┌─────────────────────────────────────────────────┐
│           React + TS + Next.js                   │
│                   用户界面                        │
└──────────────────────┬────────────────────────┘
                       │ HTTP
                       ▼
┌─────────────────────────────────────────────────┐
│                   FastAPI                        │
│  ┌─────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ 文档模块 │  │ RAG 模块  │  │ LangGraph    │   │
│  │         │  │          │  │ 工作流        │   │
│  └────┬────┘  └────┬─────┘  └──────┬───────┘   │
└───────┼─────────────┼───────────────┼───────────┘
        │             │               │
        ▼             ▼               ▼
┌───────────┐  ┌───────────┐   ┌─────────────┐
│ 本地文件系统│  │  Qdrant   │   │  LLM API    │
│ (文件存储) │  │ (向量库)  │   │ Gemini/Qwen │
└───────────┘  └───────────┘   └─────────────┘
               ┌───────────┐
               │ PostgreSQL│
               │ (元数据)  │
               └───────────┘
               ┌───────────┐
               │   Redis   │
               │ (缓存)    │
               └───────────┘
```

---

## 面试知识点

### 为什么做这个项目（必问）

**不要说**：为了学习 RAG。

**要说**：企业做 Agent 很多时候是为了沉淀专家经验、帮助新人快速定位问题。我希望通过个人知识管理场景模拟这个过程——我的笔记就是「个人经验」，面试问答就是「故障诊断」，RAG+Agent 工作流就是「知识传承 + 推理输出」。

### RAG 全流程
- Chunking 策略（为什么 500/1000 字符，Overlap 多少）
- Embedding 模型选择（BGE / text-embedding-3-small，为什么）
- ANN 索引原理（HNSW）
- Retrieval 优化（rerank、query expansion）

### LangChain / LangGraph
- LCEL（LangChain Expression Language）
- LangGraph 状态机、节点、边
- 为什么要用 Graph 而不是简单链式调用
- **为什么 Agent 需要工作流而不是直接 RAG**：意图分析、工具选择、多步骤推理

### Redis
- Query Cache 实现（同一问题直接返回）
- 缓存失效策略

### Qdrant
- 为什么选 Qdrant 而不是 Milvus
- HNSW 索引原理

### 工程能力
- Docker 容器化部署
- PostgreSQL 数据库设计
- API 设计（RESTful）

---

## 开发阶段

### Phase 1：基础 RAG（1-2 周）
- [ ] FastAPI 项目骨架
- [ ] **目录挂载 + 同步**（不是上传）
- [ ] 文档解析（PDF/Markdown/TXT）
- [ ] Qdrant 接入
- [ ] 基础 RAG 问答 API

### Phase 2：LangGraph + Redis（1-2 周）
- [ ] LangGraph 工作流（5 节点，含 Intent Parse）
- [ ] 意图分析：问答 / 摘要 / 诊断
- [ ] Redis Query Cache
- [ ] 多轮对话

### Phase 3：多模型 + 前端（1-2 周）
- [ ] 多模型封装（Gemini/Qwen/GPT）
- [ ] React + TS + Next.js 前端
- [ ] 文档管理界面（目录绑定、状态查看）
- [ ] 问答界面（引用来源）

### Phase 4：Docker + 部署（1 周）
- [ ] `docker-compose.yml`（dev vs prod profile）
- [ ] `.env.example` 示例文件
- [ ] 项目文档补全

---

## 上线安排

### 开发环境
- 全部服务本地运行：FastAPI dev server + docker compose (Postgres/Redis/Qdrant)
- 前端 `npm run dev`
- 代码改动热重载

### 生产环境
- `docker compose --profile prod up -d`
- 前端构建：`docker compose -f docker-compose.yml exec web npm run build`
- 或单独构建镜像：`docker build -t mindstream .`

### 部署检查清单
```
[ ] .env 文件已配置所有 API Key
[ ] Postgres/Redis/Qdrant 数据已持久化
[ ] 知识库目录已挂载
[ ] 健康检查通过：/health 端点
[ ] 端口未冲突（3000/5432/6379/6333）
```

---

## 后续扩展（MVP 完成后）

- **V2 - Troubleshooting Mode**：输入问题现象，输出可能原因 + 排查步骤 + 参考文档（贴近企业故障诊断场景）
- **MCP Server**：暴露知识库工具给 AI Agent 调用
- **Robot Framework**：接口自动化测试

---

## 当前状态

- [ ] 技术方案确认
- [ ] 开发环境准备
- [ ] Phase 1 开始