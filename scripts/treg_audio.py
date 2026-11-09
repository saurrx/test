#!/usr/bin/env python3
"""Extract the audio from a saved Treg tool result (Gemini TTS wav / Lyria mp3) into a file.
Usage: treg_audio.py <tool-result.txt> <out-basename>   -> writes <out-basename>.wav|.mp3, prints cost."""
import base64, json, sys
d = json.load(open(sys.argv[1]))
if isinstance(d, list):  # MCP content wrapper
    d = json.loads(d[0]["text"])
for p in d["body"]["candidates"][0]["content"]["parts"]:
    if "inlineData" in p:
        ext = "mp3" if "mpeg" in p["inlineData"]["mimeType"] else "wav"
        open(f"{sys.argv[2]}.{ext}", "wb").write(base64.b64decode(p["inlineData"]["data"]))
        print(f"{sys.argv[2]}.{ext}", "cost_usd", d.get("cost_usd"))
