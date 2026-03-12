# Agent Diff

**Interactive environments for evaluating AI agents & RL training on replicas of 3rd party APIs like Linear or Slack.**

Run it locally (or deploy it). Agents call sandboxed replicas of APIs that behave like the real ones, and you get deterministic diffs of every state change — no external services, no side effects, no rate limits.

### Run Agent-Diff Benchmark

| Example | Description |
|---|---|
| [LangChain Agent](examples/langchain_agent_benchmark.ipynb) | Run AgentDiff Benchmark with LangChain agents |
| [ReAct Agent](examples/react_agent_benchmark.ipynb) | Run AgentDiff Benchmark with a custom ReAct loop |
| `examples/` notebooks | Write custom evaluations and inspect benchmark workflows locally |


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

1. Obtain an API key from your deployment or evaluation organizer
2. Set environment variables:

```bash
export AGENT_DIFF_API_KEY="ad_live_sk_..."
export AGENT_DIFF_BASE_URL="<base-url>"
```

</details>

<details>
<summary><b>Self-Hosted</b></summary>

```bash
git clone <repository-url>
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

See the local SDK references in `sdk/agent-diff-python/README.md` and `sdk/agent-diff-ts/README.md`.

## Supported APIs

| Service | Type | Endpoints | Coverage |
|---------|------|-----------|----------|
| **Box** | REST | 27 | Files, folders, search, comments, tags, shared links, hubs, versioning |
| **Google Calendar** | REST | 37 | Calendars, events, recurring series, free/busy, ACL, push notifications |
| **Linear** | GraphQL | 19 | Issues, teams, workflow states, labels, comments, relations, memberships |
| **Slack** | Web API | 25 | Conversations, messaging, reactions, threading, users, channels |

> **108 unique endpoints** across all 4 services.


## Templates, Seeds & Environments

**Templates** are pre-configured database schemas that serve as the starting point for test environments. Think of them as snapshots of a service's state:
- **Location**: Templates live in PostgreSQL schemas (e.g., `slack_default`, `box_default`, `linear_expanded`, `calendar_base`)
- **Content**: Seeded with realistic data — users, channels, messages, files, folders, issues, calendar events, etc.
- **Seeds**: [box](examples/box/seeds/box_default.json) | [calendar](examples/calendar/seeds/calendar_default.json) | [linear](examples/linear/seeds/linear_default.json) | [slack](examples/slack/seeds/slack_default.json)

**Environments** are isolated, temporary copies of a template schema:
- **URL**: Each environment has a unique service URL (e.g., `http://localhost:8000/api/env/{env_id}/services/slack`)
- **Creation**: `client.init_env(templateService="slack", templateName="slack_default", impersonateUserId="U01AGENBOT9")`
- **Cleanup**: `client.delete_env(envId)` or auto-expires after TTL

## Agent-Diff Bench

The Agent-Diff benchmark comprises **224 tasks** across four enterprise services, each evaluated via deterministic state-diff contracts. Tasks span single-step CRUD operations to long-horizon, multi-entity workflows requiring search, conditional logic, and coordinated state changes.

### Agent-Diff Bench Results

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

Per-service assertion-weighted scores (95% Bayesian CrI). No-docs baseline: agents receive no API documentation and must discover endpoints through exploration. 3 trials per task.

### Training on Agent-Diff

Agent-Diff environments double as training infrastructure. We used the benchmark to generate rollouts and fine-tune models on API tool-calling tasks:

| Method | Model | Base | Trained (eval set) | Delta |
|---|---|---|---|---|
| RL | Qwen3-30B-A3B | 0.31 | 0.55 | **+77%** |
| SFT (LoRA) | Ministral-3-14B | 0.28 | 0.35 | **+24%** |

The SFT pipeline filters high-reward Devstral rollouts (reward > 0.8), applies command flattening and error turn removal, and trains a LoRA adapter (rank 64) with prompt-level train/val splits.


## Documentation

- **[Python SDK](sdk/agent-diff-python/README.md)** — Full Python SDK reference
- **[TypeScript SDK](sdk/agent-diff-ts/README.md)** — Full TypeScript SDK reference
- **[Assertions & Evaluation DSL](docs/evaluation-dsl.md)** — Write test assertions
- **[API Reference](docs/api-reference.md)** — REST API documentation
- **[Getting Started](docs/getting-started.md)** — Local setup and usage

## Citation

If you use Agent-Diff in your research, please cite:

```bibtex
@article{anonymous2026agentdiff,
  title={Agent-Diff: Benchmarking LLM Agents on Enterprise API Tasks via Code Execution with State-Diff-Based Evaluation},
  author={Anonymous},
  journal={Under review},
  year={2026}
}
```

