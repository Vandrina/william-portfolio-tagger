#!/usr/bin/env python3
import json
from pathlib import Path
from collections import defaultdict

root = Path(__file__).resolve().parent
manifest_path = root / 'manifest.json'

# Load manifest
with manifest_path.open('r', encoding='utf-8') as f:
    manifest = json.load(f)

# Collect all unique values
all_disciplines = set()
all_clients = set()
all_keywords = set()

# Also track which images use which tags (for verification if needed)
discipline_usage = defaultdict(int)
client_usage = defaultdict(int)
keyword_usage = defaultdict(int)

for item in manifest:
    # Disciplines
    if 'discipline' in item:
        disciplines = item['discipline']
        if isinstance(disciplines, str):
            disciplines = [disciplines]
        if isinstance(disciplines, list):
            for d in disciplines:
                if d:  # Skip empty strings
                    all_disciplines.add(d)
                    discipline_usage[d] += 1
    
    # Clients
    if 'clients' in item and isinstance(item['clients'], list):
        for c in item['clients']:
            if c:  # Skip empty strings
                all_clients.add(c)
                client_usage[c] += 1
    
    # Keywords
    if 'keywords' in item and isinstance(item['keywords'], list):
        for k in item['keywords']:
            if k:  # Skip empty strings
                all_keywords.add(k)
                keyword_usage[k] += 1

# Output results
print("=" * 60)
print("DISCIPLINES")
print("=" * 60)
for discipline in sorted(all_disciplines):
    count = discipline_usage[discipline]
    print(f"  {discipline:<30} ({count} images)")

print("\n" + "=" * 60)
print("CLIENTS")
print("=" * 60)
for client in sorted(all_clients):
    count = client_usage[client]
    print(f"  {client:<30} ({count} images)")

print("\n" + "=" * 60)
print("KEYWORDS")
print("=" * 60)
for keyword in sorted(all_keywords):
    count = keyword_usage[keyword]
    print(f"  {keyword:<30} ({count} images)")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total unique disciplines: {len(all_disciplines)}")
print(f"Total unique clients: {len(all_clients)}")
print(f"Total unique keywords: {len(all_keywords)}")

# Optional: Save to a file for easy reference
output_file = root / 'tags-summary.txt'
with output_file.open('w', encoding='utf-8') as f:
    f.write("DISCIPLINES\n")
    f.write("=" * 60 + "\n")
    for discipline in sorted(all_disciplines):
        count = discipline_usage[discipline]
        f.write(f"{discipline:<30} ({count} images)\n")
    
    f.write("\n" + "CLIENTS\n")
    f.write("=" * 60 + "\n")
    for client in sorted(all_clients):
        count = client_usage[client]
        f.write(f"{client:<30} ({count} images)\n")
    
    f.write("\n" + "KEYWORDS\n")
    f.write("=" * 60 + "\n")
    for keyword in sorted(all_keywords):
        count = keyword_usage[keyword]
        f.write(f"{keyword:<30} ({count} images)\n")

print(f"\n✓ Summary also saved to: {output_file}")
