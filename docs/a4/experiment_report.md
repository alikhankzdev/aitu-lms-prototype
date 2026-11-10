# A2. Measured encoding experiment

Source: inherited `static/course_ict.webp`, 800×450, SHA-256 recorded in `experiment_metadata.json`. This is already a compressed WebP, so PNG is a lossless representation of its decoded pixels, not the original artwork. Re-encoding cannot restore lost quality. The source contains small rasterised labels; this makes compression effects visible, but the final site should keep meaningful text in HTML.

Tools: Pillow through bundled Python 3.12; ffmpeg AAC encoder. Reproduction: `tools/build_a4_experiments.py`.

| File | Setting | Resolution/duration | Bytes | Decimal KB | Observed quality |
|---|---|---|---:|---:|---|
| image.png | PNG lossless decode | 800×450 | 175302 | 175.302 | Sharp relative to decoded input; inherited artefacts remain |
| image-jpeg80.jpg | JPEG quality 80 | 800×450 | 61842 | 61.842 | Acceptable; slight ringing around grid/text |
| image-jpeg40.jpg | JPEG quality 40 | 800×450 | 37038 | 37.038 | Poor for small text and thin grid; visible block/ringing effects |
| image-webp80.webp | WebP quality 80, method 6 | 800×450 | 18426 | 18.426 | Acceptable for a decorative cover; do not rely on embedded fine text |
| audio-10s-pcm.wav | PCM 16-bit mono 44100 Hz | 10.000 seconds | 882044 | 882.044 | Source/reference; no speech |
| audio-10s-aac96.m4a | AAC target 96 kbit/s | 10 seconds nominal | 123287 | 123.287 | Requires human A/B listening; no subjective claim recorded |

Audio method: repeat the project's existing one-second chime ten times. It is a real ten-second project-derived audio clip, not a recording of a participant. The source has exactly 441000 samples; ffprobe confirms the AAC container duration is 10.000000 seconds, mono 44100 Hz, actual container bitrate 98629 bit/s (target encoder bitrate 96000 bit/s). This does not satisfy the team's narration requirement. Listen to both files before filling any subjective audio judgement.

Visual evidence: `experiments/side-by-side-native.png` shows all four images at native pixel dimensions. Quality labels above are observations from that sheet, not a metric or a user test. Capture the image viewer at 100% to meet the brief's screenshot wording.

## Conclusion (132 words)

For course-cover delivery, our measured WebP quality-80 export is the preferred raster version: it occupies 18.426 KB, compared with 61.842 KB for JPEG quality 80 and 175.302 KB for PNG. This saves about 89.5% against the PNG encoding of the same decoded pixels. JPEG quality 40 reduces size to 37.038 KB, but the grid and small lettering visibly deteriorate, so it is unsuitable for information-bearing screenshots. We will retain PNG for evidence screenshots and SVG for trusted logos and icons. The ten-second PCM clip uses 882.044 KB; AAC at the selected setting uses 123.287 KB, about 86.0% less. AAC therefore suits a delivery audio track after listening checks, while PCM remains an editing reference. These file measurements do not establish page-load improvements or recover quality already lost in the inherited WebP source.
