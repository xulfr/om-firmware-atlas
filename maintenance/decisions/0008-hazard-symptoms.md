# 0008 — Hazards grouped by symptom

Status: proposed, 25 November 2026.

Hazards are listed by rule, which suits someone writing a patch. Someone holding a failing build starts from what they see: a camera that restarts at power-on, a slow start, a freeze when a feature runs. On 25 November, EPM2Mod traced ten-second cold starts on the E-PM2 to a hook that jumped into a segment still being copied. The same cause had already been recorded for four other bodies under "Only call code in a section that has already loaded". The title did not say that a slow start was one of its symptoms, so a reader starting from the symptom would not have found it.

Each hazard now lists one or more `symptoms` from a short list in `taxonomy/topics.yaml`. The checker requires them on hazards, rejects unknown symptoms, and rejects them on other categories. The technical reference index adds "Diagnose by symptom", which lists for each symptom every hazard that shows it, with its cameras and status. Each hazard page links its symptoms. The per-camera agent shards are unchanged, because the OM-5 Mark II research route was already at its token budget.

A symptom leads to a cause to check on another body. It does not diagnose that body. Addresses and results still never transfer between builds.

Alternatives: keep the consequence as free text only, which cannot be grouped; or a separate symptom record type, which would duplicate the hazard's sources and status.
