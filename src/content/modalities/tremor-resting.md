---
title: Tremor - resting
slug: tremor-resting
summary: Resting-tremor measurements represented as six-channel smartphone inertial data.
flag: tremor_resting_available
status: partial
---

## Task protocol

This modality records inertial measurements for the resting-tremor task.

<div class="todo">TODO — pending clinical team: confirm the exact resting position, hand and device placement, task duration, participant instructions, device models, operating-system versions and app version.</div>

## Sensor and format

Files are JSON. Channel order is exactly `gx, gy, gz, ax, ay, az`. Gyroscope values use `rad/s`; accelerometer values use `m/s²`. Sample time `t` is relative seconds from zero, never an absolute timestamp. The sampling rate is estimated for each file and is approximately 40 Hz.

## Preprocessing

Non-increasing timestamps are removed before the sampling rate is estimated. Timestamps are converted to relative time from zero.

## Quality control

Files outside 20–100 Hz are flagged and excluded. Validation also checks schema, channel order, units, subject membership and agreement with the availability flag.

## Example structure

```json
{
  "subject_id": "S####",
  "modality": "tremor_resting",
  "sampling_rate_hz": 39.8,
  "units": { "gyroscope": "rad/s", "accelerometer": "m/s^2" },
  "channels": ["gx", "gy", "gz", "ax", "ay", "az"],
  "data": [
    { "t": 0.000, "values": [0.01, 0.02, 0.03, -0.12, 0.08, 0.04] }
  ]
}
```

Source: `CheckPD_Local_Agent_Context.md` §9.
