<div align="center">

# âœ‚ï¸ quickclip

**Turn one long video into a stack of ready-to-post clips in a single command.**

Paste your timestamps â†’ get frame-accurate MP4s, optionally cropped to 9:16 for Shorts, Reels and TikTok.

</div>

```bash
python quickclip.py podcast.mp4 "0:30-1:00, 4:12-4:58, 1:02:10-1:03:00" --vertical
```

## Why

Clipping long-form content means cutting dozens of segments a day. Doing it in an editor is slow, and `ffmpeg -c copy` cuts land on keyframes, so clips start late or lose audio. quickclip re-encodes each segment (H.264 + AAC, CRF 18), so every cut is exact and every clip has sound.

## Features

- Timestamps as `ss`, `mm:ss` or `hh:mm:ss`, comma- or newline-separated
- `--vertical` centre-crops to 1080Ã—1920 for short-form platforms
- `--file` reads a timestamps list (lines starting with `#` are ignored)
- Installs ffmpeg for you on first run via `static-ffmpeg`
- Interactive mode if you run it with no arguments

## Install

```bash
git clone https://github.com/swarnasis154299/quickclip
cd quickclip
pip install -r requirements.txt
```

## Usage

```bash
python quickclip.py video.mp4 "0:30-1:00, 1:30-2:00"
python quickclip.py video.mp4 --file timestamps.example.txt --out clips --vertical
python quickclip.py video.mp4 "2:00-2:45" --crf 22      # smaller files
python quickclip.py                                     # asks for input
```

Clips are saved as `<video>_cut_01.mp4`, `<video>_cut_02.mp4`, â€¦ in `cuts/`.

## License

MIT. See [LICENSE](LICENSE).
