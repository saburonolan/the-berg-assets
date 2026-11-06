# The Berg tools (runbook for scheduled sessions)

Repo is public: never put passwords, tokens or personal data here.
The Berg app + database: https://claude.ai/artifact/UZSbKdhpV7jwv2t7E6UGyV (ArtifactData tool, collections: missions, jobs, notebooks, runs, signals, earnings, chat).

## Browser
Use Claude in Chrome, "Browser 1" (deviceId fb61d938-2d12-4dc8-9685-6fd3990ba934). If Chrome isn't reachable, mark browser jobs "failed" with note "PC asleep or Chrome closed" and move on.
Files reach upload forms by fetching them from raw.githubusercontent.com inside the page and injecting with DataTransfer into input[type=file]. Pin helper URLs to a commit SHA (raw "main" is cached ~5 min). Keep each browser_batch under ~60 s (one design per batch).

## Redbubble (brand everydayiprint)
`python3 tools/redbubble/mkbatch.py <n> <tabId>` prints a browser_batch for design n (19-50 in queue.json). The final step returns the /shop/ap/<id> link; log with `python3 logrb.py <n> <id>` in tools/redbubble. Daily upload cap: stop when the page says "exceeded your upload limit".
Colors: white/light products only (dark ink). safe_for_work true, rights declaration checked.

## TeePublic (store everydayiprint)
`python3 tools/teepublic/tp3.py <n> <tabId>` prints a batch for design n using everydayiprint/tp.js + tp-data.json. Always start from a fresh /design/quick_create draft; never re-upload onto a stalled draft (TeePublic returns 500). ~25 designs per rolling 24 h. Log "<n>\t<designId>" to teepublic-live.txt.

## RenterFix Shorts (YouTube @renterfix, Google account sf01.theberg)
Setup: `pip install --break-system-packages kokoro-onnx soundfile pillow numpy`; download kokoro-v1.0.onnx and voices-v1.0.bin from https://github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0) into $KOKORO_DIR. Fonts: Poppins (google-fonts).
Write a spec like short1.json (segments with scene names from make_short.py: hook, faucet, cabinet, hose, thermo, warn, stat, vs, heater, sediment, hair, stopper, snake, chem, grease, cta), then `KOKORO_DIR=... python3 tools/shorts/make_short.py spec.json`.
Rules: every fact from 2+ reputable sources, cited in the description; "General info only... call a licensed pro" line; "Voiceover: AI-generated"; Studio "AI was used" = Yes; not made for kids; no paid promotion. Upload in YouTube Studio (studio.youtube.com) and schedule one per day at 4:00 PM Pacific.

## Approvals
A job Nolan posts (status "requested") counts as his approval. Anything a penguin proposes on its own that would publish or post publicly: create it as status "awaiting" and stop. Only run it once Nolan sets it "approved". Never spend money, create accounts, enter passwords or accept new terms.
