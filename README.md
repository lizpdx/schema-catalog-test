
# Schema Catalog Test

Testing automated schema tracking and DataHub integration.

## Quick Start
```bash
# Generate metadata and ingest to DataHub
./scripts/ingest_to_datahub.sh

# Or step by step:
python3 scripts/generate_metadata.py
datahub ingest -c datahub_ingestion.yml
```

## View in DataHub

Open http://localhost:9002 and login with `datahub` / `datahub`

## Directory Structure

- `models/` - Python data models (versioned)
- `scripts/` - Automation scripts
- `metadata/` - Generated DataHub metadata (gitignored)
- `.github/workflows/` - GitHub Actions for CI/CD
