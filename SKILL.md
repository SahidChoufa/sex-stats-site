---
name: "quran-story-tiktok"
description: "Make the channel's long-format YouTube education video (landscape 16:9): 2D cartoon cast in a 3D toon world with 3D graphs, voice, score and SFX in Remotion, plus its max-clickbait thumbnail and posting via the YouTube API."
---

# YouTube education video (2D cartoon cast in a 3D toon world, landscape)

The channel (YouTube: **More.of.religion**) now makes **one long-format education video** at a time (landscape). This replaces the old
Quran-story TikTok pipeline (its docs under `tiktok/` in the Project are archive only).
Look and pipeline: the open-source **Claude Animated Shorts** skill (https://github.com/mromidev/claude-animated-shorts, MIT):
flat bean-head cartoon cards with plum ink, a painted 3D town with black ink lines, saturated sky, lens blur, gliding
cameras, synthesized SFX and an original score, all rendered with three.js inside Remotion (no AI video generator).
First video: **"Why Money Videos Pay More"** (2026-11-05, 31.6 s test, 1920x1080, posted public: https://youtu.be/mgFvojKIGgo) — sources under `youtube/finads/` in the Project. A backup of this skill lives in the Project at `youtube/SKILL.md`.

## Channel rules
- Landscape **1920x1080**, 30 fps (2560x1440 with `--scale 1.3333` when rendering on a GPU machine or when there is time).
- English only, one steady narrator: Kokoro `am_michael`, speed ~1.24 (~3.3 words/s).
- Every figure in the script is looked up (figures change) and written with its link at the top of `SCRIPT.md`. Say "about" / ranges when sources give ranges.
- Graphs are part of the story: 3D bars, coin stacks, trend lines built in the world (so they get ink lines) plus short value stickers ("$15–50"). No burned-in narration captions.
- Mix: voice unchanged; music bed ~10 LU under the voice and ducked -3 dB on speech ("+3 dB music" standard); SFX stem -6 dB; master -14 LUFS, true peak <= -1.2 dBTP; audio exactly the picture length.
- Story, characters and voice are always our own; the repo's reference frames are for look study only, never published.
- Every video ships with a MAX-clickbait thumbnail (A + B variant) made with the recipe below.

## Bootstrap (fresh cloud workspace, ~3 min)
1. `git clone https://github.com/mromidev/claude-animated-shorts.git ~/claude-animated-shorts`
2. Make the Remotion project (e.g. `~/yt`), then `npm i remotion@4 @remotion/cli@4 @remotion/three@4 @remotion/bundler@4 @remotion/renderer@4 react@18 react-dom@18 three@0.169 @react-three/fiber@8 @react-three/postprocessing@2 postprocessing@6 @types/three@0.169 typescript @types/react@18`
3. Restore the last video's sources from the Project with `project_read` (`youtube/<last>/...`: `package.json`, `tsconfig.json`, `src/index.ts`, `src/Root.tsx`, `src/videos/<name>/*.ts(x)` incl. `Thumb.tsx`, `scripts/stills.mjs`, `scripts/render.mjs`, `scripts/render_chunks.sh`, `scripts/thumb.mjs`, `voice/voice.py`, `audio/soundtrack.py`, `youtube_meta.json`, and `youtube/tools/upload_youtube.py`) and write each file with Write, exactly as read. Copy the unchanged look modules from the repo: `templates/bridge/{grade,shade,lights,cardshade,paint}.ts`, and `templates/audio/{dsp,instruments,sfx_gen}.py` into `audio/`.
4. `pip install --break-system-packages kokoro-onnx soundfile numpy scipy google-api-python-client google-auth-oauthlib`; voice model (GitHub releases):
   `curl -sSL -o ~/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx` and `.../voices-v1.0.bin` -> `~/voices.bin`.
5. Fonts: `npm pack @fontsource/lilita-one @fontsource/fredoka`, copy `lilita-one-latin-400-normal.woff2`, `fredoka-latin-600/700-normal.woff2` to `public/fonts/` (loaded with `FontFace` before any canvas text, behind `delayRender`).
6. Browser: cloud workspace = `/usr/bin/google-chrome`, `chromiumOptions: { gl: "swangle" }` (software WebGL; no GPU). On the person's gaming laptop with a real GPU use Remotion's default GL (`angle` on Windows), concurrency 2-4, MSAA 4, and render 2560x1440.

## Project layout
`src/videos/<name>/`
- From the repo, unchanged: `grade.ts shade.ts lights.ts cardshade.ts paint.ts`.
- From the repo, landscape-patched: `ink.ts` (pxScale = min(w, h) / 1080), `lensblur.ts` (s = min(res) / 1080).
- `toon.ts` = repo + our props: `controller`, `coin`, `phone`, `card`, `["paddle", icon, k]`, `["point", k]`, `tie` on Outfit, icons `bank chart card umbrella controller coin eye`, `fxCoin`, `fxSparkle`, thumbnail expressions `money` and `cry`.
- `build.ts` = trimmed repo build (Batch, lam, quad/tri/box, painted gabled `house()`, sight-line culling).
- Our own per video: `story.ts` (word times `W`, `at()`, sets, shots, crossfades, cameras, kicks, lens blur), `cast.ts` (pool / actor / fx machinery + people, labels, effects), `world.ts` (sky, ground, town, one set per beat, animated graph pieces, `Zoned` batch), `<Name>.tsx` (composer), `Thumb.tsx` (thumbnail, 2D canvas only), all registered in `src/Root.tsx`.

## Pipeline per video
1. **Topic + facts**: one question with a surprising, sourced answer and a simple everyday analogy. WebSearch current numbers first.
2. **Script** (target length x 3.3 words): hook paradox in sentence 1 → numbers beat (graphs) → "You see," mechanism → consequence → ironic payoff that calls back the hook. Never describe what the viewer already sees. Pick the thumbnail's contrast pair now (a real small-vs-big number pair from the script).
3. **Voice**: `python3 voice/voice.py` (script lines in `SCRIPT`, phrases split on `|`) → `voice.wav`, `words.json` (word times estimated by character share inside each phrase), `segs.json`. Adjust SPEED until the length is right.
4. **Shots** (`story.ts`): copy word onsets into `W`; visual reactions at `at(word)` = 2 frames early. One set per beat at x = 0, 80, 160, ...; crossfades 6-10 f on place changes; white flash after the hook; every hold creeps (pushK); glides 20-40 f; flip kicks on impacts.
5. **World**: static pieces go into the `Zoned` batch (one merged mesh per material per set) — a single merged town makes every frame draw everything in the main, ink and shadow passes (about 3x slower). Signs and labels: unlit `facePlane` on the NOINK layer in front of an inked board.
6. **Cast**: front-view cards; contact blob + day tail shadow; expression swaps on their word with a blink. Paddle boards radius ~44u or they vanish in wides.
7. **Look checks**: `PROPS='{"post":{"msaa":0}}' node scripts/stills.mjs <Comp> out/<dir>/x_ <f1,f2,...> 0.5` (~50 s per still), paste them into a contact sheet with PIL and view it. Check: nobody cut by the frame edge, signs not hidden by geometry, labels not colliding, graphs readable, golden sun lighting faces (use sunAz ~125 = behind-right; az < 90 leaves camera-facing facades in shadow).
8. **Sound**: `python3 audio/soundtrack.py` mirrors the word times (keep it in sync with story.ts): score (pizz bass, brushes, music box, glock, vibes, pad, timpani/cymbal accents, stop-time before the punch line, final chord on the last word), SFX (pops, zips, chimes, coin clinks, whooshes on dissolves, from `sfx_gen.py` + own), breeze + birds. Writes `out/mix.wav`, stems, `cues.md`.
9. **Render** in the background (run_in_background, timeout 7200000) in resumable chunks, ONE browser tab:
   `scripts/render_chunks.sh <Comp> <total frames> 120 out/final` (concurrency 1, MSAA off, skips chunks already on disk, joins them into `out/final/video.mp4` with ffmpeg concat; the concat list holds bare file names written inside the output folder). Cloud CPU speed: ~4.5 s per frame on simple shots, ~10 s on lens-blur shots: a 30 s video takes ~2.5 h at 1080p. Two tabs on 2 CPUs were ~3x slower and the container ran out of headroom and restarted; after a restart or a 2 h timeout just run the same command again. MSAA off looks the same (the ink pass anti-aliases the lines). Watch it with Monitor on `chunks.log`.
   Mux: `ffmpeg -i video.mp4 -i audio/out/mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart final.mp4`.
10. **QA**: grab a frame per shot + the crossfades, ffprobe duration, `ffmpeg -af ebur128` loudness; fix and re-render only the affected frame range.
11. **Thumbnail**: MAX clickbait recipe below. Render MAX + MAXB, check at feed size, export JPG.
12. **Deliver**: SendUserFile the mp4 and thumbnails (status proactive when unattended), plus a YouTube title, description with the sources, and tags in a SendUserMessage; write them to `youtube_meta.json`. Save `SCRIPT.md` and every changed source to the Project under `youtube/<name>/` and add a row to `youtube/video-log.md`.
13. **Post** only when the person asks for that video to be posted (see Posting).

## Thumbnail — MAX clickbait (default)
Made in `Thumb.tsx` (composition `<Name>Thumb`, 1280x720, 2D canvas at 2x, no WebGL): `node scripts/thumb.mjs <Comp> out/thumb/final_ MAX,MAXB` (~15 s each) → PNG → PIL JPG quality 92 (~240 KB; limit 2 MB). `paintMax()` is the template: per video swap the numbers, the two characters, their props and the kind of money. The older calm layout (`A`/`B`: "$4 VS $50" side by side on the golden frame) stays in the file as a fallback.
Building blocks: `charCanvas` (toon `bodyFront` at any scale; head centre = design y ~337, soles 975), `rimCutout` / `cutout` (white rim + cyan rim-light / dark shadow), `bigNumber`, `scribbleCircle`, `curvedArrow`, `banknote`, `cashBrick`, `coinStack`, `tag`, `headline`, `sunburst`, `glow`. Thumbnail faces in `toon.ts`: `money` (green $ eyes in big white eyes set 3u low so the hair fringe does not cut them, brows up, open laugh) and `cry` (squeezed eyes, sad brows, wailing O, blue tear streams).
The formula — ONE giant face + ONE giant number + ONE loser in a red ring + ONE arrow, money everywhere:
1. **Hero face 40-50% of the frame height**: k ≈ 1.42 x 720 / 1000, head centre ~47% down at ~65% across, body cropped by the bottom edge, looking at the viewer, `money` expression. White rim ~10 px + cyan rim-light glow so it pops off the sky. Nothing ever covers the face.
2. **One giant 3D number** = the hook, top-left, the biggest thing after the face: `bigNumber` (Lilita One ~250 px, yellow → gold gradient, orange-brown extrude, ink stroke 15% of the size, gloss on the top half, tilted ~-5°, TIGHT white outer glow: blur ≈ 0.11 x size — larger turns into a white cloud). Whole thumbnail ≤ ~12 characters of text; numbers beat words.
3. **The loser, bottom-left**: small (k ≈ 0.56), `cry` face, his small number on a red tag **crossed out** (white strike with an ink outline), all inside a hand-drawn **red scribble ring** that overshoots its start.
4. **One fat curved yellow arrow** from the red ring up to the big number: the "how do you go from $4 to $50?" curiosity gap.
5. **Money everywhere, never a single bill**: banknote rain behind the hero (kept off the face and the number), 2 blurred banknotes in the foreground for depth, a giant coin tower on the right edge, a pyramid of cash bricks bottom-right (decoration only: the duration stamp covers it).
6. **Colour**: saturated blue sky wash (radial light blue → #1e8ce1 → navy edges) over the blurred day frame of the video (blur 9 px, saturate 1.6), light-blue sunburst + gold halo behind the head: blue vs yellow/gold = complementary max contrast. Red only for the negative (ring, crossed-out tag).
7. **Safe areas**: nothing important in the bottom-right ~15% (duration stamp) or on the far edges (mobile crops).
8. **Feed-size check**: contact sheet with the full image + 320x180 + 168x94 downscales; the number, the face's emotion and the red ring must read at 168 px wide.
9. **Clickbait, never lies**: exaggerate emotion, scale, colour and contrast — never the facts. Every number on the thumbnail is a real figure from the video and its sources (here the ends of the CPM ranges, $4 and $50). A misleading promise gets clicks then fast drop-off, and YouTube's Test & Compare picks the winner by watch-time share.
10. **A/B**: B = A + ONE change (e.g. a yellow "SAME VIEWS?!" line under the number). Put both in YouTube Studio's Test & Compare (desktop, up to 3) and swap a clear loser within the first hours.

## Posting (YouTube Data API v3)
Only when the person asks for that video to be posted. Defaults: public, category 27 (Education), `madeForKids` false, `defaultLanguage`/`defaultAudioLanguage` en, notify subscribers; thumbnail A.
- Script: `youtube/tools/upload_youtube.py` (Project) with the video's `youtube_meta.json` (title <= 100 chars, description with sources, tags).
- Credentials: the person's OAuth "Desktop app" client of Google Cloud project `youtube-automation` (`client_secret.json`). Ask the person for it when it is not in the workspace. It and `token.json` (which can upload to the channel) stay in the workspace with mode 600 — never in the Project, a file sent to the person, or a published page.
- **On the person's laptop**: `python3 upload_youtube.py --video final.mp4 --thumb thumb_A.jpg --meta youtube_meta.json` (opens Google sign-in in the browser by itself).
- **In the cloud workspace**: Claude's allowed network domains must include `oauth2.googleapis.com` and `www.googleapis.com` (uploads also go to `youtube.googleapis.com`); with the default allowlist curl returns 000 and the proxy status shows a 403 CONNECT. Test with `curl -s -o /dev/null -w '%{http_code}' https://oauth2.googleapis.com/token` (404 = reachable). Two-step sign-in in chat: `python3 upload_youtube.py --auth-url` → send the link → the person signs in with the channel's Google account and allows → they paste the `http://localhost/?...code=...` address (the page itself does not load; the code lasts ~10 min) → `--auth-response '<address>' --auth-only` (prints the channel name; check it is the right one) → upload.
- Google side: YouTube Data API v3 enabled; while the OAuth app is in Testing, the channel's Gmail must be a Test user and the refresh token dies after 7 days (just sign in again); the "Google hasn't verified this app" screen → Advanced → continue. Upload quota: 100 `videos.insert` per day.
- **Custom thumbnails need a phone-verified channel** (youtube.com/verify, SMS code — only the person can do it); otherwise `thumbnails.set` returns 403 "doesn't have permissions to upload and set custom video thumbnails". Then ask them to verify and run a background loop (run_in_background) that retries `python3 upload_youtube.py --video-id <id> --thumb <thumb_A.jpg>` every 2 min for 2 h, so the thumbnail lands the moment they verify.
- After posting: report the youtu.be link, privacy and status from the script, and add the link to `youtube/video-log.md`.

## Gotchas met so far
- `EffectComposer` children: build the pass list as an array (conditional `null` children fail type-checking).
- Unmounting a crossfade layer: guard `fx.ink.dispose?.()` in try/catch (the composer may already have released it) and key layers by shot id.
- Stills reload the page and repaint every texture: ask for all frames in one call.
- Coin stacks: cylinders with ~±2 cm jitter read as stacked coins; more jitter turns tall towers into noisy dashes.
- Seesaw / plank tilt: +rotation.z lifts the +x end.
- A portico in front of a facade hides a sign on that facade: put the sign on the portico.
- Sparkles / labels centred on a character's head cover the face: place them above or beside.