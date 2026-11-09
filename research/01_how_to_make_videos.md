# 01 — How to make 30–90s reels with Claude (code + generation APIs)

_Research date: 2026-11-09. Sources: 15 MoSidd transcripts (cleaned from `data/youtube_mo-sidd/*.en.vtt`, cited by video id), web research (URLs inline), the Treg catalog (checked live with `catalog_search` / `catalog_get` this session), and the 4 reference reels already analysed in `analysis/`._

**Short answer.** The pattern that gets MoSidd 150K–263K views is this: **write the voiceover first, give each line its own scene, generate a few still cut-outs per scene, and have Claude Code animate them in Remotion** with layered parallax, a "film treatment" (grain, grunge, scan lines, vignette, halftone), subtle idle motion ("boil", drift, flicker), frame-accurate choreography, and voiceover, SFX and music mixed in at render. Claude never draws pixels. It writes the storyboard, the prompts, the React/Remotion code and the ffmpeg mix. The generation APIs supply raster art (stills, a few i2v clips), the voice and the music. For our target (Indian mythology / devotional story reels in Hindi or English), the same pipeline works if we add three things: cinematic AI stills plus a few image-to-video hero shots, Devanagari or Hinglish kinetic captions, and a devotional score.

---

## (a) Recommended production pipeline (this sandbox)

### What is in the sandbox (checked 2026-11-09)
- node v22.23, npm 10.9, ffmpeg 6.1.1, Python 3.13 with `faster-whisper` 1.2.1 and Pillow. Chrome is at `/usr/bin/google-chrome`, and Playwright browsers are under `/opt/pw-browsers`. 4 vCPU, 15 GB RAM.
- **No Devanagari font is installed.** `fc-list` shows only Noto Color Emoji among the Noto fonts. Load one through `@remotion/google-fonts` (Noto Sans Devanagari, Tiro Devanagari Hindi, Yatra One, Mukta, etc.) or through `@fontsource/*` from npm.
- **Treg connector** (no keys needed; prices from `catalog_get`):

| Need | Best Treg endpoint | Price | Notes |
|---|---|---|---|
| Still images (hero art, cut-outs, backgrounds) | `google-ai.image-gen.gemini-3-1-flash-image` (Nano Banana 2) | $0.05–0.165/img (512→4K) | `aspectRatio: "9:16"`, reference images supported (character consistency and editing). Reviews: 93% "useful". |
| | `reapi.image-gen.gpt-image-2` / `piapi…gpt-image-2-5` | $0.08 / $0.16 | Alternative look. MoSidd's default image model is "GPT Image 2" via Replicate (7wuYBfE131U, aSNYHAzPEKc). |
| | `replicate.image-gen.flux-schnell` | $0.012 | Cheap drafts, textures, storyboard thumbnails. |
| Image→video hero shots | `replicate.video-gen.veo-3.1-fast` | $0.10/s silent, $0.15/s with audio; 4–8 s | Accepts a start `image`, `aspect_ratio: "9:16"`, 1080p. Reviews: "9:16 I2V from hero still… usable"; "anti-morph re-render when digits drifted". |
| | `openrouter.video-gen.seedance-2-5` | $0.10/s (480p), $0.23/s (720p); 4–30 s | First and last frame supported, 9:16. Top of the public I2V arenas (Seedance 2.x). One review reports billing at the 720p rate even when 480p was requested. |
| | `openrouter.video-gen.wan-3-0.from_image` | $0.05/s (480p), $0.10/s (720p), $0.20/s (1080p) | Cheapest option at 1080p. |
| | `minimax.video-gen.from_image` (Hailuo) | ~$0.56/call | |
| | Kling (v2/v3) | needs our own Replicate key | Not served by Treg. |
| Voiceover | `minimax.voice-gen.speech-2-8-hd` | $1 per 10k chars (a 60 s script costs ~$0.08) | **Hindi `language_boost`**, emotions, `<#0.5#>` pause markers, **`subtitle_type: "word"` returns word timestamps**. This is the key piece for captions. |
| | `google-ai.voice-gen.gemini-3-8-flash-tts` | ~$0.002 per 10 s | 30 voices, style goes in `speechMetadata.style` (not in the spoken text), two-speaker dialogue supported. WAV at 24 kHz. |
| | `fishaudio.tts.s2-1-pro` | (check price) | Alternative. |
| Music | `google-ai.music-gen.lyria-3-5` / `lyria-3-clip` | $0.08 / $0.04 | MoSidd uses Lyria 2 for score (aSNYHAzPEKc). |
| SFX | **none in Treg** | — | Options: Veo/Seedance native audio on hero clips, synthesise whooshes and risers in ffmpeg, or use a CC0 library. ElevenLabs is not in Treg. |
| Background removal / matting | **none in Treg** (`catalog_search` → "gap") | — | Generate on a flat chroma or white background and key it in code, or run `rembg` locally (its weights download from GitHub). |

### Division of labour

| Step | Claude does it in code | Needs a generation API |
|---|---|---|
| Story, hook, script (Hindi/English/Hinglish), beat sheet | ✅ | |
| Storyboard + per-scene choreography + asset sheet | ✅ (MoSidd: "prompt Claude Code to give me the choreography in each scene… it'll give you an asset list", xOhh274Ayac) | |
| Image prompts (style bible, consistent character sheet) | ✅ | |
| Stills: deity/character art, backgrounds, props | | ✅ Nano Banana 2 / GPT Image 2 |
| Cut-out alpha, B&W, halftone, duotone, grade, masks | ✅ (CSS/SVG filters in Remotion, or Pillow/ffmpeg; "tell Claude code to make the image black and white and give it a half tone pattern", 7wuYBfE131U) | (matting is easier if the image API gives a flat background) |
| 2.5D motion: parallax layers, push-ins, drift, boil, flicker, light swings, particles, smoke | ✅ Remotion `interpolate`/`spring`, Three.js for true 3D (b7KlsXNQobs) | |
| "Real" motion: hair/cloth, water, fire, a deity turning their head | | ✅ i2v (Veo 3.1 Fast / Seedance 2.5 / Wan 3.0), 4–8 s hero shots |
| Voiceover | | ✅ MiniMax Speech 2.8 HD (Hindi) / Gemini TTS |
| Word timings → kinetic captions | ✅ (`@remotion/captions` `createTikTokStyleCaptions()` fed by MiniMax word timestamps) | |
| Music bed | | ✅ Lyria 3.5 |
| SFX (whoosh, bell, conch, riser, thunder) | ✅ ffmpeg synthesis or library | (or i2v native audio) |
| Mix: ducking, loudness −14 LUFS, true peak −1 dBTP | ✅ ffmpeg `sidechaincompress`, `loudnorm` | |
| Render 1080×1920 H.264 + AAC, QC frames | ✅ `npx remotion render` + ffmpeg/ffprobe + contact sheet via `scripts/analyze_reel.py` | |

### Step by step (a 60 s mythology reel, ~6–10 scenes)

**0. Project bootstrap (one time, about 5 min).**
```bash
npx create-video@latest reel --blank   # or bun create video
cd reel && npx skills add remotion-dev/skills   # official Agent Skills (remotion-best-practices, -captions, -render, -markup, …)
npm i @remotion/captions @remotion/google-fonts @remotion/media-utils @remotion/three three
```
- Remotion downloads its own `chrome-headless-shell` on first render. If the proxy blocks that download, pass `--browser-executable=/usr/bin/google-chrome`.
- Composition: 1080×1920, 30 fps (24 fps for a filmic feel; the reference reels run at 24 and 30). Folder structure as MoSidd uses it (7wuYBfE131U): `public/scenes/sNN/{bg,mid,fg}.png`, `public/textures/{grain,grunge,scanlines,vignette}`, `public/audio/{vo,music,sfx}`. **One composition per scene, plus a `Master` composition** that sequences them. Building scene by scene stops a fix in one scene from breaking another (xOhh274Ayac, GvC9zXk4l7s, Y6mOBK5peDU).
- Ask Claude for **Zod-schema props on every element** (scale, x, y, opacity, blur, saturation, timing). The person or agent tunes them in Studio's prop panel, and Studio saves the values back to code (7wuYBfE131U, dBakc0BdHjY, rK4vrMK4i2U). Headless, Claude does the same tuning by rendering stills: `npx remotion still Master --frame=N`.

**1. Script and beat sheet (Claude).** Write 5–8 voiceover lines of about 5 s each. **The voiceover is the timeline**: "No more than five or six voice lines. Each voice line is about 5 seconds" (xOhh274Ayac); "each snippet of the voiceover becomes one scene" (rK4vrMK4i2U). Structure: a 1–3 s hook ("You have been doing Aarti wrong.", from the reference reel `therishikatha`), a story turn, a reveal, and a closing line or CTA ("Part 2…" in `anchorlinedigital`). Output `beats.json` with `{id, vo_text, vo_lang, visual, choreography, captions_emphasis[], sfx[]}`.

**2. Style bible + asset sheet (Claude).** Lock one visual system: palette (for devotional reels, saffron, gold, deep indigo, ember), 1–2 fonts (a Devanagari display face plus a Latin serif such as Cinzel or Cormorant), one texture stack, one grade. "Lock a visual system… same fonts, same accent palette" (7wuYBfE131U); "use the same finish for every scene… the eye is really good at picking up these subtle differences" (GvC9zXk4l7s). The asset sheet lists every bg, mid and fg layer per scene, with a generation prompt for each. MoSidd's photoreal prompt formula: _framing + subject + outfit + action/pose + setting + lighting + camera/lens + quality tags_ (8qBIinJzUmE).

**3. Generate stills (Treg).** About 3–4 images per scene, so 20–35 images (~$2–4). Use Nano Banana 2 at 2K in 9:16 for backgrounds. Generate characters or deities **on a flat solid background** so they key cleanly, and pass the first approved character image as a **reference image** on every later call to keep the character consistent. Generate backgrounds larger than the frame (MoSidd generates ~6K so he can push in; rK4vrMK4i2U). Build a contact sheet and have Claude review it (Read the image), then regenerate any failures.

**4. Prepare assets in code (Claude).** Key out the background, add an edge feather and a drop shadow, split parts for rigging (e.g. mask a wheel so it spins, rK4vrMK4i2U; mask a hull so the passengers sit inside the boat, aSNYHAzPEKc). Apply the shared grade or halftone. SVG assets can be animated directly (blinks, sways; zCuthqXIAcg).

**5. Voiceover first (Treg), then retime.** Call MiniMax Speech 2.8 HD with `language_boost: "Hindi"` (or English), `subtitle_enable: true, subtitle_type: "word"`, `emotion: "calm"`, or a deep narrator voice for mythology, with pause markers between beats. Generate **one file per line** (MoSidd syncs each scene to its own line: "each scene should start and end on its own narration", 7wuYBfE131U), or one file and split it on the word timestamps. Set each scene's `durationInFrames` from the measured audio (`getAudioDurationInSeconds`) plus 6–10 frames of tail. A second option is Gemini 3.8 Flash TTS (put style in `speechMetadata`). Pick the voice by A/B listening, as MoSidd does when he picks a narrator in Claude Code (Y6mOBK5peDU).

**6. Hero motion clips (Treg, optional, 1–3 per reel).** Use them only where 2.5D motion can't deliver the moment (a deity opening their eyes, a river of fire, a chariot charge). Veo 3.1 Fast, i2v from the approved still, 9:16, 6–8 s, silent (`generate_audio:false`), about $0.60–0.80 each. Use Seedance 2.5 with first and last frame when the shot must land on a specific end frame. Treat the clip as just another layer in Remotion (`<OffthreadVideo>`). MoSidd builds all of his hits **without** i2v, so the 2.5D route alone is enough to look professional. The reference mythology reels (`artandartists_ai`, `therishikatha`) do show i2v-style painterly motion, though.

**7. Animate each scene (Claude in Remotion).** This is the MoSidd technique catalogue, all of it code:
- **Camera without a camera:** scale and translate a wrapper div. "Slow push 1→1.16, then accelerate to 6.8× from frame 46 to 76"; a portal "weld and detach" where frame and photo travel together until frame 62 (f393grXJn9E, xOhh274Ayac).
- **Parallax:** the background zooms slower than the character, and a fake contact shadow (a duplicated, darkened, skewed copy) grounds the figure (xOhh274Ayac).
- **Idle life:** cloud drift, character "boil" (a small per-frame jitter from fractal noise), sine bob with amplitude and frequency props (iceberg, GvC9zXk4l7s), a lamp swing plus light flicker using hold keyframes (xOhh274Ayac), and eyes glowing red (rK4vrMK4i2U).
- **Easing:** use `Easing.out` for an editorial or documentary feel. `spring` pops (e.g. damping 19, stiffness 280; dv3ADYu74DE) suit callouts. Stagger elements so nothing arrives all at once (xOhh274Ayac's newspapers, dv3ADYu74DE's bars).
- **Stop-motion feel:** posterize time (12–15 fps steps) on **selected layers only**, and vary the holds ("turn off the metronomic grid"; aSNYHAzPEKc, GvC9zXk4l7s).
- **Overlays:** stock smoke, fire or explosions on black, screen-blended, with greys crushed and edges feathered (xOhh274Ayac, Y6mOBK5peDU, rK4vrMK4i2U). For mythology: diya flames, incense smoke, dust motes, light rays, petals.
- **Seamless transitions:** each scene starts on the last frame of the previous one (one continuous shot; Y6mOBK5peDU, rK4vrMK4i2U). Pull-back/push-in beats a pan, which "looks a bit amateur" (GvC9zXk4l7s).
- **Address time in frames, not seconds:** "do a motion blur from frame 56 to 67" (xOhh274Ayac). Claude should print frame numbers for every beat in `beats.json`.

**8. Film treatment (Claude, one shared component).** Grain plus grunge "texture sandwich", scan lines ("1.6 px black line at 16%"), vignette, colour grade, gate weave, corner blur (xOhh274Ayac); halftone for a magazine look (7wuYBfE131U, rK4vrMK4i2U); marker-edge noise and boil on graphics (dv3ADYu74DE). This is what MoSidd credits for the jump from "just a digital image" to "a lot more cinematic". For devotional reels, swap the grunge for a warm bloom, a light-leak glow and soft film grain at about 8–12%.

**9. Kinetic captions (Claude).** Feed MiniMax word timestamps into `createTikTokStyleCaptions()`. Show 1–3 words per page, bold, centred in the lower third away from faces, with a key word in an accent colour. This is exactly the reference `anchorlinedigital` style: Hinglish in Latin caps, "ANDHERA" and "BUJHNE" in red. `therishikatha` uses a serif in small caps over gold. Pick per channel: Hinglish in Latin script (most readable and most common) or Devanagari. Always caption from **our script text**, never from Whisper. The local faster-whisper Hindi transcript in `analysis/anchorlinedigital…/transcript.json` is badly garbled ("त्रेन राद दोबगजे").

**10. Music, SFX, mix (Treg + ffmpeg).** Music: Lyria 3.5 ("devotional cinematic, tanpura drone, low taiko and dhol, slow build, 90 bpm, no vocals"), about $0.08. SFX: bell, conch, whoosh on camera moves, riser into the reveal. MoSidd layers whooshes on every camera move plus a riser at a named frame ("at 620 frames make sure a riser happens", rK4vrMK4i2U). Mix with Remotion `<Audio volume={…}>` ducking, or in ffmpeg (`sidechaincompress`, then `loudnorm=I=-14:TP=-1`). The reference reels peak at around −9 to −12 LUFS short-term (`analysis/*/meta.json`).

**11. Render and QC (Claude).** `npx remotion render Master out.mp4 --codec=h264 --crf=18 --concurrency=4`. Then run `python3 scripts/analyze_reel.py out.mp4` for cuts, shot lengths, loudness and a contact sheet. Claude views the contact sheet and spot-frames, fixes issues per scene by frame number, and re-renders. Targets from the references: first cut by 1.8–3.5 s (or continuous motion), mean shot about 2.4–3 s for the energetic style, with loudness and true peak as in step 10.

**Cost and time per 60 s reel:** about 30 images (~$3), 0–3 i2v clips (~$0–2.5), voiceover (<$0.10), music (<$0.10). **Roughly $3–6 total.** That matches MoSidd's "about $4 in API credits" (aSNYHAzPEKc). Remotion rendering on 4 cores should take minutes.

### Alternatives we considered, and why we don't recommend them as the default
- **EffectCraft / FilmCraft** (ArtCraft "Crafting Apps"): EffectCraft is an open-source After Effects clone in Rust with 306–308 effects and an MCP server (`effectcraft-cli mcp`, headless mode). It exports H.264, ProRes, WebM and Lottie on Linux. FilmCraft is the matching Premiere-style editor (cuts, colour, sound) (DceFrd65KUg, zCuthqXIAcg; https://raw.githubusercontent.com/storytold/effectcraft/main/README.md; https://getartcraft.com/apps/effectcraft). The project calls itself alpha and "not yet recommended for production client work"; one review rates it about 45% ready for professional work (https://aiidelist.com/blog/effectcraft-review). It is worth a later experiment for a keyframe-and-effects workflow that a human can open and tweak, but Remotion + code is more deterministic and easier to diff for an agent.
- **All-in-one "script-to-video" tools** (InVideo, Revid, FluxNote, Atlabs): they produce Hindi voiceover, stock and AI visuals and captions in a single pass, but the output is generic and Claude does no craft. That defeats the purpose of this study (https://fluxnote.io/guides/ai-video-generator-hindi, https://www.revid.ai/category/hindu-mythology).
- **Generating graphs or text with image or video models:** MoSidd tried it, and the output was "pretty bad… none of them are actually usable" (dBakc0BdHjY). Render all text, numbers and captions in code.
- **Pure ffmpeg (Ken Burns + drawtext):** this is a fallback if Remotion can't install. It works for a basic slideshow but loses the layering, springs and caption tooling.

---

## (b) MoSidd video summaries (Claude/Remotion/reel-related; 2022 generic videos and OpenClaw/dropshipping videos skipped)

| id | Title | Views | Technique / stack | Key takeaways for us |
|---|---|---|---|---|
| 7wuYBfE131U | I Made Vox-Style Motion Graphics Using Only Claude Code & Remotion | 263,654 | Claude Code + Remotion. Higgsfield and Magnific MCP connectors for cut-outs. ElevenLabs voiceover ("Kate", British RP). | Script table maps each VO line to bg, mid and fg assets plus image prompts. One locked background; halftone B&W characters with an offset red marker stroke; `spring` stagger. Prop controls for scale and x/y. Assemble a master, then "sync scenes to voice-over". 47 s piece. |
| xOhh274Ayac | I Made This Viral Reel Using ONLY Remotion & Claude Code | 150,620 | Remotion 1080×1920@30, Claude Code. Assets from Google Images, GPT Image 2 via Replicate, and asset packs. ElevenLabs for VO **and SFX**, plus a music track. | 6 lines × ~5 s gives 6 scenes. Claude writes the choreography and asset list. Film look (grain, grunge, 1.6 px scan lines at 16%, vignette, gate weave). Portal weld/detach. Character boil, cloud drift. Smoke screen-blend with crushed greys. Parallax plus a fake shadow. Lamp swing and flicker. Reference frame numbers. Scene-by-scene, then a master. |
| f393grXJn9E | Full Remotion Tutorial to Create Insane Motion Graphics | 28,403 | Remotion install (CLI with agent skills, or "ask Claude"), Studio tour. 3 builds: bar chart, timeline, reel. | Write prompts like specs: build / copy / data / colours / motion sections. The camera is a div transform (scale 1→2.8). Halftone unifies mismatched Google-Images assets. 12 fps stepped motion. Remotion is weak at cutting and colour, strong at graphics and type. |
| b7KlsXNQobs | I Made This SaaS Animation Using ONLY Claude Code & Remotion | 23,591 | Remotion 1920×1080; CSS glassmorphism plus a **Three.js** refractive sphere, rendered in two passes and composited. | Quality comes from knowing the parameters (blur 12–14 px, edge light 16%, 58% opacity, 22 px radius, light 38 px blur, refraction 1.35×). Tuning each one gets you "the difference between AI slop and client-ready". |
| aSNYHAzPEKc | Claude Fable 5 + Remotion Built This $1,000 Collage Animation | 20,414 | Claude **Fable 5** in Claude Code. GPT Image 2 via Replicate (~25 generations, about $4). Lyria 2 + ElevenLabs audio. | Prompt 1: download a reference video (Behance), step through it frame by frame, write a master asset sheet and a storyboard. Prompt 2: generate every cut-out as a transparent PNG and a contact sheet. Build layer by layer. Posterize selected layers. Hull/pilgrim "sandwich". 4 prompts total. |
| rK4vrMK4i2U | I Made Documentary Motion Graphics Using Only Claude Code & Remotion | 15,966 | Remotion. AI images via Replicate plus Google Images. Looping cloud video background. ElevenLabs "Kate". | 3 VO lines give 3 scenes. Generate backgrounds at ~6K so you can push in. Mask car wheels so they spin. Smoke overlay on a cigar. Red eye glow. Prompts give exact frames, x/y, saturation 65%, brightness 86%. SFX: counter, pencil, engine, risers. |
| Y6mOBK5peDU | I Built a Vox Explainer Using Claude Code & Remotion (No Plugins) | 14,322 | Remotion + world-atlas + TopoJSON + d3-geo maps. ElevenLabs VO and SFX (picked inside Claude Code); Magnific music. | Six prompts. Each scene starts on the previous scene's last frame, so it plays as one shot. Ease-out is the "Vox" ease. Explosion video on black keyed by screen blend. A film-grain pass at the end. Claude generates the music prompt and the foley list. |
| GvC9zXk4l7s | I Made This Minimal Reel Using ONLY Remotion & GPT 6 | 10,982 | GPT-6 Astra (Codex) + Remotion + GSAP, **15 fps** stop motion, GLB 3D eye. ElevenLabs VO; SFX via GPT. | 3 colours, very few assets. Icons, battery, contour lines and halftone are all procedural. Build layer by layer: bg, practicals, hero, blur, type and finish. Sine-bob iceberg. Shared print finish. Pull-back/push-in transitions. Symbolism in the storyboard. |
| dBakc0BdHjY | Create Animated Charts and Graphics Instantly with AI & Remotion | 5,868 | Cursor + Opus 4.5 + Remotion; screenshots of Jitter/Hera templates used as references. | Image models (Nano Banana Pro, Kling) produced unusable charts. Code gives pixel-perfect, editable output. Ask for "full prop control". Render with a transparent background for overlays (ask the agent to render it, because the Studio render bugs out). |
| dv3ADYu74DE | Vox-Style Animated Charts With ONE PROMPT | 4,983 | Remotion + Claude Code, one prompt per chart. | Paper look = paper grain + marker-edge noise + full-frame grain. "Boil" (fractal noise) is right; too much becomes "buzz". Parliament chart uses a lattice with a left→right wave. |
| DceFrd65KUg | I Made This Viral Reel Using ONLY EffectCraft & Claude Code | 44,657 | EffectCraft (open-source After Effects alternative) driven by Claude/GPT through MCP. | One prompt installs the app and configures MCP. The scene is built from a detailed prompt plus an asset folder. Keyframe edits by prompt ("tint 100 until frame 50 → 0 at frame 55"). Exports 1080×1920 MP4. |
| zCuthqXIAcg | I Made This Talking Head Explainer Using ONLY FilmCraft & Remotion | 1,499 | FilmCraft (Premiere-like) for cuts, LUT and audio, plus Remotion graphics composited on top; Replicate for a character in a matching style. | The agent removes bad takes, converts S-Log2 to Rec.709 with a LUT, and does EQ and compression. SVG assets are easy for agents to animate. Generating new characters from a style reference keeps everything consistent. |
| UW-jxCvuH9E | I Automated My Entire Video Edit With GPT-6 (Premiere Pro) | 2,722 | GPT-6 Astra (Codex) driving Premiere; Replicate matting for text-behind-subject. | Cut down 21 min of footage to 10 min (rated 8/10; sometimes clips words, so add 5 frames after each sentence). Audio −22.4 → −16 LUFS with HPF 70 Hz, EQ and compression. Punch-ins: 13% over 0.28 s, cubic ease-out. Matting cost $0.011 and took 11 s. |
| W48cbXsIdzk | Claude Fable 5 vs Opus 4.8 | 466 | Same Remotion prompt on both models. | **Fable 5 rendered Arabic calligraphy legibly where Opus 4.8 botched it**, and built an HTML player unprompted. Relevant for Devanagari. Costs about 2× and hits Max-plan usage limits. |
| 8qBIinJzUmE | Flux LoRA Masterclass | 967 | Replicate `ostris/flux-dev-lora-trainer`, 20–40 photos, 2–3k steps, rank 32, about $3–4. | Recipe for a recurring presenter or character. Prompt formula: framing, outfit, pose, scene, lighting, camera, quality. |

Common threads across the hits:
1. VO-first storyboard: one line per scene, 5–6 lines.
2. Few assets with heavy reuse: shared background, swapped characters.
3. A film treatment unifies mismatched sources.
4. Subtle idle motion everywhere.
5. Frame-number-precise prompts.
6. Build scene by scene, then a master.
7. Tune in Studio with props.
8. Sound design (VO, SFX, music) is "one of the most important steps".

MoSidd also claims "you don't need to know how to code", but every video still involves a human tweaking props visually. **The open question for this project is whether Claude can replace that visual tuning loop** by rendering stills and judging them.

---

## (c) Open questions and risks

1. **Visual QC without a human.** MoSidd's quality depends on hand-tuning props in Studio (scale, eye positions, logo placement; xOhh274Ayac). Our loop has to be: render stills or a contact sheet → Claude inspects the images → patch props. We need to measure how many iterations this takes and whether Claude catches things like misaligned eyes or text crowding.
2. **Devanagari rendering and Hindi TTS quality.** Conjuncts and matras need proper shaping. Chrome handles it if the font is loaded, but check for clipping at heavy weights. Fable 5 handled Arabic better than Opus 4.8 (W48cbXsIdzk). MiniMax Hindi pronunciation of Sanskrit names (e.g. "Hiranyakashipu", "Pradyumna") needs `pronunciation_dict` testing. Gemini TTS Hindi support has not been verified yet.
3. **Captions from timestamps.** Local Whisper is poor at Hindi (see `analysis/anchorlinedigital…/transcript.json`). The plan depends on MiniMax `subtitle_type:"word"` timings. If those are unreliable for Hindi, fall back to sentence timings with evenly spread words, or forced alignment.
4. **No SFX and no background removal in Treg.** ElevenLabs (MoSidd's VO and SFX source) isn't available. Decide between ffmpeg-synthesised SFX, a CC0 library (licensing, and whether the proxy reaches it), and i2v native audio. For cut-outs, test flat-background generation plus keying versus `rembg` (model download through the proxy).
5. **AI image consistency for deities and characters** across 20–30 images. Use reference-image conditioning in Nano Banana 2, and consider a LoRA (8qBIinJzUmE, about $4, via Replicate; needs our own key). **Religious sensitivity:** iconography errors (wrong number of arms, wrong vahana, wrong mudras, mismatched attributes) will draw backlash on devotional pages. Claude should write an iconography checklist per deity and check every frame against it.
6. **i2v artefacts and cost.** Veo and Seedance reviews mention morphing digits, jittery wings, and broken cause and effect between first and last frames. Seedance via OpenRouter was once billed at the 720p rate for a 480p request. Keep i2v to 1–3 short hero shots and budget for one re-roll each.
7. **Remotion licence.** Free for individuals and companies of 3 or fewer people. Larger companies need a Company License (Creators $25 per seat per month; Automators minimum $100/month) (https://www.remotion.dev/docs/license/faq, https://remotion.dev/license). Check before any commercial use.
8. **Rendering in the sandbox.** First render downloads `chrome-headless-shell`, which may be blocked by the proxy (fallback: `--browser-executable=/usr/bin/google-chrome`). The rendering speed of WebGL/Three.js layers headless on 4 CPUs (no GPU) is unknown. Keep 3D to a minimum or pre-render it.
9. **Style fit.** MoSidd's look is Vox/collage/documentary. The reference mythology reels are painterly-cinematic (`artandartists_ai`), flat-vector stories (`anchorlinedigital`, 18 shots in 49 s) and glowing 3D devotional (`therishikatha`). Our 2.5D parallax + film treatment pipeline fits the first two well. The glossy 3D-temple look will rely more on i2v.
10. **Unverified claims.** MoSidd's "viral" and "$1,000" framing is marketing. His prompts and assets are behind the Skool community (https://www.skool.com/ai-visual-production-lab-4976) and we have not reviewed them. Model names in his videos (GPT-6 Astra, Fable 5, GPT Image 2) and Treg's catalogue (Seedance 2.5, Wan 3.0, Lyria 3.5, Gemini 3.8 TTS) are current as of Nov 2026. Third-party rankings disagree: Seedance 2.0 tops Artificial Analysis T2V and I2V, while Techsy names Veo 3.1 the best all-rounder (https://techsy.io/en/blog/best-ai-video-models, https://atlascloud.ai/blog/guides/best-ai-video-generation-models-2026).

### Sources
- Transcripts: `data/youtube_mo-sidd/<id>.en.vtt` for the ids in table (b).
- Remotion Agent Skills: https://www.remotion.dev/docs/ai/skills (install `npx skills add remotion-dev/skills`; skills: best-practices, create, markup, studio, render, maps, captions, interactivity, docs, license, …)
- Remotion licence: https://www.remotion.dev/docs/license/faq, https://remotion.dev/license
- Claude Code + Remotion workflows and captions (Whisper → `createTikTokStyleCaptions`): https://www.tella.com/blog/how-to-use-remotion-agent-skills-with-claude-code, https://www.nemovideo.com/blog/remotion-agent-skills-claude-code-guide, https://vloggingpro.com/ai/workflows/agentic-remotion-videos/
- EffectCraft / FilmCraft: https://raw.githubusercontent.com/storytold/effectcraft/main/README.md, https://getartcraft.com/apps/effectcraft, https://aiidelist.com/blog/effectcraft-review, https://pasqualepillitteri.it/en/news/23653/effectcraft-free-after-effects-alternative-rust
- Video model landscape: https://techsy.io/en/blog/best-ai-video-models, https://atlascloud.ai/blog/guides/best-ai-video-generation-models-2026, https://evolink.ai/blog/best-ai-video-generation-models-2026-pricing-guide
- Mythology reel production (typical stack Midjourney → Runway → Suno → Premiere/After Effects; generate 9:16 stills then animate; separate Hindi voiceover): https://contra.com/p/RNNr63Mb-gen-ai-video-production-for-indian-mythological-stories, https://fluxnote.io/guides/ai-video-generator-hindi, https://info.invideo.io/i-want-to-make-faceless-mythology-videos-whats-the-best-ai, https://help.atlabs.ai/en-us/article/how-do-i-make-faith-and-devotional-videos-christian-islamic-hindu-etc-171p5nd/
- Treg catalog entries (live, 2026-11-09): `google-ai.image-gen.gemini-3-1-flash-image`, `reapi.image-gen.gpt-image-2`, `replicate.video-gen.veo-3.1-fast`, `openrouter.video-gen.seedance-2-5`, `openrouter.video-gen.wan-3-0.from_image`, `minimax.voice-gen.speech-2-8-hd`, `google-ai.voice-gen.gemini-3-8-flash-tts`, `google-ai.music-gen.lyria-3-5`.
- Reference reels: `analysis/{anchorlinedigital__DfCTMOFDrgx, artandartists_ai__DevsUAKS1hP, therishikatha__De8phEeIRf3, anim_aman__DfOiMdsRMFM}`.
