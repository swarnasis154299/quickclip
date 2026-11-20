"""quickclip: cut one long video into many frame-accurate clips from a list of timestamps.

    python quickclip.py video.mp4 "0:30-1:00, 1:30-2:05, 1:02:10-1:03:00"
    python quickclip.py video.mp4 --file timestamps.txt --out cuts --vertical
    python quickclip.py            # interactive mode
"""
import argparse
import os
import subprocess
import sys

try:
    import static_ffmpeg
    static_ffmpeg.add_paths()  # downloads ffmpeg on first run if it isn't installed
except ImportError:
    pass


def time_to_seconds(t: str) -> float:
    parts = t.strip().split(":")
    try:
        if len(parts) == 1:
            return float(parts[0])
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except ValueError:
        pass
    raise ValueError(f"bad timestamp: {t!r}")


def parse_timestamps(text: str):
    segments = []
    for part in text.replace("\n", ",").split(","):
        part = part.strip()
        if not part or part.startswith("#"):
            continue
        if "-" not in part:
            print(f"skipping {part!r}: expected start-end")
            continue
        start_s, end_s = (x.strip() for x in part.split("-", 1))
        start, end = time_to_seconds(start_s), time_to_seconds(end_s)
        if end <= start:
            print(f"skipping {part!r}: end is before start")
            continue
        segments.append((start, end))
    return segments


def cut(video, segments, out_dir="cuts", vertical=False, crf=18):
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(video))[0]
    ok = 0
    for i, (start, end) in enumerate(segments, 1):
        out = os.path.join(out_dir, f"{base}_cut_{i:02d}.mp4")
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(start), "-to", str(end), "-i", video]
        if vertical:
            # centre-crop to 9:16 and scale to 1080x1920 for Shorts / Reels / TikTok
            cmd += ["-vf", "crop='min(iw,ih*9/16)':ih,scale=1080:1920"]
        cmd += ["-c:v", "libx264", "-crf", str(crf), "-preset", "fast",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-y", out]
        print(f"[{i}/{len(segments)}] {start:.2f}s -> {end:.2f}s")
        r = subprocess.run(cmd, stderr=subprocess.PIPE)
        if r.returncode == 0:
            ok += 1
            print(f"    saved {out}")
        else:
            print(f"    failed: {r.stderr.decode(errors='ignore').strip()}")
    print(f"done: {ok}/{len(segments)} clips in {out_dir}/")
    return ok


def main():
    p = argparse.ArgumentParser(description="Cut a video into clips from timestamps.")
    p.add_argument("video", nargs="?", help="input video file")
    p.add_argument("timestamps", nargs="?", help='e.g. "0:30-1:00, 1:30-2:00"')
    p.add_argument("-f", "--file", help="text file with one start-end per line")
    p.add_argument("-o", "--out", default="cuts", help="output folder (default: cuts)")
    p.add_argument("--vertical", action="store_true", help="crop to 9:16 1080x1920")
    p.add_argument("--crf", type=int, default=18, help="quality, lower is better (default 18)")
    a = p.parse_args()

    video = a.video or input("Path to your video: ").strip().strip('"')
    if a.file:
        text = open(a.file, encoding="utf-8").read()
    else:
        text = a.timestamps or input("Timestamps (e.g. 0:30-1:00, 1:30-2:00): ")
    if not os.path.isfile(video):
        sys.exit(f"file not found: {video}")
    segments = parse_timestamps(text)
    if not segments:
        sys.exit("no valid segments found")
    cut(video, segments, a.out, a.vertical, a.crf)


if __name__ == "__main__":
    main()
