# A1. Format comparison

Size is content- and setting-dependent. Entries below describe expected relative size, not a fabricated universal KB value. Container and codec are named together where relevant.

| Format / combination | Type | Compression | Transparency / animation | Typical relative size | Browser/device considerations | Project use |
|---|---|---|---|---|---|---|
| PNG | Image | Lossless | Alpha; APNG animation variant | Larger for photos; useful for flat UI | Broad support | Lossless screenshots and experiment reference |
| JPEG | Image | Lossy | No alpha or animation | Adjustable by quality | Broad support | Photographic course covers; avoid fine labels |
| WebP | Image | Lossy or lossless | Alpha and animation | Often compact; measure actual content | Modern browsers | Course cover delivery |
| SVG | Image/vector | Vector description; optional transport compression | Alpha; animation possible | Small for simple geometry; complexity increases size | Modern browsers; sanitise untrusted content | Trusted local logo/icons |
| WAV + PCM | Audio | Uncompressed PCM in container | Not applicable | Large; predictable from sample rate/depth/channels | Common PCM browser support | Editing/reference audio |
| MP3 | Audio | Lossy | Not applicable | Controlled by bitrate | Broad playback support | Compact notification/narration fallback |
| M4A/MP4 + AAC | Audio | Lossy AAC | Not applicable | Controlled by bitrate | Widely supported; platform codecs matter | Final demo audio track |
| MP4 + H.264/AAC | Video | Usually lossy tracks | No portable alpha assumption | Controlled by resolution, bitrate and duration | Broad practical support | Required submission export |
| WebM + VP9/Opus | Video | Usually lossy tracks | Alpha depends on encoder/playback | Content/settings determine savings | Verify target browsers | Optional web delivery alternative |
| MOV + ProRes/PCM | Video | Common editing combination, intraframe video | Alpha only with suitable ProRes profile | Usually much larger editing master | Not a dependable browser delivery choice | Optional editing master, not LMS upload |

A container packages tracks and metadata, while a codec encodes and decodes the image or sound carried by those tracks; MP4 can contain H.264 video and AAC audio.

References: [MDN image guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types), [WebP specification](https://www.rfc-editor.org/rfc/rfc9649.html), [MDN containers](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Containers), [MDN audio codecs](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Audio_codecs). Checked 31 October 2026. Actual browser testing in this project remains separate evidence.
