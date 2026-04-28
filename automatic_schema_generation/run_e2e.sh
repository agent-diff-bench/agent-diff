#!/usr/bin/env bash
# End-to-end pipeline driver for multiple apps.
#
# For each app passed on the command line (or the default trio if none
# given), runs the full pipeline through register_tests, then runs
# seed_template + test_endpoints. Per-app failures stop the run.
#
# Usage:
#   ./run_e2e.sh                      # asana github todoist
#   ./run_e2e.sh asana                # one app
#   ./run_e2e.sh asana todoist        # any subset
#
# Requires the backend container to be up (``docker compose up`` from
# ops/), since seed_template + test_endpoints both shell into it.

set -euo pipefail

cd "$(dirname "$0")"

APPS=("${@:-asana github todoist}")
if [[ "${#APPS[@]}" -eq 1 && "${APPS[0]}" == "asana github todoist" ]]; then
    APPS=(asana github todoist)
fi

echo ">>> Running end-to-end pipeline for: ${APPS[*]}"
echo

# Phase 1: build (no docker dependency). Each app runs through the
# scaffold/configure/extract/implement/register chain in isolation.
for app in "${APPS[@]}"; do
    echo "================================================================"
    echo "  BUILD — $app"
    echo "================================================================"
    python -m pipeline.run "apps/$app/app.yaml" --up-to-stage register_tests
    echo
done

# Phase 2: seed + test (docker dependency). Done after every app's code
# is generated so the backend only reseeds three times instead of once
# per stage interleave.
for app in "${APPS[@]}"; do
    echo "================================================================"
    echo "  SEED + TEST — $app"
    echo "================================================================"
    python -m pipeline.run "apps/$app/app.yaml" --stage seed_template
    python -m pipeline.run "apps/$app/app.yaml" --stage test_endpoints
    echo
done

echo ">>> All done."
