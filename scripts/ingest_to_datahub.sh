
#!/bin/bash
set -e

echo "🔄 Generating metadata from models..."
python3 scripts/generate_metadata.py

echo "📤 Ingesting to DataHub..."
datahub ingest -c datahub_ingestion.yml

echo "✅ Done! Check DataHub at http://localhost:9002"
