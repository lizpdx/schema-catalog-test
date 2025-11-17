
#!/usr/bin/env python3
"""Generate DataHub metadata from Python models"""

import ast
import json
from pathlib import Path
from datetime import datetime

def extract_class_fields(python_file):
    """Parse Python file and extract class fields"""
    with open(python_file) as f:
        tree = ast.parse(f.read())
    
    fields = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    field_name = item.target.id
                    field_type = ast.unparse(item.annotation) if item.annotation else "unknown"
                    fields.append({
                        "fieldPath": field_name,
                        "type": {"type": {"com.linkedin.pegasus2avro.schema.StringType": {}}},
                        "nativeDataType": field_type,
                        "description": f"{field_name} field"
                    })
            return class_name, fields
    return None, []

def create_dataset_metadata(file_path, version):
    """Create DataHub dataset metadata"""
    class_name, fields = extract_class_fields(file_path)
    
    if not class_name:
        return None
    
    return {
        "auditHeader": None,
        "proposedSnapshot": {
            "com.linkedin.pegasus2avro.metadata.snapshot.DatasetSnapshot": {
                "urn": f"urn:li:dataset:(urn:li:dataPlatform:custom,schema-catalog-test.{class_name},PROD)",
                "aspects": [
                    {
                        "com.linkedin.pegasus2avro.dataset.DatasetProperties": {
                            "customProperties": {
                                "version": version,
                                "source": str(file_path),
                                "last_modified": datetime.now().isoformat()
                            },
                            "description": f"{class_name} model {version}",
                            "tags": []
                        }
                    },
                    {
                        "com.linkedin.pegasus2avro.schema.SchemaMetadata": {
                            "schemaName": class_name,
                            "platform": "urn:li:dataPlatform:custom",
                            "version": 0,
                            "hash": "",
                            "platformSchema": {
                                "com.linkedin.pegasus2avro.schema.OtherSchema": {
                                    "rawSchema": f"class {class_name}"
                                }
                            },
                            "fields": fields
                        }
                    }
                ]
            }
        }
    }

if __name__ == "__main__":
    # Generate metadata for all Python files
    models_dir = Path("models")
    output_dir = Path("metadata")
    output_dir.mkdir(exist_ok=True)
    
    for py_file in models_dir.rglob("*.py"):
        version = py_file.parent.name
        metadata = create_dataset_metadata(py_file, version)
        
        if metadata:
            output_file = output_dir / f"{py_file.stem}_{version}.json"
            with open(output_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"✅ Generated: {output_file}")
