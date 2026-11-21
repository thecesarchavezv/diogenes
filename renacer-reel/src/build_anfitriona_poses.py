"""Renacer hostess reel, pose-to-pose version.

0-8 s   : forest welcome, full illustrated frames (her world, like the garden)
8-31 s  : real garden photos, background-removed poses swapped on the beat
31-36 s : outro with seal and contact line
"""
import html
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
W, H, DUR = 1080, 1920, 36.0
BEAT = 0.5
els, js = [], []
uid = [0]
FLASH = []


def nid(p):
    uid[0] += 1
    return f"{p}{uid[0]}"


def words(text):
    return " ".join(f'<span class="wd">{html.escape(w)}</span>' for w in text.split(" "))


def full_image(src, start, dur, track, kb, pos="50% 50%", dim=0.0, fade=0.3):
    i = nid("ph")
    els.append(
        f'<div id="{i}" class="clip photo" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{track}">'
        f'<div class="pw" id="{i}w"><img src="{src}" id="{i}i" style="object-position:{pos}" alt=""></div>'
        f'<div class="shade" style="opacity:{dim}"></div><div class="grad"></div></div>'
    )
    s0, s1, x0, x1, y0, y1 = kb
    js.append(f'tl.fromTo("#{i}i",{{scale:{s0},x:{x0},y:{y0}}},{{scale:{s1},x:{x1},y:{y1},duration:{dur:.3f},ease:"none"}},{start:.3f});')
    js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:{fade},ease:"power2.out"}},{start:.3f});')
    return i


def bubble(start, dur, text, sub=None, variant=""):
    i = nid("bb")
    subhtml = "".join(f'<div class="bsub">{html.escape(x)}</div>' for x in sub.split("|")) if sub else ""
    els.append(
        f'<div id="{i}" class="clip bubblewrap" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{6 + (uid[0] % 2)}">'
        f'<div class="bubble {variant}" id="{i}b"><div class="btext">{words(text)}</div>{subhtml}<div class="tail"></div></div></div>'
    )
    js.append(f'tl.fromTo("#{i}b",{{scale:0,rotation:-8}},{{scale:1,rotation:0,duration:0.4,ease:"back.out(2.2)"}},{start:.3f});')
    js.append(f'tl.from("#{i} .wd",{{y:30,opacity:0,duration:0.3,ease:"back.out(2)",stagger:0.07}},{start + 0.15:.3f});')
    if sub:
        js.append(f'tl.from("#{i} .bsub",{{opacity:0,y:16,duration:0.3,stagger:0.12}},{start + 0.6:.3f});')
    js.append(f'tl.to("#{i}b",{{scale:0.6,opacity:0,duration:0.2,ease:"power2.in"}},{start + dur - 0.2:.3f});')


def chip(start, dur, n, label):
    i = nid("ch")
    els.append(f'<div id="{i}" class="clip chipwrap" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="8">'
               f'<div class="chip" id="{i}c"><span class="cn">{n}</span><span class="cl">{html.escape(label)}</span></div></div>')
    js.append(f'tl.from("#{i}c",{{x:-500,duration:0.45,ease:"power4.out"}},{start + 0.1:.3f});')
    js.append(f'tl.to("#{i}c",{{x:-500,duration:0.25,ease:"power2.in"}},{start + dur - 0.25:.3f});')


def _even(n):
    n = max(2, int(n))
    return n if n % 2 == 0 else n - 1


# ------------------------------------------------------------------ base
els.append('<div id="bg" class="clip full" data-start="0" data-duration="36" data-track-index="0"></div>')

# ================================================================== 0-8 FOREST WELCOME
forest = [
    ("u04-tronco", 0.0, 2.0, (1.18, 1.08, 0, 0, 30, 0)),
    ("u01-saludo-sien", 2.0, 2.0, (1.06, 1.16, 0, 0, 0, -20)),
    ("v06-manos-abiertas", 4.0, 2.0, (1.18, 1.06, 0, 0, 0, 0)),
    ("u10-camina-saluda", 6.0, 2.0, (1.0, 1.22, 0, 0, 0, -60)),
]
for k, (name, st, du, kb) in enumerate(forest):
    full_image(f"assets/img/bosque/{name}.jpg", st, du, 1 + k % 2, kb, fade=0.2 if k else 0.6)
    if k:
        FLASH.append((st, 0.35))
bubble(0.5, 3.4, "¡hola! bienvenidos a renacer", variant="low")
bubble(4.2, 3.4, "pásale, estás en tu casa", "aquí empieza tu celebración", variant="low")
# 7.75-8.0: music gap -> warm "door opening" light
els.append('<div id="door" class="clip full" data-start="7.6" data-duration="0.9" data-track-index="9"><div id="door-l" class="door"></div></div>')
js.append('tl.fromTo("#door-l",{scale:0,opacity:0.0},{scale:1,opacity:1,duration:0.35,ease:"power2.in"},7.6);')
js.append('tl.to("#door-l",{opacity:0,duration:0.5,ease:"power2.out"},8.0);')

# ================================================================== 8-31 GARDEN WITH POSES
POSES = {  # name: (display height px, bottom y, center x)
    "u03-brazos-arriba": (1075, 1885, 245), "u05-caminando": (1000, 1885, 245),
    "u06-pensativa": (1035, 1885, 245), "u07-carcajada": (990, 1885, 245),
    "u09-sorpresa-mano": (1010, 1885, 245), "u10-camina-saluda": (1010, 1885, 245),
    "v01-binoculares": (910, 1930, 250), "v02-audifonos": (1000, 1885, 245),
    "v03-selfie": (910, 1930, 285), "v05-senala-sorpresa": (950, 1885, 245),
    "v06-manos-abiertas": (1000, 1885, 260), "v08-camina-senala": (1000, 1885, 245),
    "v10-camina-saluda": (1010, 1885, 245),
}
ASPECT = {"u03-brazos-arriba": 501, "u05-caminando": 425, "u06-pensativa": 367, "u07-carcajada": 468,
          "u09-sorpresa-mano": 479, "u10-camina-saluda": 456, "v01-binoculares": 537, "v02-audifonos": 399,
          "v03-selfie": 529, "v05-senala-sorpresa": 433, "v06-manos-abiertas": 569, "v08-camina-senala": 483,
          "v10-camina-saluda": 469}
imgs = []
for name, (h, bottom, cx) in POSES.items():
    w = round(h * ASPECT[name] / 1100)
    imgs.append(f'<img id="p-{name}" class="pose" src="assets/img/poses/{name}.png" '
                f'style="left:{cx - w // 2}px;top:{bottom - h}px;width:{w}px;height:{h}px" alt="">')
els.append(
    '<div id="host" class="clip full" data-start="8" data-duration="28" data-track-index="5">'
    '<div id="h-move" class="layer"><div id="h-shadow"></div><div id="h-hop" class="layer"><div id="h-bob" class="layer">'
    '<div id="h-tilt" class="layer"><div id="h-squash" class="layer">' + "".join(imgs) + '</div></div></div></div></div></div>'
)
js.append('tl.fromTo("#h-move",{x:-620},{x:0,duration:0.6,ease:"back.out(1.4)"},8.0);')
n_breath = _even(28 / 1.2)
js.append(f'tl.fromTo("#h-tilt",{{scaleY:1}},{{scaleY:1.012,duration:0.6,ease:"sine.inOut",yoyo:true,repeat:{n_breath - 1},immediateRender:false}},8.0);')

SCHEDULE = []  # (time, pose)
current = [None]


def pose(t, name, pop=True):
    if current[0]:
        js.append(f'tl.set("#p-{current[0]}",{{opacity:0}},{t:.3f});')
    js.append(f'tl.set("#p-{name}",{{opacity:1}},{t:.3f});')
    bleed = POSES[name][1] > 1900
    js.append(f'tl.set("#h-shadow",{{autoAlpha:{0 if bleed else 1}}},{t:.3f});')
    if pop and current[0]:
        js.append(f'tl.fromTo("#h-squash",{{scaleY:0.93,scaleX:1.05}},{{scaleY:1,scaleX:1,duration:0.3,ease:"back.out(2.5)",immediateRender:false}},{t:.3f});')
    current[0] = name


def hop(t, hgt=60):
    js.append(f'tl.fromTo("#h-hop",{{y:0}},{{y:-{hgt},duration:0.18,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-shadow",{{scale:1}},{{scale:0.7,duration:0.18,yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')


def walk(t, dur):
    n = _even(dur / 0.25)
    js.append(f'tl.fromTo("#h-bob",{{y:0}},{{y:-16,duration:0.125,ease:"sine.out",yoyo:true,repeat:{2 * n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-tilt",{{rotation:-2.2}},{{rotation:2.2,duration:0.25,ease:"sine.inOut",yoyo:true,repeat:{n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:0,duration:0.15}},{t + n * 0.25:.3f});')


def lean(t, dur, ang=4):
    js.append(f'tl.to("#h-tilt",{{rotation:{ang},duration:0.3,ease:"back.out(2)"}},{t:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:0,duration:0.3,ease:"power2.inOut"}},{t + dur - 0.3:.3f});')


def dance(t, dur):
    n = _even(dur / BEAT)
    js.append(f'tl.fromTo("#h-tilt",{{rotation:-5}},{{rotation:5,duration:{BEAT},ease:"sine.inOut",yoyo:true,repeat:{n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-bob",{{y:0}},{{y:-36,duration:{BEAT / 2},ease:"power2.out",yoyo:true,repeat:{2 * n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:0,duration:0.2}},{t + n * BEAT:.3f});')


# A · garden
full_image("assets/img/panoramica-noche.jpg", 8.0, 5.0, 1, (1.25, 1.25, 260, -260, 0, 0), dim=0.3)
chip(8.0, 5.0, "01", "el jardín")
pose(8.0, "v08-camina-senala", pop=False)
walk(8.0, 0.75)
bubble(8.5, 4.3, "te invito a conocer nuestro jardín", "entre encinos de décadas")
pose(10.5, "u05-caminando")
walk(10.5, 2.5)
FLASH.append((8.0, 0.9))

# B · dance floor
full_image("assets/img/pista-led.jpg", 13.0, 5.0, 2, (1.3, 1.1, 0, 0, 0, 0), dim=0.2)
chip(13.0, 5.0, "02", "la pista")
pose(13.0, "v05-senala-sorpresa")
lean(13.0, 2.0, 5)
bubble(13.3, 4.5, "aquí está la pista… ¡lista para bailar!")
for k in range(6):
    pose(15.0 + k * BEAT, "u03-brazos-arriba" if k % 2 == 0 else "v02-audifonos")
dance(15.0, 3.0)
FLASH.append((13.0, 0.45))

# C · grill
full_image("assets/img/parrilla-barra.jpg", 18.0, 2.25, 1, (1.25, 1.1, 0, 0, 0, 0), "40% 50%", dim=0.25)
full_image("assets/img/carne-asada.jpg", 20.25, 2.25, 2, (1.05, 1.25, 0, 0, 0, -40), "50% 40%", dim=0.3)
chip(18.0, 4.5, "03", "la parrilla")
pose(18.0, "u09-sorpresa-mano")
hop(18.05, 40)
bubble(18.3, 4.0, "y la parrilla siempre encendida", "el sabor de casa")
pose(20.25, "v03-selfie")
lean(20.25, 2.0, -3)
FLASH.extend([(18.0, 0.45), (20.25, 0.35)])

# D · corners
full_image("assets/img/arco-columnas.jpg", 22.5, 2.0, 1, (1.1, 1.28, 0, 0, 0, 0), "50% 45%", dim=0.25)
full_image("assets/img/escalera-luces.jpg", 24.5, 2.0, 2, (1.2, 1.2, 160, -160, 0, 0), dim=0.25)
chip(22.5, 4.0, "04", "los rincones")
pose(22.5, "v06-manos-abiertas")
bubble(22.8, 3.6, "espacios con historia y luz cálida", "como llegar a casa")
pose(24.5, "v01-binoculares")
lean(24.5, 2.0, 3)
FLASH.extend([(22.5, 0.45), (24.5, 0.35)])

# E · events
full_image("assets/img/kiosco-escalera.jpg", 26.5, 4.5, 1, (1.15, 1.3, 0, 0, 0, 0), "50% 55%", dim=0.5)
pose(26.5, "u07-carcajada")
bubble(26.7, 4.1, "ven a celebrar tus eventos", "como en casa, entre los árboles")
for k, ev in enumerate(["bodas", "xv años", "bautizos", "convivios"]):
    t = 26.9 + k * 0.85
    i = nid("ev")
    els.append(f'<div id="{i}" class="clip evwrap" data-start="{t:.3f}" data-duration="{31 - t:.3f}" data-track-index="9">'
               f'<div class="evcard" id="{i}c" style="top:{250 + k * 130}px">{html.escape(ev)}</div></div>')
    js.append(f'tl.fromTo("#{i}c",{{x:900,rotation:12}},{{x:0,rotation:{(-3, 2, -2, 3)[k]},duration:0.45,ease:"back.out(1.7)"}},{t:.3f});')
    js.append(f'tl.to("#{i}c",{{x:-1100,duration:0.3,ease:"power2.in"}},30.6);')
    hop(t, 50)
pose(30.0, "u03-brazos-arriba")
hop(30.0, 70)
FLASH.extend([(26.5, 0.5), (30.0, 0.3)])

# ================================================================== 31-36 OUTRO
els.append('<div id="outro-bg" class="clip full outro-bg" data-start="31" data-duration="5" data-track-index="3"></div>')
js.append('tl.fromTo("#outro-bg",{opacity:0},{opacity:1,duration:0.35},31.0);')
els.append('<div id="seal" class="clip logo" data-start="31" data-duration="5" data-track-index="4"><img id="seal-i" src="assets/img/sello-dorado.png" alt=""></div>')
js.append('tl.fromTo("#seal-i",{scale:0.3,rotation:-120,opacity:0},{scale:1,rotation:0,opacity:1,duration:0.7,ease:"back.out(1.5)"},31.1);')
js.append('tl.to("#seal-i",{rotation:10,duration:4,ease:"sine.inOut"},31.8);')
pose(31.0, "u06-pensativa")
bubble(31.4, 4.5, "¿qué estás celebrando?", "escríbenos por whatsapp|san josé el vidrio, edo. de méxico")
pose(33.5, "v10-camina-saluda")
hop(33.5, 50)
lean(33.6, 2.2, -3)
FLASH.append((31.0, 0.5))

# flash + audio
els.append('<div id="flash" class="clip full" data-start="0" data-duration="36" data-track-index="10"></div>')
for t, a in sorted(FLASH):
    js.append(f'tl.fromTo("#flash",{{opacity:{a}}},{{opacity:0,duration:0.3,ease:"power2.out",immediateRender:false}},{t:.3f});')
els.append('<audio id="bgm" src="assets/music.wav" data-start="0" data-duration="36" data-track-index="11" data-volume="1"></audio>')

CSS = """
@font-face{font-family:'Josefin Sans';font-weight:300;src:url(assets/fonts/josefin-sans-latin-300-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:400;src:url(assets/fonts/josefin-sans-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;src:url(assets/fonts/cormorant-garamond-latin-500-italic.woff2) format('woff2')}
html,body{margin:0;background:#1A2214}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Josefin Sans',sans-serif;color:#F0EBE0}
.full,.layer{position:absolute;left:0;top:0;width:1080px;height:1920px}
#bg{background:radial-gradient(ellipse at 50% 40%,#2b3822 0%,#1A2214 60%,#10160c 100%)}
.outro-bg{background:radial-gradient(ellipse at 50% 35%,#2b3822 0%,#1A2214 65%,#0f150b 100%)}
#flash{background:#F0EBE0;opacity:0}
.door{position:absolute;left:-460px;top:-60px;width:2000px;height:2040px;border-radius:50%;background:radial-gradient(ellipse at center,#fff6e0 0%,#F0EBE0 45%,rgba(240,235,224,0) 70%);display:block}
.photo{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden}
.photo .pw,.photo img{position:absolute;inset:0;width:1080px;height:1920px}
.photo img{object-fit:cover;display:block}
.photo .shade{position:absolute;inset:0;background:#1A2214}
.photo .grad{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,34,20,.45) 0%,rgba(26,34,20,0) 18%,rgba(26,34,20,0) 55%,rgba(26,34,20,.7) 88%,rgba(26,34,20,.85) 100%)}
#h-tilt,#h-squash{transform-origin:245px 1885px}
.pose{position:absolute;display:block;opacity:0;filter:drop-shadow(0 8px 20px rgba(0,0,0,.4))}
#h-shadow{position:absolute;left:95px;top:1860px;width:300px;height:50px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 70%);display:block}
.logo{position:absolute;inset:0;width:1080px;height:1920px;display:flex;justify-content:center;align-items:flex-start;padding-top:250px;box-sizing:border-box}
.logo img{width:460px;height:460px;border-radius:50%;display:block}
.bubblewrap,.chipwrap,.evwrap{position:absolute;inset:0;width:1080px;height:1920px}
.bubble{position:absolute;left:470px;top:790px;width:580px;box-sizing:border-box;padding:40px 44px 42px;background:#F0EBE0;color:#1A2214;border-radius:44px;transform-origin:8% 100%;box-shadow:0 18px 50px rgba(0,0,0,.35);display:block}
.bubble.low{left:150px;top:1440px;width:780px;transform-origin:50% 0%;text-align:center}
.btext{font-size:58px;font-weight:400;line-height:1.14}
.wd{display:inline-block}
.bsub{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:42px;color:#5A4818;margin-top:10px;line-height:1.1;white-space:nowrap}
.tail{position:absolute;left:-26px;bottom:44px;width:0;height:0;border-top:22px solid transparent;border-bottom:22px solid transparent;border-right:44px solid #F0EBE0}
.low .tail{left:50%;top:-40px;bottom:auto;margin-left:-22px;border-left:22px solid transparent;border-right:22px solid transparent;border-bottom:44px solid #F0EBE0;border-top:none}
.chip{position:absolute;left:0;top:250px;padding:20px 40px 16px 60px;background:#1A2214;border:3px solid #C4B480;border-left:none;border-radius:0 60px 60px 0;display:flex;gap:22px;align-items:baseline}
.cn{font-size:40px;color:#C4B480;font-weight:300;letter-spacing:.1em}
.cl{font-size:52px;font-weight:300;letter-spacing:.08em;color:#F0EBE0}
.evcard{position:absolute;right:70px;padding:20px 46px 14px;background:#C4B480;color:#1A2214;font-size:72px;font-weight:400;letter-spacing:.04em;border-radius:20px;box-shadow:0 14px 40px rgba(0,0,0,.4);display:block}
"""

doc = f"""<!doctype html>
<html lang="es"><head><meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>renacer · anfitriona</title>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-width="{W}" data-height="{H}" data-duration="{DUR}" data-fps="30">
{chr(10).join(els)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body></html>
"""
doc = re.sub(r'<div id="([^"]+)" class="clip([^"]*)"([^>]*?)data-track-index="(\d+)"',
             lambda m: f'<div id="{m.group(1)}" class="clip{m.group(2)}"{m.group(3)}data-track-index="{m.group(4)}" style="z-index:{m.group(4)}"', doc)
OUT.write_text(doc, encoding="utf-8")
print("wrote", OUT, len(els), "clips", len(js), "tweens")
