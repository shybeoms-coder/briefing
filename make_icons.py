#!/usr/bin/env python3
# 순수 표준 라이브러리만으로 앱 아이콘 PNG 생성 (Liner풍 민트그린)
import zlib, struct, math

GREEN = (0x00, 0xc4, 0x71)
WHITE = (0xff, 0xff, 0xff)

def make(size, path):
    S = size
    sc = S / 512.0
    buf = bytearray(S * S * 4)  # RGBA, 초기 투명

    def idx(x, y): return (y * S + x) * 4

    def blend(x, y, rgb, a):
        if x < 0 or y < 0 or x >= S or y >= S: return
        i = idx(x, y)
        ba = buf[i+3] / 255.0
        na = a + ba * (1 - a)
        if na <= 0: return
        for k in range(3):
            buf[i+k] = int((rgb[k]*a + buf[i+k]*ba*(1-a)) / na)
        buf[i+3] = int(na * 255)

    def rrect_inside(px, py, x, y, w, h, r):
        if px < x or py < y or px > x+w or py > y+h: return False
        rx0, rx1 = x+r, x+w-r
        ry0, ry1 = y+r, y+h-r
        cx = min(max(px, rx0), rx1)
        cy = min(max(py, ry0), ry1)
        return (px-cx)**2 + (py-cy)**2 <= r*r

    def fill_rrect(x, y, w, h, r, rgb, a=1.0):
        x, y, w, h, r = x*sc, y*sc, w*sc, h*sc, r*sc
        for py in range(int(y-1), int(y+h+2)):
            for px in range(int(x-1), int(x+w+2)):
                # 안티앨리어싱: 4x 슈퍼샘플
                hits = 0
                for ox in (0.25, 0.75):
                    for oy in (0.25, 0.75):
                        if rrect_inside(px+ox, py+oy, x, y, w, h, r): hits += 1
                if hits: blend(px, py, rgb, a * hits/4.0)

    def dist_seg(px, py, ax, ay, bx, by):
        dx, dy = bx-ax, by-ay
        L2 = dx*dx + dy*dy
        t = 0 if L2 == 0 else max(0, min(1, ((px-ax)*dx + (py-ay)*dy)/L2))
        cx, cy = ax+t*dx, ay+t*dy
        return math.hypot(px-cx, py-cy)

    def thick_line(pts, width, rgb, a=1.0):
        w = width*sc/2.0
        pts = [(x*sc, y*sc) for x, y in pts]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        for py in range(int(min(ys)-w-1), int(max(ys)+w+2)):
            for px in range(int(min(xs)-w-1), int(max(xs)+w+2)):
                hits = 0
                for ox in (0.25, 0.75):
                    for oy in (0.25, 0.75):
                        d = min(dist_seg(px+ox, py+oy, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])
                                for i in range(len(pts)-1))
                        if d <= w: hits += 1
                if hits: blend(px, py, rgb, a*hits/4.0)

    def fill_circle(cx, cy, r, rgb, a=1.0):
        cx, cy, r = cx*sc, cy*sc, r*sc
        for py in range(int(cy-r-1), int(cy+r+2)):
            for px in range(int(cx-r-1), int(cx+r+2)):
                hits = 0
                for ox in (0.25, 0.75):
                    for oy in (0.25, 0.75):
                        if (px+ox-cx)**2 + (py+oy-cy)**2 <= r*r: hits += 1
                if hits: blend(px, py, rgb, a*hits/4.0)

    # 배경 라운드 사각형
    fill_rrect(0, 0, 512, 512, 114, GREEN, 1.0)
    # 추세선 (반투명)
    thick_line([(132,268),(256,196),(380,132)], 22, WHITE, 0.55)
    # 막대 3개
    fill_rrect(120,300,48,92,14, WHITE)
    fill_rrect(232,244,48,148,14, WHITE)
    fill_rrect(344,160,48,232,14, WHITE)
    # 끝점 원
    fill_circle(380,132,20, WHITE)

    # PNG 인코딩
    raw = bytearray()
    for y in range(S):
        raw.append(0)
        raw += buf[y*S*4:(y+1)*S*4]
    comp = zlib.compress(bytes(raw), 9)
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag+data) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", S, S, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    print("wrote", path, S, "x", S)

make(180, "/Users/bums/Downloads/test/web/icon-180.png")
make(512, "/Users/bums/Downloads/test/web/icon-512.png")
print("DONE")
