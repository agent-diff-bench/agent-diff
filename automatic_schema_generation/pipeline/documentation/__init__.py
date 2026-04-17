"""Stage 2: Structured documentation output (endpoints.json, resources.json)."""

from pipeline.documentation.endpoints import classify_responses, generate_endpoints_document, write_endpoints_document
from pipeline.documentation.resources import generate_resources_document, write_resources_document
