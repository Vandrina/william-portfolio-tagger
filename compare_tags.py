#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parent

# Paths to compare
old_manifest_path = root / 'data' / 'manifest.json'  # Rename your baseline to this
new_manifest_path = root / 'manifest.json'  # Current manifest

def extract_tags(manifest_path):
    """Extract all unique disciplines, clients, keywords from a manifest"""
    with manifest_path.open('r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    disciplines = set()
    clients = set()
    keywords = set()
    
    for item in manifest:
        # Disciplines
        if 'discipline' in item:
            d = item['discipline']
            if isinstance(d, str):
                d = [d]
            if isinstance(d, list):
                disciplines.update(tag for tag in d if tag)
        
        # Clients
        if 'clients' in item and isinstance(item['clients'], list):
            clients.update(tag for tag in item['clients'] if tag)
        
        # Keywords
        if 'keywords' in item and isinstance(item['keywords'], list):
            keywords.update(tag for tag in item['keywords'] if tag)
    
    return disciplines, clients, keywords

# Check if old manifest exists
if not old_manifest_path.exists():
    print(f"ERROR: Baseline manifest not found at {old_manifest_path}")
    print("\nTo use this script:")
    print("1. Save your current manifest as 'data/manifest-before-william.json' (baseline)")
    print("2. After William tags, compare against 'data/manifest.json' (updated)")
    exit(1)

if not new_manifest_path.exists():
    print(f"ERROR: New manifest not found at {new_manifest_path}")
    exit(1)

# Extract tags from both
old_disciplines, old_clients, old_keywords = extract_tags(old_manifest_path)
new_disciplines, new_clients, new_keywords = extract_tags(new_manifest_path)

# Find what's new
added_disciplines = new_disciplines - old_disciplines
added_clients = new_clients - old_clients
added_keywords = new_keywords - old_keywords

# Output results
print("=" * 60)
print("NEW DISCIPLINES (add these to website filters)")
print("=" * 60)
if added_disciplines:
    for discipline in sorted(added_disciplines):
        print(f"  + {discipline}")
else:
    print("  (no new disciplines)")

print("\n" + "=" * 60)
print("NEW CLIENTS (add these to website filters)")
print("=" * 60)
if added_clients:
    for client in sorted(added_clients):
        print(f"  + {client}")
else:
    print("  (no new clients)")

print("\n" + "=" * 60)
print("NEW KEYWORDS (add these to website filters)")
print("=" * 60)
if added_keywords:
    for keyword in sorted(added_keywords):
        print(f"  + {keyword}")
else:
    print("  (no new keywords)")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"New disciplines: {len(added_disciplines)}")
print(f"New clients: {len(added_clients)}")
print(f"New keywords: {len(added_keywords)}")

# Save to file
output_file = root / 'new-tags.txt'
with output_file.open('w', encoding='utf-8') as f:
    f.write("NEW DISCIPLINES\n")
    f.write("=" * 60 + "\n")
    for discipline in sorted(added_disciplines):
        f.write(f"+ {discipline}\n")
    
    f.write("\nNEW CLIENTS\n")
    f.write("=" * 60 + "\n")
    for client in sorted(added_clients):
        f.write(f"+ {client}\n")
    
    f.write("\nNEW KEYWORDS\n")
    f.write("=" * 60 + "\n")
    for keyword in sorted(added_keywords):
        f.write(f"+ {keyword}\n")

print(f"\n✓ New tags saved to: {output_file}")
