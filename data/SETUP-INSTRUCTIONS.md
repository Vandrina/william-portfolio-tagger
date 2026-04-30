# Portfolio Image Tagger - Setup Instructions

## What This Does
William can tag all 388 images through a web interface. Every change auto-saves to GitHub (with version history). No files to download or upload.

## One-Time Setup (5 minutes)

### 1. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `william-portfolio-tagger` (or whatever you want)
3. Make it **Private** (so the manifest isn't public)
4. Create repository

### 2. Upload Files
1. In your new repo, click "Add file" → "Upload files"
2. Upload:
   - `image-tagger-github.html` (the file I just created)
   - `manifest.json` (from your sandbox)
3. Commit the files

### 3. Enable GitHub Pages
1. In your repo, go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` → `/ (root)` → Save
4. Wait 1-2 minutes for deployment
5. You'll get a URL like: `https://yourusername.github.io/william-portfolio-tagger/`

### 4. Create Access Token (for auto-save)
1. Go to https://github.com/settings/tokens?type=beta
2. Click "Generate new token" (fine-grained)
3. Token name: "Portfolio Tagger"
4. Expiration: 30 days (or however long William needs)
5. Repository access: "Only select repositories" → choose `william-portfolio-tagger`
6. Permissions:
   - Repository permissions → Contents: **Read and write**
7. Generate token
8. **COPY THE TOKEN** - you can't see it again!

## Give to William

Send him:
1. **The GitHub Pages URL**: `https://yourusername.github.io/william-portfolio-tagger/image-tagger-github.html`
2. **These credentials** (he'll enter them once):
   - Repository Owner: `yourusername`
   - Repository Name: `william-portfolio-tagger`
   - Branch: `main`
   - Personal Access Token: `ghp_xxxxxxxxxxxxx` (the token from step 4)

## How William Uses It

1. Opens the URL in his browser
2. Enters the credentials (they save to his browser, only needs to do this once)
3. Clicks "Connect & Load Manifest"
4. Tags images:
   - Checkboxes for disciplines/clients
   - "Other" field to add new options
   - Keywords in comma-separated field
5. **Auto-saves every 30 seconds** to GitHub
6. Can filter by discipline to work in chunks
7. Green border shows completed images
8. Progress bar shows overall completion

## Features

- ✅ Auto-saves to GitHub every 30 seconds
- ✅ Full version history (every save is a commit)
- ✅ Shows image thumbnails
- ✅ Dynamic checkboxes (add new disciplines/clients on the fly)
- ✅ Progress tracking
- ✅ Filter by discipline
- ✅ Download backup anytime
- ✅ View commit history

## When He's Done

The updated `manifest.json` is already in your GitHub repo. You can:
1. Download it from the repo
2. Copy it back to your sandbox
3. Revoke the access token if you want

## Troubleshooting

**Images don't show:**
- The images need to be in the same GitHub repo
- Upload the `images/` and `thumbnails/` folders to the repo
- OR just ignore - the tagger works fine without thumbnails, William can still tag by filename

**Auto-save fails:**
- Check the token has "Contents: Read and write" permission
- Make sure the token hasn't expired
- Check browser console for errors

**Lost connection:**
- Everything saves to GitHub
- Just reload the page and enter credentials again
- All progress is preserved

## Security Note

The access token is stored in William's browser (localStorage) and is only sent to GitHub's API. It's not sent anywhere else. When you're done, you can revoke the token at https://github.com/settings/tokens
