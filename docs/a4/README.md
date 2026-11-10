# Assignment 4 evidence pack

This pack supports the university brief `ICT_Assignment_4.pdf`, pages 1–3. It is not a claim that the assignment is ready for submission. Generated with Codex assistance; team members must verify, understand, and disclose that assistance according to instructor policy.

## What is completed

- `format_comparison.md`: ten format/container/codec combinations and project uses.
- `measurements.csv`: actual image and ten-second audio encoding measurements.
- `experiments/side-by-side-native.png`: 2×2 comparison, each panel exactly 800×450 source pixels. Open at 100% in an image viewer; do not fit-to-window for judging quality. This is a generated contact sheet, not a screenshot of an image editor; capture it at 100% for the brief's screenshot requirement.
- `experiment_report.md`: settings, observed visual differences, limitations, and a 100–150-word conclusion.
- `media_inventory.json`: hashes, sizes and dimensions of inherited media; licence provenance explicitly unverified.
- `storyboard.md`: eight-shot plan and recording script. It is a plan; no one has recorded the required voices yet.
- `integration_and_contributions.md`: factual change log and contribution verification table.
- `requirement_matrix.md`: outstanding Assignment 4 and End-term deliverables, with source page references.
- `performance_capture_protocol.md`: reproducible DevTools procedure and empty measurement form. No fabricated timings.

## Reproduce

Run `tools/build_a4_experiments.py` with Python + Pillow and ffmpeg installed. The local Codex bundled Python was used for this run. Input media is never overwritten. Output files are in `docs/a4/experiments/`. Decimal KB = bytes / 1000.

## Submission blockers

1. Team must establish permission/source/tool for inherited assets, or replace them with documented usable assets. No licence has been invented here.
2. Record actual 2–3-minute screen demo and each member's own voice. Generate and check full VTT against the final audio; the inherited 26.5-second VTT is not that evidence.
3. Capture actual DevTools Fast 4G before/after network measurements, screenshots and three-run End-term average.
4. Confirm each member's personal contribution. AI-generated code and documentation are not evidence that an individual personally produced them.
5. Compile final report PDF only after pending evidence is supplied. No finished report PDF is claimed by this pack.
