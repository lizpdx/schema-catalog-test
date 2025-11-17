
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def extract_fields(file_path):
    """Extract field names from Python class"""
    with open(file_path) as f:
        fields = []
        for line in f:
            if ':' in line and 'class' not in line:
                field = line.strip().split(':')[0].strip()
                if field and not field.startswith('#'):
                    fields.append(field)
        return fields

def compare_schemas(old_file, new_file):
    """Compare two schema versions"""
    old_fields = set(extract_fields(old_file))
    new_fields = set(extract_fields(new_file))
    
    removed = old_fields - new_fields
    added = new_fields - old_fields
    
    if removed:
        print(f"⚠️  BREAKING: Removed fields: {removed}")
    if added:
        print(f"✅ Added fields: {added}")
    
    return bool(removed)  # True if breaking change

if __name__ == "__main__":
    has_breaking = compare_schemas("models/v1/user.py", "models/v2/user.py")
    sys.exit(1 if has_breaking else 0)
