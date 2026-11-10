"""Render the project's simple A monogram as PNG without external dependencies."""
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'static'

def inside(x, y, polygon):
    result = False
    previous = polygon[-1]
    for current in polygon:
        a, b = previous, current
        if (a[1] > y) != (b[1] > y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            result = not result
        previous = current
    return result

def chunk(kind, data):
    return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))

for size in (192, 512):
    raw = bytearray()
    for row in range(size):
        raw.append(0)
        for col in range(size):
            x, y = (col+.5)*512/size, (row+.5)*512/size
            color = (17, 36, 64)
            if inside(x, y, [(146,340),(224,172),(288,172),(366,340),(309,340),(296,308),(216,308),(203,340)]) and not inside(x,y,[(233,264),(279,264),(256,207)]):
                color = (255,255,255)
            if 176 <= x < 336 and 368 <= y < 384:
                color = (223,183,89)
            raw.extend(color)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR',struct.pack('!IIBBBBB',size,size,8,2,0,0,0)) + chunk(b'IDAT',zlib.compress(raw,9)) + chunk(b'IEND',b'')
    (ROOT / f'pwa-icon-{size}.png').write_bytes(data)
