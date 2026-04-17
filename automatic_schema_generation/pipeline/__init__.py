"""Pipeline 2.0 — config-first OpenAPI analysis and code generation.

Stages:
  extraction/      — mechanical reference extraction from OpenAPI specs
  documentation/   — structured output (endpoints.json, resources.json)
  aliases/         — alias expansion loop (suggest, review, apply)
  implementation/  — LLM prompt construction for entity implementation
"""
