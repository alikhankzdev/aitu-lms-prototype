"""Reproduce actual A4 measurements; never treats a re-encoded WebP as a raw original."""
from pathlib import Path
import csv, hashlib, json, subprocess, wave
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'a4'
EXP = OUT / 'experiments'
EXP.mkdir(parents=True, exist_ok=True)
source = ROOT / 'static' / 'course_ict.webp'
im = Image.open(source).convert('RGB')
variants = [('image.png', 'PNG', {}), ('image-jpeg80.jpg', 'JPEG', {'quality':80}), ('image-jpeg40.jpg', 'JPEG', {'quality':40}), ('image-webp80.webp', 'WEBP', {'quality':80, 'method':6})]
rows=[]
for name, fmt, settings in variants:
    target=EXP/name
    im.save(target, fmt, **settings)
    rows.append({'file':name,'format':fmt,'settings':json.dumps(settings),'dimensions':f'{im.width}x{im.height}','bytes':target.stat().st_size,'KB_decimal':round(target.stat().st_size/1000,3),'quality_review':'Compare visually at native size; ratings in report are observations, not a perceptual metric.'})
canvas=Image.new('RGB',(im.width*2, (im.height+40)*2),'white')
d=ImageDraw.Draw(canvas)
for i,(name,fmt,settings) in enumerate(variants):
    x=(i%2)*im.width; y=(i//2)*(im.height+40)
    d.text((x+12,y+12),f'{name} - {rows[i]["bytes"]} bytes - native {im.width}x{im.height}',fill='black')
    canvas.paste(Image.open(EXP/name).convert('RGB'),(x,y+40))
canvas.save(EXP/'side-by-side-native.png')
# Repeat the project's one-second non-speech chime with silence into an exact ten-second clip.
with wave.open(str(ROOT/'static'/'notification.wav'),'rb') as src:
    params=src.getparams(); sound=src.readframes(src.getnframes())
framebytes=params.nchannels*params.sampwidth
silence=b'\0'*(params.framerate*framebytes-len(sound))
with wave.open(str(EXP/'audio-10s-pcm.wav'),'wb') as dst:
    dst.setparams(params); dst.writeframes((sound+silence)*10)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(EXP/'audio-10s-pcm.wav'),'-c:a','aac','-b:a','96k',str(EXP/'audio-10s-aac96.m4a')],check=True)
for name in ['audio-10s-pcm.wav','audio-10s-aac96.m4a']:
    rows.append({'file':name,'format':'WAV/PCM' if name.endswith('wav') else 'M4A/AAC','settings':'44100 Hz mono 16-bit PCM' if name.endswith('wav') else 'AAC target 96 kbit/s, mono 44100 Hz','dimensions':'10.000 seconds','bytes':(EXP/name).stat().st_size,'KB_decimal':round((EXP/name).stat().st_size/1000,3),'quality_review':'Non-speech chime; listen to both. Not narration.'})
with (OUT/'measurements.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
inventory=[]
for f in sorted((ROOT/'static').glob('*')):
    if f.suffix not in {'.webp','.svg','.wav','.vtt'}:continue
    dimensions='vector' if f.suffix=='.svg' else '26.5 s caption timeline, no matching speech' if f.suffix=='.vtt' else '1 second, PCM mono 44100 Hz' if f.suffix=='.wav' else str(Image.open(f).size)
    inventory.append({'file':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'dimensions_or_duration':dimensions,'source':'Inherited teammate ZIP; author/tool not independently confirmed','license':'UNVERIFIED - ask creator for source and permission; do not claim own work','sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(OUT/'media_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
(OUT/'experiment_metadata.json').write_text(json.dumps({'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_is_already_lossy_webp':True,'image_size':im.size,'side_by_side_native_pixel_size':canvas.size,'note':'PNG is a lossless decode of inherited WebP. It cannot restore information lost in the inherited source. These measurements are an A2 encoding comparison, not DevTools network measurements.'},indent=2))
print(json.dumps(rows,indent=2))
