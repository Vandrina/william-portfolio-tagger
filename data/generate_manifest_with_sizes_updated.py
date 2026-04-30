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
manifest_path = root / 'data' / 'manifest.json'

image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

old_manifest = {}
if manifest_path.exists():
    try:
        with manifest_path.open('r', encoding='utf-8') as old_file:
            old_items = json.load(old_file)
            old_manifest = {item.get('file'): item for item in old_items if isinstance(item, dict) and item.get('file')}
    except Exception:
        print('Warning: could not read existing manifest metadata; rebuilding fresh.')

manifest = []

for image_path in sorted(images_root.rglob('*')):
    if not image_path.is_file():
        continue
    if image_path.suffix.lower() not in image_extensions:
        continue
    if image_path.name == '.DS_Store':
        continue

    relative_path = image_path.relative_to(root)
    
    # Construct thumbnail path with _thumbnail before extension
    relative_subpath = image_path.relative_to(images_root)
    thumb_filename = f"{relative_subpath.stem}_thumbnail{relative_subpath.suffix}"
    thumb_path = thumbs_root / relative_subpath.parent / thumb_filename

    if not thumb_path.exists():
        print(f'WARNING: thumbnail not found for {image_path} -> {thumb_path}')
        continue

    with Image.open(image_path) as img:
        full_width, full_height = img.size
    with Image.open(thumb_path) as img:
        thumb_width, thumb_height = img.size

    # Get folder name as default discipline
    folder_discipline = image_path.parent.name
    
    key = str(relative_path).replace('\\', '/')
    old_item = old_manifest.get(key, {})
    
    # Placeholder handling - preserve from old manifest if it existed
    placeholder_path = placeholders_root / image_path.relative_to(images_root)
    if placeholder_path.exists():
        placeholder_rel = str(placeholder_path.relative_to(root)).replace('\\', '/')
    else:
        # Keep old placeholder path even if file doesn't exist
        placeholder_rel = old_item.get('placeholder', None)
    
    # Preserve discipline if it exists, otherwise use folder name as array
    if 'discipline' in old_item:
        # Preserve existing discipline (might be array from William's tagging)
        discipline = old_item['discipline']
        # If it's a string (old format), convert to array
        if isinstance(discipline, str):
            discipline = [discipline]
    else:
        # New item - use folder name as single-item array
        discipline = [folder_discipline]
    
    manifest.append({
        'file': key,
        'thumbnail': str(thumb_path.relative_to(root)).replace('\\', '/'),
        'placeholder': placeholder_rel,
        'width': full_width,
        'height': full_height,
        'thumbWidth': thumb_width,
        'thumbHeight': thumb_height,
        'aspectRatio': round(full_width / full_height, 4),
        'thumbAspectRatio': round(thumb_width / thumb_height, 4),
        'title': old_item.get('title', ''),  # Preserve title from William's tagging
        'discipline': discipline,  # Now an array
        'clients': old_item.get('clients', []),
        'keywords': old_item.get('keywords', []),
        'sort': old_item.get('sort', 999),
    })

manifest_path.parent.mkdir(parents=True, exist_ok=True)
with manifest_path.open('w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print(f'Wrote {len(manifest)} items to {manifest_path}')
