# CLAUDE.md

Guidance for Claude Code in this repository. **Read HOUSE-RULES.md before any video work** — it
holds the quality bar, the eyes-and-ears checks, and the rendering rules, and it applies to
everything you build here.

## What this project is

A HyperFrames project: video written as HTML and rendered to a real MP4 with headless Chrome.
Because it's code and not a text-to-video model, it can't hallucinate. The logo stays the logo,
the numbers stay the numbers, and changing one value re-renders everything else identically.

## The four rules (full versions in HOUSE-RULES.md)

1. **Audio first, then visuals.** The voiceover is the spine. Transcribe it with
   `scripts/transcribe.py` before building any visual, and derive every beat boundary from the
   word timestamps, never by ear. Every boundary lands on a sentence end.
2. **One folder per video, split by type** (`assets/{audio,video,images,logos,stock,sfx,reference,brief}`),
   so you can write your own asset paths.
3. **Plan mode before anything structural.** A whole composition or a restructure goes through a
   plan in PLAN.md first. Small property changes don't.
4. **Repolish one element at a time.** When I name one element and one property, change exactly
   that and nothing else. Redescribing the whole video is prompting a video model; naming one
   element and one value is directing a codebase.

## HyperFrames build notes

- Install the HyperFrames skills before writing composition code (`npx hyperframes skills update`),
  then run `npx hyperframes lint` and `npx hyperframes check` after every pass and fix what they
  report.
- One sub-composition per chapter; more than three timed elements in one file warns, so split it.
- Deliver H.264, not HEVC, unless asked.
- Captions enter as whole phrases, never word by word.
- Iterate with `render --quality draft`; deliver at full quality. Run long renders detached with a
  log; if Chrome fails, run `npx hyperframes doctor` and the browser ensure step.
- The skills send a usage beacon (telemetry). It does not block anything; just know it's there.

## Before claiming a video is finished

1. `npx hyperframes lint` and `npx hyperframes check` are clean.
2. Make a still at each beat's midpoint and **actually look at every one**. Clipped headings,
   illegible text and wrong crops are only visible in the image.
3. Check arithmetically that no shot outlasts its clip and the duration is exact (ffprobe).
4. Measure the mix (ebur128): about -15 LUFS, true peak about -2 dBTP, bed present every second.
5. State plainly what you verified and what you didn't.
