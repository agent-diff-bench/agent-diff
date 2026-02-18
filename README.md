# Agent Diff

**Interactive environments for evaluating AI agents & RL training on replicas of 3rd party APIs like Linear or Slack.**

Run it locally (or deploy it). Agents call sandboxed replicas of APIs that behave like the real ones, and you get deterministic diffs of every state change — no external services, no side effects, no rate limits.

<p align="center">
  <a href="https://arxiv.org/abs/2602.11224"><img src="https://img.shields.io/badge/arXiv-2602.11224-b31b1b.svg" alt="arXiv"></a>
  <a href="https://huggingface.co/datasets/hubertmarek/agent-diff-bench"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Dataset-yellow.svg" alt="HuggingFace"></a>
</p>

<p align="center">
  <a href="https://agentdiff.dev">Website</a> •
  <a href="https://agentdiff.mintlify.app/introduction">Docs</a> •
  <a href="https://arxiv.org/abs/2602.11224">Paper</a> •
  <a href="mailto:hubert@uni.minerva.edu">Feedback</a>
</p>

### Try it now

| | Description | |
|---|-------------|---|
| [LangChain Agent](examples/langchain_agent_benchmark.ipynb) | Run AgentDiff Benchmark (LangChain Agents) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/agent-diff-bench/agent-diff/blob/main/examples/langchain_agent_benchmark.ipynb) |
| [ReAct Agent (Paper)](examples/react_agent_benchmark.ipynb) | AgentDiff Benchmark (ReAct)| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/agent-diff-bench/agent-diff/blob/main/examples/react_agent_benchmark.ipynb) |
| [Custom Evaluations Demo](https://colab.research.google.com/drive/1Hext-WWDsm9BxsOrASYoMjgu1N_lN0Fz) | Write your own assertions & evaluate agents | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Hext-WWDsm9BxsOrASYoMjgu1N_lN0Fz) |
| [Prime Intellect](https://app.primeintellect.ai/dashboard/environments/hubert-marek/agent-diff-bench) | Run evals or RL training| [![Prime Intellect](https://img.shields.io/badge/Prime%20Intellect-Run%20Evals-blue.svg)](https://app.primeintellect.ai/dashboard/environments/hubert-marek/agent-diff-bench) |

## Quick Start

### 1. Install SDK

**Python:** [Python SDK docs](sdk/agent-diff-python/README.md)
```bash
uv add agent-diff
```

**TypeScript:** [TS SDK docs](sdk/agent-diff-ts/README.md)
```bash
npm install agent-diff
```

### 2. Configure

<details>
<summary><b> Hosted</b></summary>

1. Sign up at [agentdiff.dev](https://agentdiff.dev) and get your API key
2. Set environment variables:

```bash
export AGENT_DIFF_API_KEY="ad_live_sk_..."
export AGENT_DIFF_BASE_URL="https://api.agentdiff.dev"
```

</details>

<details>
<summary><b>Self-Hosted</b></summary>

```bash
git clone https://github.com/agent-diff-bench/agent-diff.git
cd agent-diff/ops
docker-compose up --build
# Backend runs on http://localhost:8000
```

</details>

### 3. Use

```python
from agent_diff import AgentDiff

client = AgentDiff()

# Create an isolated environment from a template
env = client.init_env(
    templateService="slack",
    templateName="slack_default",
    impersonateUserId="U01AGENBOT9",
)

# Snapshot before agent runs
run = client.start_run(envId=env.environmentId)

# --- Your agent interacts with the API here ---
# SDK provides code execution proxies (Python/Bash) for OpenAI Agents, LangChain, etc.
# Agent writes normal code (e.g. requests.post('https://slack.com/api/chat.postMessage', ...))
# which is automatically intercepted and routed to the sandboxed environment.

from agent_diff import BashExecutorProxy, create_openai_tool
bash = BashExecutorProxy(env.environmentId)
tool = create_openai_tool(bash)  # also: create_langchain_tool, create_smolagents_tool

# Compute state diff and inspect changes
diff = client.diff_run(runId=run.runId)
print(diff.diff['inserts'])   # new records created by agent
print(diff.diff['updates'])   # modified records
print(diff.diff['deletes'])   # deleted records

# Clean up
client.delete_env(envId=env.environmentId)
```

See the [Python SDK](https://agentdiff.mintlify.app/sdks/python/installation) and [TS SDK](https://agentdiff.mintlify.app/sdks/python/installation) for full reference.

## Supported APIs

| Service | Type | Endpoints | Coverage |
|---------|------|-----------|----------|
| **[Box](https://agentdiff.mintlify.app/services/overview)** | REST | 27 | Files, folders, search, comments, tags, shared links, hubs, versioning |
| **[Google Calendar](https://agentdiff.mintlify.app/services/overview)** | REST | 37 | Calendars, events, recurring series, free/busy, ACL, push notifications |
| **[Linear](https://agentdiff.mintlify.app/services/linear/overview)** | GraphQL | 19 | Issues, teams, workflow states, labels, comments, relations, memberships |
| **[Slack](https://agentdiff.mintlify.app/services/slack/overview)** | Web API | 25 | Conversations, messaging, reactions, threading, users, channels |

> **108 unique endpoints** across all 4 services.


## Templates, Seeds & Environments

**Templates** are pre-configured database schemas that serve as the starting point for test environments. Think of them as snapshots of a service's state:
- **Location**: Templates live in PostgreSQL schemas (e.g., `slack_default`, `box_default`, `linear_expanded`, `calendar_base`)
- **Content**: Seeded with realistic data — users, channels, messages, files, folders, issues, calendar events, etc.
- **Seeds**: [box](examples/box/seeds/) | [calendar](examples/calendar/seeds/) | [linear](examples/linear/seeds/) | [slack](examples/slack/seeds/)

<img width="2330" height="688" alt="image" src="https://github.com/user-attachments/assets/481d3f40-e378-402c-9d3c-8a2ab75c880e" />

**Environments** are isolated, temporary copies of a template schema:
- **URL**: Each environment has a unique service URL (e.g., `http://localhost:8000/api/env/{env_id}/services/slack`)
- **Creation**: `client.init_env(templateService="slack", templateName="slack_default", impersonateUserId="U01AGENBOT9")`
- **Cleanup**: `client.delete_env(envId)` or auto-expires after TTL

<img width="2344" height="432" alt="image" src="https://github.com/user-attachments/assets/c61e93f2-1826-429e-8ee7-4a32f4172a38" />



## Run Evaluations

- **[Prime Intellect](https://app.primeintellect.ai/dashboard/environments/hubert-marek/agent-diff-bench)** — Run evals or RL training with no setup required
- **[Colab Notebooks](#try-it-now)** — Run locally with the example notebooks above
- **[Dataset](https://huggingface.co/datasets/hubertmarek/agent-diff-bench)** — 224 tasks across all 4 services (80/20 train/test split)

## Benchmark

The Agent-Diff benchmark comprises **224 tasks** across four enterprise services, each evaluated via deterministic state-diff contracts. Tasks span single-step CRUD operations to long-horizon, multi-entity workflows requiring search, conditional logic, and coordinated state changes.

### Task Distribution

| Metric | Box | Calendar | Linear | Slack | **Total** |
|---|---|---|---|---|---|
| Tasks | 48 | 60 | 57 | 59 | **224** |
| Task horizon _n*_ (range) | 1–13 | 1–24 | 1–13 | 1–14 | 1–24 |
| Task horizon _n*_ (mean) | 4.6 | 5.9 | 5.2 | 5.6 | 5.3 |
| | | | | | |
| **Operation profile** _(% of tasks, non-exclusive)_ | | | | | |
| Search | 92 | 77 | 89 | 64 | 80 |
| Create | 58 | 78 | 63 | 88 | 73 |
| Read | 54 | 82 | 14 | 68 | 55 |
| Update | 62 | 93 | 70 | 37 | 66 |
| Delete | 19 | 53 | 7 | 24 | 26 |


Tasks are characterized along five dimensions: _task horizon_ (minimum API calls under an optimal policy), _operation profile_ (which CRUD primitives are required), _entity scope_ (single vs. multi-entity state changes), _information availability_ (whether identifiers are given explicitly or must be discovered), and _prompt ambiguity_ (how underspecified the target is).

### Results (No-Docs Baseline)

| Model | Box | Calendar | Linear | Slack | **Overall** | Pass % | Cost/test | Score/$ |
|---|---|---|---|---|---|---|---|---|
| deepseek-v3.2 | 76.6 | **87.5** | **94.8** | **86.1** | **88.1** | 76 | $0.03 | 2,938 |
| devstral-2512 | 79.0 | 80.0 | 91.5 | 85.7 | **86.0** | 74 | $0.08 | 1,075 |
| qwen3-vl-235b | 68.4 | 71.0 | 82.0 | 75.8 | **79.2** | 65 | $0.02 | 3,959 |
| kimi-k2-0905 | 66.5 | 72.3 | 88.2 | 82.2 | **75.4** | 64 | $0.04 | 1,885 |
| grok-4.1-fast | 58.5 | 75.7 | 66.0 | 77.1 | **74.9** | 52 | $0.01 | 7,489 |
| gemini-3-flash | **80.3** | 62.2 | 84.0 | 77.5 | **73.8** | 67 | $0.05 | 1,477 |
| gpt-oss-120b | 70.1 | 68.4 | 79.5 | 69.1 | **68.5** | 60 | $0.02 | 3,428 |
| claude-haiku-4.5 | 45.1 | 57.8 | 35.6 | 57.3 | **49.3** | 50 | $0.22 | 224 |
| llama-4-scout | 33.7 | 41.4 | 20.9 | 42.9 | **38.0** | 29 | $0.02 | 1,900 |

Per-service assertion-weighted scores (95% Bayesian CrI). No-docs baseline: agents receive no API documentation and must discover endpoints through exploration. 3 trials per task. Full methodology and documentation ablation results in the [paper](https://arxiv.org/abs/2602.11224).

## Test Suites

| Service | Test Suite | Tests | Coverage |
|---------|-----------|-------|----------|
| Box | [box_bench.json](examples/box/testsuites/box_bench.json) | 48 | File/folder ops, search, tags, comments, hubs, versioning |
| Calendar | [calendar_bench.json](examples/calendar/testsuites/calendar_bench.json) | 60 | Event CRUD, recurring events, free/busy, ACL, lifecycle |
| Linear | [linear_bench.json](examples/linear/testsuites/linear_bench.json) | 57 | Issues, labels, comments, workflow states, teams |
| Slack | [slack_bench.json](examples/slack/testsuites/slack_bench.json) | 59 | Messages, channels, reactions, threading |

Each test defines expected state changes via declarative assertions. See the [assertions docs](https://agentdiff.mintlify.app/core-concepts/assertions) for how they work.

<img width="2516" height="1020" alt="image" src="https://github.com/user-attachments/assets/3270f1f1-5afa-4db2-97b0-c35c070ef44f" />

## Documentation

- **[Python SDK](https://agentdiff.mintlify.app/sdks/python/installation)** — Full Python SDK reference
- **[TypeScript SDK](https://agentdiff.mintlify.app/sdks/typescript/installation)** — Full TypeScript SDK reference
- **[Assertions & Evaluation DSL](https://agentdiff.mintlify.app/core-concepts/assertions)** — Write test assertions
- **[API Reference](https://agentdiff.mintlify.app/api-reference/introduction)** — REST API documentation
- **[Self-Hosting](https://agentdiff.mintlify.app/hosting/docker-setup)** — Docker setup & configuration

## Citation

If you use Agent-Diff in your research, please cite:

```bibtex
@article{pysklo2025agentdiff,
  title={Agent-Diff: Benchmarking LLM Agents on Enterprise API Tasks via Code Execution with State-Diff-Based Evaluation},
  author={Pysklo, Hubert M. and Zhuravel, Artem and Watson, Patrick D.},
  journal={arXiv preprint arXiv:2602.11224},
  year={2025}
}
```

