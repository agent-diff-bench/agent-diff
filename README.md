# Agent Diff

**Interactive environments for evaluating AI agents & RL training on replicas of 3rd party APIs like Linear or Slack.**

Run it locally (or deploy it). Agents call sandboxed replicas of APIs that behave like the real ones, and you get deterministic diffs of every state change — no external services, no side effects, no rate limits.

<p align="center">
  <a href="https://arxiv.org/abs/2602.11224">Paper (arXiv)</a> •
  <a href="https://agentdiff.dev">Website</a> •
  <a href="https://agentdiff.mintlify.app/introduction">Docs</a> •
  <a href="https://huggingface.co/datasets/hubertmarek/agent-diff-bench">Dataset</a> •
  <a href="https://app.primeintellect.ai/dashboard/environments/hubert-marek/agent-diff-bench">Prime Intellect</a> •
  <a href="mailto:hubert@uni.minerva.edu">Feedback</a>
</p>


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
git clone https://github.com/hubertpysklo/agent-diff.git
cd agent-diff/ops
docker-compose up --build
# Backend runs on http://localhost:8000
```

</details>

### 3. Flow
```python
from agent_diff import AgentDiff

# Self-hosted (defaults to http://localhost:8000)
client = AgentDiff()

# Initialise isolated environment from a template. See: examples/slack/seeds
env = client.init_env(templateService="slack", templateName="slack_default",
impersonateUserId="U01AGENBOT9", TTL="3600") #impersonateUserId - seeded user account that agent will use

# print(env.environmentUrl) = http://localhost:8000/api/env/{environmentId}/services/slack

# Take before snapshot
run = client.start_run(envId=env.environmentId)

# Your agent does stuff using the environment URL 
# You can swap the URLs in MCPs or use the code executor tool (Python or bash) with a proxy 

# Using CodeExecutorProxy with OpenAI Agents SDK (For Vercel AI, check TS SDK docs)
from agent_diff import PythonExecutorProxy, create_openai_tool
from agents import Agent, Runner

# Create executor (auto-loads from AGENT_DIFF_API_KEY and AGENT_DIFF_BASE_URL env vars)
python_executor = PythonExecutorProxy(env.environmentId)
python_tool = create_openai_tool(python_executor) 

agent = Agent(
        name="Slack Assistant",
        instructions="Use execute_python tool to interact with Slack API at https://slack.com/api/*. Complete the task using the tools provided. Authentication is handled automatically via proxy. Leave a placeholder credential where you would add a real token.",
        tools=[python_tool] # python_tool (or bash_tool) where agent will write code
    )

response = await Runner.run(agent, "Post 'Hello' to Slack channel #general")

# The agent writes normal code like:
# requests.post('https://slack.com/api/chat.postMessage', ...)
# But it will be proxied to the temporary sandbox environment
# e.g. transforms:
# from: https://api.slack.com/api/conversations.list
# to: http://localhost:8000/api/env/{environmentId}/services/slack/conversations.list 

# Compute diff (changes in the environment) and get results
diff = client.diff_run(runId=run.runId)

# Inspect changes
print(diff.diff['inserts'])   # New records, e.g. new message or user added by agent
print(diff.diff['updates'])   # Modified records, edited message
print(diff.diff['deletes'])   # Deleted records, deleted message, linear issue, etc.

# Clean up
client.delete_env(envId=env.environmentId)

```

## Supported APIs

- **Box** – REST API for file/folder management, search, comments, tags, shared links, hubs, and content versioning. See [`backend/src/services/box/README.md`](backend/src/services/box/README.md). 27 endpoints.

- **Google Calendar** – REST API for calendar CRUD, events, recurring series, free/busy queries, ACL rules, calendar list management, and push notifications. See [`backend/src/services/calendar/README.md`](backend/src/services/calendar/README.md). 37 endpoints.

- **Linear** – GraphQL API for issue tracking, teams, workflow states, labels, comments, relations, and memberships. See [`backend/src/services/linear/README.md`](backend/src/services/linear/README.md). 19 endpoints.

- **Slack** – Web API for conversations, messaging, reactions, threading, users, and channels. See [`backend/src/services/slack/README.md`](backend/src/services/slack/README.md). 25 endpoints.

> **108 unique endpoints** across all 4 services.

## Templates, Seeds & Environments

**Templates** are pre-configured database schemas that serve as the starting point for test environments. Think of them as snapshots of a service's state:
- **Location**: Templates live in PostgreSQL schemas (e.g., `slack_default`, `linear_base`)
- **Content**: Templates are seeded during startup time from seeds with data like users, channels, messages, issues, etc.
- **Example Seeds**: **[slack_default](examples/slack/seeds/slack_bench_default.json)** - sample users, channels and messages.

<img width="2330" height="688" alt="image" src="https://github.com/user-attachments/assets/481d3f40-e378-402c-9d3c-8a2ab75c880e" />

**Environments** are isolated, temporary copies of a template schema:
- **URL**: Each environment has a unique service URL (e.g., `http://localhost:8000/api/env/{env_id}/services/slack`)
- **Creation**: `client.init_env(templateService="slack", templateName="slack_default", impersonateUserId="U01AGENBOT9")`
- **Cleanup**: `client.delete_env(envId)` or auto-expires after TTL

<img width="2344" height="432" alt="image" src="https://github.com/user-attachments/assets/c61e93f2-1826-429e-8ee7-4a32f4172a38" />


## CodeExecutorProxy

SDK provides **code execution proxies** - tools for AI agents. You add it to your toolbox in Vercel AI SDK, Langchain or OpenAI Agents, making LLM write Python or Bash code to talk with Slack or Linear API. Requests will automatically be intercepted and routed to isolated test environments. This enables agents to interact with service replicas without any code changes. See more in: **[Python SDK](sdk/agent-diff-python/README.md)** 


## Paper

> **Agent-Diff: Benchmarking LLM Agents on Enterprise API Tasks via Code Execution with State-Diff-Based Evaluation**
> Hubert M. Pysklo, Artem Zhuravel, Patrick D. Watson
> *Pre-print. Under review for KDD 2026.*
> [arXiv:2602.11224](https://arxiv.org/abs/2602.11224)

If you use Agent-Diff in your research, please cite:

```bibtex
@article{pysklo2025agentdiff,
  title={Agent-Diff: Benchmarking LLM Agents on Enterprise API Tasks via Code Execution with State-Diff-Based Evaluation},
  author={Pysklo, Hubert M. and Zhuravel, Artem and Watson, Patrick D.},
  journal={arXiv preprint arXiv:2602.11224},
  year={2025}
}
```

## Run Evaluations

The fastest way to run Agent-Diff evaluations is via **[Prime Intellect](https://app.primeintellect.ai/dashboard/environments/hubert-marek/agent-diff-bench)** — run evals or RL training with no setup required.

Alternatively, run locally or self-hosted using the SDK (see [To run evaluations](#to-run-evaluations) below).

**Resources:**
- **Dataset**: [hubertmarek/agent-diff-bench](https://huggingface.co/datasets/hubertmarek/agent-diff-bench) — 224 tasks across all 4 services (80/20 train/test split)
- **Prime Intellect**: [agent-diff-bench on Prime Lab](https://app.primeintellect.ai/dashboard/environments/hubert-marek/agent-diff-bench) — hosted evaluations & RL training

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
| | | | | | |
| **Entity scope** | | | | | |
| Single-entity | 28 | 11 | 33 | 33 | 105 |
| Multi-entity | 20 | 49 | 24 | 26 | 119 |
| | | | | | |
| **Information availability** | | | | | |
| Explicit | 6 | 10 | 25 | 36 | 77 |
| Implicit | 42 | 50 | 32 | 23 | 147 |
| | | | | | |
| **Prompt ambiguity** | | | | | |
| Low | 24 | 13 | 37 | 27 | 101 |
| Medium | 17 | 45 | 19 | 22 | 103 |
| High | 7 | 2 | 1 | 10 | 20 |

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

## Evaluations & Test Suites

Collections of test cases with assertions that you can run against agent runs using evaluations.

- **[box_bench.json](examples/box/testsuites/box_bench.json)** - test cases covering file/folder operations, search, tags, comments, hubs, and content versioning
- **[calendar_bench.json](examples/calendar/testsuites/calendar_bench.json)** - test cases covering event CRUD, recurring events, free/busy queries, ACL management, and calendar lifecycle
- **[linear_bench.json](examples/linear/testsuites/linear_bench.json)** - test cases covering issue management, labels, comments, workflow states, and team operations
- **[slack_bench.json](examples/slack/testsuites/slack_bench.json)** - test cases covering message sending, channel ops, reactions, threading

<img width="2985" height="1966" alt="pass_rates_annotated" src="https://github.com/user-attachments/assets/f5c59c81-c3bd-427e-977c-a5c2c0695e86" />

- **[Evaluation DSL](docs/evaluation-dsl.md)** - Check DSL docs on how it works.

<img width="2516" height="1020" alt="image" src="https://github.com/user-attachments/assets/3270f1f1-5afa-4db2-97b0-c35c070ef44f" />


### To run evaluations:

```python
from agent_diff import AgentDiff, PythonExecutorProxy, BashExecutorProxy, create_openai_tool
from agents import Agent, Runner

client = AgentDiff()


suite_list = client.list_test_suites(name="Slack Bench")
slack_suite = suite_list.testSuites[0]
suite = client.get_test_suite(slack_suite.id, expand=True)

evaluation_results = []

for test in suite.tests:
    prompt = test.prompt
    test_id = test.id

    #In test suite you define which env seed template is used for each test
    env = client.init_env(testId=test_id)

    # This function will take a snapshot before run
    run = client.start_run(envId=env.environmentId, testId=test_id)


    bash_executor = BashExecutorProxy(env.environmentId)  # Auto-loads from env vars
    bash_tool = create_openai_tool(bash_executor)

    agent = Agent(
        name="Slack Assistant",
        instructions="Use execute_bash tool with curl to interact with Slack API at https://slack.com/api/*. Authentication is handled automatically.",
        tools=[bash_tool]
    )

    response = await Runner.run(agent, prompt)

    #This function will take a 2nd snapshot, run diff and assert results against expected state defined in test suite
    
    #computes eval
    client.evaluate_run(runId=run.runId)
    
    #returns score runId, full diff and score (0/1)
    run_result = client.get_results_for_run(runId=run.runId)

    evaluation_results.append(run_result) 

    client.delete_env(envId=env.environmentId)
```

### Example output:

<img width="1669" height="878" alt="image" src="https://github.com/user-attachments/assets/096393d2-e464-4a3d-b0a8-b188af5cf8a9" />


## Documentation

- **[Python SDK](sdk/agent-diff-python/README.md)** - Complete Python SDK reference
- **[TS SDK](sdk/agent-diff-ts/README.md)** - Complete TS SDK reference
- **[Evaluation DSL](docs/evaluation-dsl.md)** - Write test assertions
- **[API Reference](docs/api-reference.md)** - REST API documentation

