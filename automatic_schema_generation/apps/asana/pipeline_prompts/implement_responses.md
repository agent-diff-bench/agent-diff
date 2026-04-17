Read the file `/Users/azh/agent-diff/automatic_schema_generation/apps/asana/pipeline_out/responses.json`. It contains all component response definitions from the Asana API spec, along with their referenced schemas.

Implement the standard HTTP error response handlers in `/Users/azh/agent-diff/backend/src/services/asana/core/errors.py`. For each standard error response (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error, etc.), create a constructor function that returns the correct response shape matching the schemas in the file.

Skip domain-specific or resource-specific responses — only implement responses that represent standard HTTP error patterns reusable across all endpoints.

Read the existing `/Users/azh/agent-diff/backend/src/services/asana/core/errors.py` first and preserve any code already there.