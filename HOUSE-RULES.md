# House rules for every video in this project

Claude Code reads these on every request (CLAUDE.md points here). They are the difference
between a finished video and generated slop. HyperFrames writes video as HTML; these rules are
tool-agnostic and apply to every build in this repo.

## Working rules
- One folder per video. Inside assets/ split by type: video, audio, images, logos, stock, sfx, reference. Never write outside this project folder. Keep temp files and renders on a drive with room.
- Never edit or overwrite a source file. Every render gets a new version name (v1, v2, ...).
- Render only when the prompt tells you to. To check your work use stills, not a full render.
- One change per prompt, in absolute values (seconds, pixels, dB). When I name one element, change only that element and report which files you touched.
- A prompt that says it is my approval means: write the plan to PLAN.md, show it in your final report, and do not stop to ask. For anything else structural, show a plan with a beat table first and wait for my approval.
- Never invent product UI, numbers, quotes, logos or claims. Use only what I supplied or what was captured from the real source. Real logo files only, never redrawn.
- On-screen copy never overclaims. If the voice says completely free, the screen says Free.

## Your eyes (you render to a file, so look at it)
- Frames of any video: `ffmpeg -ss <t> -i <file> -frames:v 1 out.png`
- Contact sheet: `ffmpeg -i <file> -vf "fps=1,scale=240:-1,tile=6x5" -frames:v 1 sheet.png`
- Open every PNG and look at it, at full size and at phone size.
- For your own composition use the tool's still command: `npx hyperframes snapshot` (add `--at <t>` for a time, `--against <ref.mp4>` to place your frame next to a reference).

## Your ears (you cannot listen, so measure)
- Pauses: `ffmpeg -i <file> -af silencedetect=noise=-38dB:d=0.12 -f null -` (a phrase starts at each silence_end).
- Words and confidence: faster-whisper base.en with word_timestamps through `scripts/transcribe.py`. A word under probability 0.6 may be a mispronunciation or a name: report it, never fix it silently. Use silencedetect for phrase starts and whisper only for words inside a phrase.
- Loudness: `ffmpeg -af ebur128=peak=true` and `-af volumedetect`. Measure in 1 second windows to prove a music bed never drops out.

## Self-check after every pass
- Run `npx hyperframes lint` and `npx hyperframes check`. Fix what they report before you show me anything, and list what they caught.
- Vary the easing by role. Every entrance gets an exit. Never one ease for everything.

## Quality bar
1. One concept spine, not a slideshow: one visual idea carries the video and returns at the end. Say it in the plan before building.
2. Every spoken noun gets its graphic on its own word. Numbers are the stars: count them up in sync with the spoken number.
3. Real content only, read off the real source. Never invent counts.
4. Transitions: six or more different ones in anything over 30 s, each 0.4 s or longer with its own quiet sound. Hide every jump cut under a transition or a small punch-in.
5. Stock footage is welcome as a window or card background: no faces, no readable text, no real brands, one clip per slot, graded into the palette.
6. Sound: effect peaks 12 to 15 dB under the voice peaks, repeated effects quieter, bed about 14 dB under the voice. Final mix about -15 LUFS integrated, true peak about -2 dBTP.
7. Captions: whole phrases, 32 characters or fewer, one line, each phrase enters as one unit (never word by word), one payoff word in the accent colour, inside the safe band.
8. 9:16 safe area: nothing in the top 168 px, stage content in the 168 to 1250 band, nothing in the bottom. 16:9: keep everything inside a 5% title-safe margin. Graphics never cover a face or each other.
9. Process: plan, build, stills at every beat and every transition midpoint, read each still and fix, render only on signal, then verify the finished file (ffprobe, LUFS, true peak, bed present, real frames pulled from the MP4). Delete only files you made, by exact name.

## HyperFrames specifics
- Deliver H.264 (the universal codec), not HEVC/H.265, unless I ask otherwise.
- One sub-composition per chapter. More than three timed elements in a single file triggers a warning: split them.
- Captions enter as whole phrases (a caption block that reveals word by word is wrong here).
- Glass over bright areas washes out: put a dark scrim behind it, a dark glass base and a ~22 px blur. Full-screen linear gradients on a dark ground band; use a radial gradient, or a solid plus glow.
- Iterate with `render --quality draft`; deliver at full quality at the end. Run long renders detached with a log. If Chrome fails, run `npx hyperframes doctor` and the browser ensure step.
- The HyperFrames skills send a usage beacon (telemetry). Note it; it does not block anything.
