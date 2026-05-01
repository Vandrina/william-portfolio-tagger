#!/usr/bin/env python3
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent
images_root = root / 'images'
thumbs_root = root / 'thumbnails'
placeholders_root = root / 'gallery-blur-placeholders'
manifest_path = root / 'data' / 'manifest.json'

# Load manifest
with manifest_path.open('r', encoding='utf-8') as f:
    manifest = json.load(f)

# Track renames for updating manifest
renames = {}

def rename_with_leading_zeros(directory, is_thumbnail=False):
    """Rename files that start with 1-2 digit numbers to have 3-digit numbers"""
    if not directory.exists():
        print(f"Skipping {directory} (doesn't exist)")
        return
    
    for file_path in sorted(directory.rglob('*')):
        if not file_path.is_file():
            continue
        if file_path.name == '.DS_Store':
            continue
        
        # Match filenames starting with 1-2 digits followed by a dot or space
        match = re.match(r'^(\d{1,2})(\.\s*.+)$', file_path.name)
        if not match:
            continue
        
        number = match.group(1)
        rest = match.group(2)
        
        # Already has 3 digits? Skip
        if len(number) >= 3:
            continue
        
        # Pad to 3 digits
        new_number = number.zfill(3)
        new_name = f"{new_number}{rest}"
        new_path = file_path.parent / new_name
        
        # Store the rename mapping (relative to root)
        old_rel = str(file_path.relative_to(root)).replace('\\', '/')
        new_rel = str(new_path.relative_to(root)).replace('\\', '/')
        
        print(f"Renaming: {old_rel} → {new_rel}")
        file_path.rename(new_path)
        renames[old_rel] = new_rel

print("=== Renaming Main Images ===")
rename_with_leading_zeros(images_root)

print("\n=== Renaming Thumbnails ===")
rename_with_leading_zeros(thumbs_root, is_thumbnail=True)

print("\n=== Renaming Placeholders ===")
rename_with_leading_zeros(placeholders_root)

# Update manifest
print("\n=== Updating Manifest ===")
changes = 0
for item in manifest:
    # Update file path
    if item.get('file') in renames:
        old_file = item['file']
        item['file'] = renames[old_file]
        print(f"Updated file: {old_file} → {item['file']}")
        changes += 1
    
    # Update thumbnail path
    if item.get('thumbnail') in renames:
        old_thumb = item['thumbnail']
        item['thumbnail'] = renames[old_thumb]
        print(f"Updated thumbnail: {old_thumb} → {item['thumbnail']}")
        changes += 1
    
    # Update placeholder path
    if item.get('placeholder') in renames:
        old_placeholder = item['placeholder']
        item['placeholder'] = renames[old_placeholder]
        print(f"Updated placeholder: {old_placeholder} → {item['placeholder']}")
        changes += 1

# Save updated manifest
with manifest_path.open('w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print(f"\n✓ Renamed {len(renames)} files")
print(f"✓ Updated {changes} paths in manifest")
print(f"✓ Manifest saved to {manifest_path}")
