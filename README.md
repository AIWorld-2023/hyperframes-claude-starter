# HyperFrames + Claude Code starter

Everything you need to make client-ready video by prompting, from a machine with nothing
installed on it. HyperFrames (by HeyGen) writes your video as HTML and renders it to a real MP4,
and Claude Code drives the whole thing.

This is the starter repo from the video. Clone it, open it in VS Code, paste one prompt, and
Claude scaffolds the rest, with the rules that separate a finished video from generated slop
already in place.

The Remotion sibling of this kit is at **github.com/AIWorld-2023/remotion-claude-starter**.

---

## Prerequisites

Three installs, none of them optional. Skip to **Quickstart** if you already have them.

### 1. Node.js
HyperFrames runs on Node. Go to **nodejs.org**, download the **LTS** build, run it with the
defaults. Prove it worked in a terminal:

```bash
node -v
npm -v
```

> If either says "command not found", close the terminal and open a fresh one. The installer
> updates your PATH, but a window that was already open never gets the memo.

### 2. VS Code
Download from **code.visualstudio.com**, install, open.

### 3. The Claude Code extension
In VS Code, open extensions with **Ctrl+Shift+X** (**Cmd+Shift+X** on Mac), search **Claude
Code** by Anthropic, install it, open the panel and sign in. **No API key** — any paid Claude
plan covers it.

---

## Quickstart

```bash
git clone <this-repo> my-hyperframes-video
cd my-hyperframes-video
code .
```

In the Claude Code panel, paste the contents of [`PROMPT.md`](PROMPT.md). Claude installs the
HyperFrames skills, checks the toolchain, scaffolds a blank HyperFrames project, sets up local
Whisper, and stops so you can start prompting.

---

## What's in here

| File | What it does |
|---|---|
| [`PROMPT.md`](PROMPT.md) | The setup prompt. Paste it into Claude Code once, at the start. |
| [`CLAUDE.md`](CLAUDE.md) | The project rules. Claude reads it automatically on every request. |
| [`HOUSE-RULES.md`](HOUSE-RULES.md) | The quality bar, the eyes-and-ears checks, the rendering rules. CLAUDE.md points here. |
| [`scripts/transcribe.py`](scripts/transcribe.py) | Turns a voiceover into word-level timestamps with faster-whisper, locally. |
| [`scripts/make_audio.py`](scripts/make_audio.py) | Synthesizes a free music bed and a set of quiet sound effects (no downloads). |

`HOUSE-RULES.md` is the part that actually matters. It's why the video comes out with varied
easing, entrances that also exit, real logos and a proper mix, instead of the stiff, silent-bed
version the same model gives you without it.

---

## The workflow, in four rules

1. **Audio first, then visuals** — the voiceover is the spine; every cut hangs off its word timestamps.
2. **One folder per video, split by type** — so Claude can write its own asset paths.
3. **Plan mode before anything structural** — approve the approach before a file is written.
4. **Repolish one element at a time** — name one element and one property, never re-describe the video.

> Redescribing the whole video is prompting a video model.
> Naming one element and one property is directing a codebase.

The full versions, with the reasoning behind each, are in [`HOUSE-RULES.md`](HOUSE-RULES.md).

---

## Two things that will spook you

**The preview degrades as the video gets longer.** Scenes snap, animations don't land. That's the
preview drawing frames live, not a bug. Render to judge motion.

**HEVC sneaks in.** If a render comes back as HEVC/H.265, some players and editors won't open it.
Ask for H.264 for anything you'll hand off.

---

## Rendering

```bash
npx hyperframes render                      # render the composition
npx hyperframes render --quality draft      # fast preview while iterating
```

Version every output `-v1`, `-v2`; never overwrite a previous cut. Run long renders detached with
a log, and keep scratch space on a drive with room — a full disk fails a long render at the final
step, after every frame is already done.
