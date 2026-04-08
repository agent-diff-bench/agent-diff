# REST Service Mock Templates

These files are seedable mock templates for the REST MVP generator.

Token placeholders:

- `__APP_NAME__`
- `__APP_SLUG__`
- `__SERVICE_MOUNT_NAME__`

Expected replacement flow:

1. Copy this template directory into the app workspace.
2. Replace placeholders with app-specific values.
3. Expand resource declarations and endpoint implementations packet by packet.

The files intentionally include standardized markers so endpoint-level edits can
target bounded sections without restructuring modules.
