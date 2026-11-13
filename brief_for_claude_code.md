# Brief: YouTube automation, move everything to this gaming PC

Context for Claude Code on my gaming PC. Everything below was decided or changed on 2026-11-13.

## The channel
- YouTube channel "Finances by bazzfite" (formerly named More.of.religion), phone-verified, so custom thumbnails are allowed.
- Format: one ~12-minute personal-finance education video per day, English, landscape 1920x1080 (2560x1440 on this GPU), 30 fps.
- Look: 2D cartoon cast in a 3D toon world with 3D graphs, rendered with three.js inside Remotion
  (look based on github.com/mromidev/claude-animated-shorts, MIT). Original score + SFX, voice from Kokoro TTS.

## Change 1: new audience (people over 35)
- Every episode is now for people **over 35**: catching up late, family, mortgage, retirement, protecting what you built.
- Every current figure (rates, limits, prices, laws) is looked up on the day and cited with its link in SCRIPT.md.
  Our own arithmetic is labelled as an assumption.
- Every video says clearly it is "education, not financial advice".

## Change 2: new thumbnail rules
Follow github.com/charlie947/social-media-skills `skills/youtube-thumbnail/SKILL.md`, adapted to the cartoon cast:
- 1280x720. The hero's face fills 30-50% of the frame, clear emotion, looks at the viewer, never covered.
- Text = a hook phrase of 3-5 words (3 is best, never more than 6), big bold sans-serif with a thick outline,
  readable at 320 px wide. No small text.
- Two dominant colours: one primary + one high-contrast accent (yellow, red or cyan).
- ONE focal element besides the face (a big number, an arrow or a prop).
- Nothing in the bottom-right corner (YouTube's duration stamp). Same style on every video.
- No em dashes. Never promise what the video does not deliver.
- Also write `<job>/thumb_prompt.md`: the brief (composition, text, placement, palette hex codes, supporting element,
  tone) + a ready-to-paste Gemini prompt in that skill's format, in case I want a Gemini version.
- Check every thumbnail at full size and at ~320 px wide.
- Make an A and a B version (B = A + one change) for YouTube's Test & Compare.

## Change 3: more human voice
- The old narration sounded flat and robotic (one Kokoro call per phrase, fixed gaps).
- New `py/voice_ep.py`: voice **am_puck**, speed **1.02**, **one Kokoro call per beat** (intonation carries across
  sentences), exact word timings from **faster-whisper (base.en)** aligned back onto the script words.
  Needs `pip install kokoro-onnx soundfile numpy scipy faster-whisper num2words`, plus the Kokoro model files
  `kokoro-v1.0.onnx` and `voices-v1.0.bin` from github.com/thewh1teagle/kokoro-onnx releases (model-files-v1.0).
- Scripts must be written to be spoken: questions, short punchy sentences, "..." for dramatic pauses, "|" for a breath.
- Next step on this PC: test **Chatterbox TTS** (open source, runs on the GPU) for an even more human voice and
  compare it with am_puck on one beat.

## Change 4: no more Google Drive, everything runs on this PC
- Google refuses YouTube + Drive scopes in one sign-in, so the Drive hand-off is dropped.
- Google Cloud project: `youtube-automation-513723`, OAuth "Desktop app" client already created.
  The YouTube token only needs scopes `youtube.upload` + `youtube.readonly`. Sign-in works (channel "Finances by bazzfite").
  The token from yesterday lived in a cloud session that is gone: sign in again here with `client_secret.json`
  (`python upload_youtube.py ...` opens the Google sign-in in the browser). Keep `client_secret.json` and `token.json`
  private (never commit, never share). The OAuth app is in Testing mode, so the refresh token expires after 7 days.
- New setup:
  1. One working folder on this PC (e.g. `C:\yt`), connected to the Claude desktop app so the daily cloud task can reach it.
  2. Put the engine there (Remotion project: `src/ep/`, `src/look/`, `py/`, `scripts/`, `laptop/`, `examples/`).
     Files not in the backup: `src/look/{paint,lights,shade,grade,cardshade}.ts` from `templates/bridge/` and
     `py/{dsp,instruments,sfx_gen}.py` from `templates/audio/` of claude-animated-shorts; fonts from
     `npm pack @fontsource/lilita-one @fontsource/fredoka` (lilita-one-latin-400, fredoka-latin-600/700) into `public/fonts/`;
     then `npm install`.
  3. Adapt the laptop scripts (`laptop/daily.ps1`, `laptop/yt.mjs`, `py/drive.py`) to work from local folders instead of
     Drive: a job folder `jobs/<YYYY-MM-DD>_<slug>/` with `READY.txt` = render it, then upload, then write `status.json`.
  4. Render with Remotion's default GL on Windows (`angle`), concurrency 2-4, MSAA 4, 2560x1440.
  5. Test-render the episode already prepared: `2026-11-05_compound-interest`
     ("The Penny That Beats a Million Dollars (Compound Interest Explained)", 11.4 min). Redo its voice with am_puck first.
  6. Then I turn on "Require this computer" on the daily scheduled task and its prompt gets rewritten for this local
     hand-off (no Drive).

## Status
- Daily runs on 2026-11-12 and 2026-11-13 made no video (the task still looked for the token on Drive).
- Already posted: "Why Money Videos Pay More on YouTube" (31.6 s test), https://youtu.be/mgFvojKIGgo
- Next topic in the queue: "Starting to invest at 35, 40 or 45: is it too late?"

## Rules that do not change
- Never post anything that is not sourced. Clickbait in emotion and colour, never in facts.
- Upload defaults: public, category 27 (Education), madeForKids false, language en, thumbnail A.
- Mix: voice untouched, music ~10 LU under the voice and ducked on speech, master -14 LUFS, true peak <= -1.2 dBTP.
