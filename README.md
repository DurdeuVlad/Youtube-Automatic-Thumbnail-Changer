# Automated Thumbnail Changer

#### Submission by Vlad-Ioan Durdeu

## Introduction

This was a quick but fun automation project I threw together to save time messing with YouTube thumbnails. The idea was simple: cycle through different thumbnails and titles on a video, check how each one performs, and let the data tell you what works best.

Built it using Python and the YouTube Data API. No fluff. Just scripts that connect, update, and rotate thumbnails and titles based on folders and config files you control.

## What It Does

You drop your thumbnail images in folders  
Point the script at a video  
It rotates thumbnails and optionally titles too  
Each one runs for a set duration  
At the end, it gives you a view count comparison to help you decide what actually performs

## File Structure

```
├── clients
│   ├── analytics.py
│   ├── yt_stats.py
│   ├── youtube_analytics.py
│   ├── youtube_client.py
│   └── youtube_title.py
├── creds
│   ├── api_key
│   └── client_secret.json
├── thumbnails
│   ├── folder_1
│   ├── folder_2
│   └── folder_3
├── config.ini
├── requirements.txt
└── run.py
```

## How to Use

### 1. Clone the repo

```bash
git clone https://github.com/yourname/automated-thumbnail-changer.git
cd automated-thumbnail-changer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure it

- Fill in `config.ini` with your API key and channel ID  
- Drop your `client_secret.json` in the `creds/` folder

### 4. Add thumbnails

Put your test images in the `thumbnails/` folders. You can create new folders or reuse the ones there.

### 5. Run the script

```bash
python run.py
```

It will ask what script to run and guide you through selecting thumbnails and titles to rotate.

## Script Options

- `rotate_thumbnails`: cycles through thumbnails only, tracks view count
- `rotate_thumbnails_titles`: rotates both thumbnails and video titles
- `rotate_titles`: just title testing, no image changes
