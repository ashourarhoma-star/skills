#!/usr/bin/env bash
# Builds the 15 s accrual-basis video (vertical 9:16).
#   VOICE_MODEL=/path/ar_JO-kareem-medium.onnx ./build.sh [workdir]
# Requires: node + playwright (chromium), python3 (numpy, scipy, piper-tts), ffmpeg.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${1:-$HERE/.work}"
VOICE_MODEL="${VOICE_MODEL:?set VOICE_MODEL to the piper ar_JO-kareem-medium.onnx path}"
OUT="$HERE/out"
mkdir -p "$WORK/vo" "$OUT"

# ---------- 1. Voice-over (Arabic male, offline piper TTS) ----------
# Segment start times (s) aligned to scenes; tempo 1.17 fits the narration into 15 s.
STARTS=(0.25 4.35 9.65 12.15)
TRIM="silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse"
VOFX="atempo=1.17,highpass=f=75,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=4:release=90:makeup=2,aresample=48000"
inputs=() ; filters="" ; labels=""
for i in 1 2 3 4; do
  python3 -m piper -m "$VOICE_MODEL" -f "$WORK/vo/raw$i.wav" --length-scale 0.7 < "$HERE/voice/s$i.txt" 2>/dev/null
  ffmpeg -v error -y -i "$WORK/vo/raw$i.wav" -af "$TRIM,$VOFX" "$WORK/vo/s$i.wav"
  ms=$(python3 -c "print(int(${STARTS[$((i-1))]}*1000))")
  inputs+=(-i "$WORK/vo/s$i.wav")
  filters+="[$((i-1)):a]adelay=${ms}|${ms},pan=stereo|c0=c0|c1=c0[v$i];"
  labels+="[v$i]"
done
ffmpeg -v error -y "${inputs[@]}" -filter_complex "${filters}${labels}amix=inputs=4:normalize=0,apad=whole_dur=15,atrim=0:15,aecho=0.8:0.5:35|60:0.12|0.07[vo]" -map "[vo]" -ar 48000 "$WORK/voice.wav"

# ---------- 2. Music + SFX ----------
python3 "$HERE/audio.py" "$WORK/music_sfx.wav"

# ---------- 3. Mix: duck music under voice, loudness -14 LUFS / -1 dBTP ----------
ffmpeg -v error -y -i "$WORK/music_sfx.wav" -i "$WORK/voice.wav" -filter_complex \
  "[1:a]asplit=2[vsc][vmix];[0:a]volume=0.25[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=300[duck];[duck][vmix]amix=inputs=2:normalize=0:weights=1 2,loudnorm=I=-14:TP=-1.0:LRA=9" \
  -ar 48000 -ac 2 "$WORK/mix.wav"

# ---------- 4. Frames (2160x3840) ----------
WORKERS="${WORKERS:-3}"
if [ ! -f "$WORK/frames/f0449.jpg" ]; then
  for w in $(seq 0 $((WORKERS - 1))); do
    node "$HERE/render.mjs" frames "$WORK/frames" 30 2 "$w" "$WORKERS" &
  done
  wait
fi

# ---------- 5. Encode ----------
ffmpeg -v error -y -framerate 30 -i "$WORK/frames/f%04d.jpg" -i "$WORK/mix.wav" \
  -c:v libx264 -preset slow -crf 22 -profile:v high -level 5.1 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT/accrual-basis-4k.mp4"
ffmpeg -v error -y -i "$OUT/accrual-basis-4k.mp4" -vf "scale=1080:1920:flags=lanczos" \
  -c:v libx264 -preset slow -crf 19 -profile:v high -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT/accrual-basis-1080p.mp4"
ffmpeg -v error -y -ss 3.2 -i "$OUT/accrual-basis-1080p.mp4" -frames:v 1 "$OUT/cover.jpg"
echo "done -> $OUT"
