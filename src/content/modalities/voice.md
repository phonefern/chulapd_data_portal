---
title: Voice
slug: voice
summary: Sustained phonation and connected-speech recordings supplied as standard audio files.
flag: voice_available
status: partial
---

## Task protocol

The voice release contains two tasks: `voiceAhh` is sustained phonation, while `voiceYPL` is connected speech.

<div class="todo">TODO — pending clinical team: confirm the exact spoken instructions, recording posture, device models, operating-system versions and CheckPD app version used for this release.</div>

## Sensor and format

- Audio format: WAV
- Channels: mono
- Sampling rate: 16 kHz
- Duration, `voiceAhh`: variable, 3–10 seconds — the natural phonation length is kept
- Duration, `voiceYPL`: exactly 5.000 seconds — segmented to a fixed window
- File patterns: `voice/voiceAhh/S####_voiceAhh.wav` and `voice/voiceYPL/S####_voiceYPL.wav`

## Preprocessing

Preprocessing is automatic; no recording is segmented by hand.

`voiceAhh` is **not segmented at all**. Sustained-phonation length is Maximum Phonation Time, a clinical measure in its own right, so the natural duration is kept — truncated only at the app's 10 s recording limit, and rejected below 3 s as an aborted attempt.

`voiceYPL` is segmented automatically to a fixed 5 s window: 25 ms RMS frames, an ambient noise floor taken as the 20th percentile, and the 5 s position carrying the most speech energy above that floor. One contiguous span is kept, so rhythm and timing inside the window survive — it is not a silence-removing VAD.

## Quality control

Each WAV must be readable, mono and sampled at 16 kHz.

Duration is checked per task, not with one shared tolerance: `voiceAhh` must fall between 3 and 10 seconds, and `voiceYPL` must be exactly 5.000 seconds. A `voiceYPL` recording shorter than 5 seconds is zero-padded rather than rejected, so padded clips are flagged and reviewed rather than assumed usable. Availability flags are checked against files present in the release.

## Example structure

```text
voice/
├── voiceAhh/S####_voiceAhh.wav
└── voiceYPL/S####_voiceYPL.wav
```

Source: `CheckPD_Local_Agent_Context.md` §8.
