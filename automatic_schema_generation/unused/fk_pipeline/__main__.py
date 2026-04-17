"""Allow running as: python -m fk_pipeline <app_config.yaml>"""
from .cli import main

raise SystemExit(main())
