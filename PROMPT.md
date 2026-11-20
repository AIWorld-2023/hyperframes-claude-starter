# The setup prompt

Paste everything below the line into the Claude Code panel once, at the start.

---

Set up a HyperFrames project in this folder, then stop and wait for me.

Read `CLAUDE.md` and `HOUSE-RULES.md` in this repo first. Those rules apply to everything you build here.

**1. Install the HyperFrames skills, then check the toolchain**

Run `npx hyperframes skills update`, then `npx hyperframes skills check`, then `npx hyperframes doctor` and tell me what is missing. (The skills send a usage beacon / telemetry — just so you know.)

The skills teach you the real HyperFrames APIs: composition, captions, overlays, motion, rendering. Without them you write HTML that only looks right.

**2. Scaffold a blank project**

Run `npx hyperframes init` with the flags for a blank project (no example, skip re-installing skills). Read `--help` for the exact flag names first. Keep the existing `README.md`, `CLAUDE.md`, `HOUSE-RULES.md`, `PROMPT.md`, `LICENSE` and `scripts/` — merge the scaffold around them, never overwrite them.

**3. Install the local toolchain this repo expects**

Check what's installed and install anything missing, showing me each command first: `git`, `node`, `npm`, `ffmpeg`, `ffprobe`, `py` + `pip`, `yt-dlp`, Google Chrome, and the Python packages `numpy`, `scipy`, `soundfile`, `pillow`, `faster-whisper`. On Windows use winget (`Gyan.FFmpeg`, `Python.Python.3.12`, `Google.Chrome`, `yt-dlp.yt-dlp`) and `pip`. Load faster-whisper `base.en` and `small.en` once so they download. Keep everything on a drive with room.

Whisper runs on this machine: no API key, no cost, nothing leaves the computer. `scripts/transcribe.py` turns a voiceover into word-level timestamps; check it runs once faster-whisper is installed.

**4. Confirm and stop**

Run `npx hyperframes lint` and `npx hyperframes check` on the blank project and confirm they pass. Tell me what you installed and whether I need to start a new Claude Code session. Don't build a composition yet.

> Alternative install to try (and mark VERIFY): in the prompt box, `/plugin marketplace add heygen-com/hyperframes`, then `/plugin install hyperframes@hyperframes`, then `/reload-plugins`.

---

## After setup: the prompt that builds the video

Record your voiceover, drop it in `assets/audio/`, transcribe it, then prompt in this order:
identity, audience, voice, structure with timings, technical constraints.

> This is for **[product]**, a **[one-line description of what it actually does]**.
>
> The audience is **[who they are and what they just did]**. The voice is **[three adjectives]**, never hype.
>
> Audio first: transcribe `assets/audio/<vo>.wav` with `scripts/transcribe.py` and tie every beat to a word time.
>
> Structure it into these beats: **[beat 1 — what's said, what's shown]**, **[beat 2]**, ...
>
> 1920x1080 (or 1080x1920), 30fps. Vary the easing by role, every entrance also exits, real logos only, captions as whole phrases, bed about 14 dB under the voice. Deliver H.264.

Then improve in passes, not regenerations: brand and content, then typography in motion, then real footage or screenshots composited over the layout. Then polish one element at a time: *"Nothing exits in scene two, add exit animations."* Run `npx hyperframes lint` and `check` after every pass, and make a still at each beat and actually look at it before you call anything done.
