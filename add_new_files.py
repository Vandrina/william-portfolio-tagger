#!/usr/bin/env python3
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print('Pillow is required to run this script. Install it with: pip install Pillow')
    raise

root = Path(__file__).resolve().parent
images_root = root / 'images'
thumbs_root = root / 'thumbnails'
placeholders_root = root / 'gallery-blur-placeholders'
manifest_path = root / 'manifest.json'

image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
video_extensions = {'.mov', '.mp4', '.avi', '.webm'}
all_extensions = image_extensions | video_extensions

print("=" * 60)
print("SAFE MANIFEST UPDATER - Preserves all existing data")
print("=" * 60)

# Load existing manifest
existing_manifest = {}
manifest_list = []

if manifest_path.exists():
    with manifest_path.open('r', encoding='utf-8') as f:
        manifest_list = json.load(f)
        existing_manifest = {item['file']: item for item in manifest_list}
    print(f"✓ Loaded {len(existing_manifest)} existing entries")
else:
    print("! No existing manifest found - will create new one")

print("\nScanning for new files...")
print("-" * 60)

added_count = 0
skipped_count = 0
error_count = 0

for file_path in sorted(images_root.rglob('*')):
    if not file_path.is_file():
        continue
    if file_path.suffix.lower() not in all_extensions:
        continue
    if file_path.name == '.DS_Store':
        continue

    relative_path = file_path.relative_to(root)
    key = str(relative_path).replace('\\', '/')
    
    # Check if already in manifest
    if key in existing_manifest:
        skipped_count += 1
        continue
    
    # NEW FILE - add it
    relative_subpath = file_path.relative_to(images_root)
    
    # Try to find thumbnail with matching extension first, then try .jpg, then .png
    possible_extensions = [file_path.suffix, '.jpg', '.png']
    thumb_path = None
    
    for ext in possible_extensions:
        thumb_filename = f"{relative_subpath.stem}_thumbnail{ext}"
        potential_thumb_path = thumbs_root / relative_subpath.parent / thumb_filename
        if potential_thumb_path.exists():
            thumb_path = potential_thumb_path
            break
    
    if not thumb_path:
        print(f"✗ SKIPPED (no thumbnail): {key}")
        error_count += 1
        continue

    # Get thumbnail dimensions
    try:
        with Image.open(thumb_path) as img:
            thumb_width, thumb_height = img.size
    except Exception as e:
        print(f"✗ ERROR reading thumbnail for {key}: {e}")
        error_count += 1
        continue

    # Get dimensions from original file
    is_video = file_path.suffix.lower() in video_extensions
    
    if is_video:
        # For videos, can't read with PIL - use None or estimate from thumbnail
        full_width = None
        full_height = None
        aspect_ratio = round(thumb_width / thumb_height, 4)
    else:
        # For images, get actual dimensions
        try:
            with Image.open(file_path) as img:
                full_width, full_height = img.size
            aspect_ratio = round(full_width / full_height, 4)
        except Exception as e:
            print(f"✗ ERROR reading image {key}: {e}")
            error_count += 1
            continue

    # Get folder name as default discipline
    folder_discipline = file_path.parent.name
    
    # Placeholder path (may or may not exist)
    placeholder_path = placeholders_root / file_path.relative_to(images_root)
    placeholder_rel = str(placeholder_path.relative_to(root)).replace('\\', '/') if placeholder_path.exists() else None
    
    # Create new entry
    new_entry = {
        'file': key,
        'thumbnail': str(thumb_path.relative_to(root)).replace('\\', '/'),
        'placeholder': placeholder_rel,
        'width': full_width,
        'height': full_height,
        'thumbWidth': thumb_width,
        'thumbHeight': thumb_height,
        'aspectRatio': aspect_ratio,
        'thumbAspectRatio': round(thumb_width / thumb_height, 4),
        'title': '',
        'discipline': [folder_discipline],  # Array format
        'clients': [],
        'keywords': [],
        'sort': 999,
    }
    
    if is_video:
        new_entry['isVideo'] = True
    
    manifest_list.append(new_entry)
    print(f"✓ ADDED: {key}")
    if is_video:
        print(f"  └─ Video (dimensions from thumbnail)")
    added_count += 1

# Save updated manifest
if added_count > 0:
    with manifest_path.open('w', encoding='utf-8') as f:
        json.dump(manifest_list, f, indent=2)
    print("-" * 60)
    print(f"✓ Manifest updated and saved")
else:
    print("-" * 60)
    print("! No changes - manifest not modified")

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Existing entries preserved: {len(existing_manifest)}")
print(f"New entries added: {added_count}")
print(f"Files skipped (already in manifest): {skipped_count}")
print(f"Errors/missing thumbnails: {error_count}")
print(f"Total entries in manifest: {len(manifest_list)}")
print("=" * 60)
