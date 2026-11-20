"""Voiceover -> word-level timestamps, locally, with faster-whisper.

Whisper runs on this machine: no API key, no cost, and the audio never leaves the
computer. The JSON it writes is what every beat boundary in the video is derived
from, which is why this runs before any visual is built.

    py scripts/transcribe.py assets/audio/vo.wav
    py scripts/transcribe.py assets/audio/vo.wav --model small.en --out assets/audio/words.json

Writes a JSON of words with start/end seconds and probability, prints the transcript,
and flags every word under 0.6 confidence (a likely name or mispronunciation: report
it, never silently fix it). Run with `py -I` if the input folder is untrusted.
"""
import argparse, json, os, subprocess, sys, tempfile

def to_wav16k(src):
    out = os.path.join(tempfile.gettempdir(), "vo-16k.wav")
    subprocess.run(["ffmpeg", "-y", "-i", src, "-ar", "16000", "-ac", "1", out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--model", default="base.en")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if not os.path.exists(a.audio):
        sys.exit(f"no audio at {a.audio}")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper not installed. Run: pip install faster-whisper")
    wav = to_wav16k(a.audio)
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(wav, word_timestamps=True, vad_filter=False)
    words, text, low = [], [], []
    for s in segments:
        text.append(s.text)
        for w in (s.words or []):
            rec = {"word": w.word.strip(), "start": round(w.start, 3),
                   "end": round(w.end, 3), "p": round(w.probability, 2)}
            words.append(rec)
            if w.probability < 0.6:
                low.append(rec)
    out = a.out or os.path.splitext(a.audio)[0] + ".words.json"
    json.dump({"duration": round(info.duration, 3), "model": a.model, "words": words},
              open(out, "w", encoding="utf8"), indent=2)
    print("".join(text).strip())
    print(f"\n{len(words)} words -> {out}")
    if low:
        print("\nLOW CONFIDENCE (<0.6), check these by ear, do not auto-fix:")
        for r in low:
            print(f"  {r['start']:6.2f}s  {r['word']!r}  p={r['p']}")

if __name__ == "__main__":
    main()
