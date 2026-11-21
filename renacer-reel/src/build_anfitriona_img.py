"""Second Renacer reel: an original flat-illustration hostess invites viewers
through the garden. Text bubbles + music (no voice). 36 s, 120 BPM grid.
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


def nid(p):
    uid[0] += 1
    return f"{p}{uid[0]}"


def words(text):
    return " ".join(f'<span class="wd">{html.escape(w)}</span>' for w in text.split(" "))


def photo(img, start, dur, track, kb, pos="50% 50%", dim=0.25):
    i = nid("ph")
    els.append(
        f'<div id="{i}" class="clip photo" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{track}">'
        f'<div class="pw" id="{i}w"><img src="assets/img/{img}" id="{i}i" style="object-position:{pos}" alt=""></div>'
        f'<div class="shade" style="opacity:{dim}"></div><div class="grad"></div></div>'
    )
    s0, s1, x0, x1, y0, y1 = kb
    js.append(f'tl.fromTo("#{i}i",{{scale:{s0},x:{x0},y:{y0}}},{{scale:{s1},x:{x1},y:{y1},duration:{dur:.3f},ease:"none"}},{start:.3f});')
    js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.3,ease:"power2.out"}},{start:.3f});')
    return i


FLASH = []

# ------------------------------------------------------------------ the hostess (original design)
SKIN, SKIN_D = "#C98E6B", "#B07A58"
HAIR = "#2B1D14"
DRESS, DRESS_D = "#4A6236", "#3A4E2A"
HOST = f'''
<svg id="host-svg" viewBox="0 0 400 900" class="hostsvg">
 <ellipse cx="200" cy="884" rx="130" ry="14" fill="#000" opacity=".28"/>
 <g id="h-hop"><g id="h-breath">
  <g id="leg-l"><path d="M168 600 L162 850" stroke="{SKIN}" stroke-width="30" stroke-linecap="round"/>
   <ellipse cx="156" cy="862" rx="30" ry="14" fill="#5A4818"/></g>
  <g id="leg-r"><path d="M232 600 L238 850" stroke="{SKIN}" stroke-width="30" stroke-linecap="round"/>
   <ellipse cx="244" cy="862" rx="30" ry="14" fill="#5A4818"/></g>
  <path d="M200 70 C110 70 118 230 132 300 L268 300 C282 230 290 70 200 70 Z" fill="{HAIR}"/>
  <g id="arm-l"><path d="M150 312 C128 360 124 430 132 505" stroke="{SKIN}" stroke-width="30" stroke-linecap="round" fill="none"/>
   <path d="M152 300 C130 316 124 350 126 372 L166 372 Z" fill="{DRESS}"/>
   <circle cx="133" cy="514" r="19" fill="{SKIN}"/></g>
  <rect x="186" y="250" width="28" height="56" rx="10" fill="{SKIN_D}"/>
  <path d="M140 304 Q200 284 260 304 L304 652 Q200 684 96 652 Z" fill="{DRESS}"/>
  <path d="M120 470 Q200 488 280 470 L304 652 Q200 684 96 652 Z" fill="{DRESS_D}" opacity=".55"/>
  <path d="M168 300 Q200 336 232 300 Q200 318 168 300 Z" fill="#F0EBE0"/>
  <rect x="122" y="440" width="156" height="16" rx="8" fill="#C4B480"/>
  <g transform="translate(222 338) scale(.9)"><path d="M10 0 Q16 0 17 5 Q22 9 18 14 Q21 20 16 24 Q14 30 10 32 Q6 30 4 24 Q-1 20 2 14 Q-2 9 3 5 Q4 0 10 0 Z" fill="#C4B480"/>
   <line x1="10" y1="2" x2="10" y2="38" stroke="#C4B480" stroke-width="2.4" stroke-linecap="round"/></g>
  <g id="arm-r"><path d="M250 312 C272 360 276 430 268 505" stroke="{SKIN}" stroke-width="30" stroke-linecap="round" fill="none"/>
   <path d="M248 300 C270 316 276 350 274 372 L234 372 Z" fill="{DRESS}"/>
   <circle cx="267" cy="514" r="19" fill="{SKIN}"/></g>
  <g id="head">
   <ellipse cx="136" cy="206" rx="12" ry="16" fill="{SKIN_D}"/><ellipse cx="264" cy="206" rx="12" ry="16" fill="{SKIN_D}"/>
   <ellipse cx="200" cy="196" rx="64" ry="74" fill="{SKIN}"/>
   <circle cx="200" cy="96" r="36" fill="{HAIR}"/>
   <path d="M136 186 C134 120 170 112 200 112 C238 112 268 124 264 186 C246 150 214 140 190 132 C176 154 158 170 136 186 Z" fill="{HAIR}"/>
   <circle cx="138" cy="226" r="6" fill="#C4B480"/><circle cx="262" cy="226" r="6" fill="#C4B480"/>
   <path d="M166 180 Q178 172 190 178" stroke="{HAIR}" stroke-width="4" fill="none" stroke-linecap="round"/>
   <path d="M210 178 Q222 172 234 180" stroke="{HAIR}" stroke-width="4" fill="none" stroke-linecap="round"/>
   <g id="eyes"><ellipse cx="178" cy="202" rx="7.5" ry="9.5" fill="#1A2214"/><ellipse cx="222" cy="202" rx="7.5" ry="9.5" fill="#1A2214"/>
    <circle cx="180.5" cy="198.5" r="2.4" fill="#fff"/><circle cx="224.5" cy="198.5" r="2.4" fill="#fff"/></g>
   <circle cx="164" cy="226" r="10" fill="#E07A6A" opacity=".45"/><circle cx="236" cy="226" r="10" fill="#E07A6A" opacity=".45"/>
   <path id="mouth-smile" d="M184 234 Q200 250 216 234" stroke="#6A2A24" stroke-width="4.5" fill="none" stroke-linecap="round"/>
   <path id="mouth-open" d="M184 232 Q200 262 216 232 Q200 238 184 232 Z" fill="#7A2E2A" opacity="0"/>
  </g>
 </g></g>
</svg>'''

# host clip spans the whole video; wrapper #host-move carries x/y entrances
els.append(f'<div id="host" class="clip hostclip" data-start="0" data-duration="{DUR}" data-track-index="5"><div id="h-move"><div id="h-shadow"></div><div id="h-hop"><div id="h-bob"><div id="h-tilt"><div id="h-squash"><img id="h-img" src="assets/img/anfitriona-host.png" alt=""></div></div></div></div></div></div>')

# pivots (svgOrigin, in viewBox coords)
O_ARM_L, O_ARM_R = "150 312", "250 312"
O_LEG_L, O_LEG_R = "168 600", "232 600"


def talk(t, dur):
    n = int(dur / 0.16)
    n = n if n % 2 == 1 else n - 1  # odd yoyo count -> ends closed
    js.append(f'tl.fromTo("#mouth-open",{{opacity:0}},{{opacity:1,duration:0.08,ease:"steps(1)",yoyo:true,repeat:{n},immediateRender:false}},{t:.3f});')


def blink(t):
    js.append(f'tl.fromTo("#eyes",{{scaleY:1}},{{scaleY:0.1,svgOrigin:"200 202",duration:0.07,yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')


def wave(t, dur=1.6):
    js.append(f'tl.to("#arm-l",{{rotation:150,svgOrigin:"{O_ARM_L}",duration:0.3,ease:"back.out(1.6)"}},{t:.3f});')
    n = int((dur - 0.6) / 0.22)
    n = n if n % 2 == 0 else n - 1
    js.append(f'tl.fromTo("#arm-l",{{rotation:150}},{{rotation:120,svgOrigin:"{O_ARM_L}",duration:0.22,ease:"sine.inOut",yoyo:true,repeat:{n},immediateRender:false}},{t + 0.3:.3f});')
    js.append(f'tl.to("#arm-l",{{rotation:0,svgOrigin:"{O_ARM_L}",duration:0.3,ease:"power2.inOut"}},{t + dur - 0.3:.3f});')


def point(t, dur=2.0, angle=-115):
    js.append(f'tl.to("#arm-r",{{rotation:{angle},svgOrigin:"{O_ARM_R}",duration:0.3,ease:"back.out(1.8)"}},{t:.3f});')
    js.append(f'tl.to("#arm-r",{{rotation:{angle + 8},svgOrigin:"{O_ARM_R}",duration:0.25,ease:"sine.inOut",yoyo:true,repeat:1}},{t + 0.5:.3f});')
    js.append(f'tl.to("#arm-r",{{rotation:0,svgOrigin:"{O_ARM_R}",duration:0.3,ease:"power2.inOut"}},{t + dur - 0.3:.3f});')


def both_arms_up(t, dur=1.4):
    js.append(f'tl.to("#arm-l",{{rotation:140,svgOrigin:"{O_ARM_L}",duration:0.3,ease:"back.out(1.6)"}},{t:.3f});')
    js.append(f'tl.to("#arm-r",{{rotation:-140,svgOrigin:"{O_ARM_R}",duration:0.3,ease:"back.out(1.6)"}},{t:.3f});')
    js.append(f'tl.to("#arm-l",{{rotation:0,svgOrigin:"{O_ARM_L}",duration:0.3,ease:"power2.inOut"}},{t + dur - 0.3:.3f});')
    js.append(f'tl.to("#arm-r",{{rotation:0,svgOrigin:"{O_ARM_R}",duration:0.3,ease:"power2.inOut"}},{t + dur - 0.3:.3f});')


def walk(t, dur):
    steps = int(dur / 0.25)
    steps = steps if steps % 2 == 0 else steps - 1
    js.append(f'tl.fromTo("#leg-l",{{rotation:-16}},{{rotation:16,svgOrigin:"{O_LEG_L}",duration:0.25,ease:"sine.inOut",yoyo:true,repeat:{steps - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#leg-r",{{rotation:16}},{{rotation:-16,svgOrigin:"{O_LEG_R}",duration:0.25,ease:"sine.inOut",yoyo:true,repeat:{steps - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-hop",{{y:0}},{{y:-14,duration:0.125,ease:"sine.out",yoyo:true,repeat:{2 * steps - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.to(["#leg-l","#leg-r"],{{rotation:0,svgOrigin:"168 600",duration:0.15}},{t + steps * 0.25:.3f});')


def dance(t, dur):
    n = int(dur / BEAT)
    n = n if n % 2 == 0 else n - 1
    js.append(f'tl.fromTo("#h-breath",{{rotation:-5}},{{rotation:5,svgOrigin:"200 880",duration:{BEAT},ease:"sine.inOut",yoyo:true,repeat:{n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-hop",{{y:0}},{{y:-26,duration:{BEAT / 2},ease:"power2.out",yoyo:true,repeat:{2 * n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.to("#h-breath",{{rotation:0,svgOrigin:"200 880",duration:0.2}},{t + n * BEAT:.3f});')


def hop(t):
    js.append(f'tl.fromTo("#h-hop",{{y:0}},{{y:-60,duration:0.18,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')


def bubble(start, dur, text, sub=None, side="right"):
    i = nid("bb")
    subhtml = "".join(f'<div class="bsub">{html.escape(x)}</div>' for x in sub.split("|")) if sub else ""
    els.append(
        f'<div id="{i}" class="clip bubblewrap" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{6 + (uid[0] % 2)}">'
        f'<div class="bubble" id="{i}b"><div class="btext">{words(text)}</div>{subhtml}<div class="tail"></div></div></div>'
    )
    js.append(f'tl.fromTo("#{i}b",{{scale:0,rotation:-8}},{{scale:1,rotation:0,duration:0.4,ease:"back.out(2.2)"}},{start:.3f});')
    js.append(f'tl.from("#{i} .wd",{{y:30,opacity:0,duration:0.3,ease:"back.out(2)",stagger:0.07}},{start + 0.15:.3f});')
    if sub:
        js.append(f'tl.from("#{i} .bsub",{{opacity:0,y:16,duration:0.3}},{start + 0.6:.3f});')
    js.append(f'tl.to("#{i}b",{{scale:0.6,opacity:0,duration:0.2,ease:"power2.in"}},{start + dur - 0.2:.3f});')
    talk(start + 0.1, min(dur - 0.6, 0.18 * len(text.split()) + 0.6))


def chip(start, dur, n, label):
    i = nid("ch")
    els.append(f'<div id="{i}" class="clip chipwrap" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="8">'
               f'<div class="chip" id="{i}c"><span class="cn">{n}</span><span class="cl">{html.escape(label)}</span></div></div>')
    js.append(f'tl.from("#{i}c",{{x:-500,duration:0.45,ease:"power4.out"}},{start + 0.1:.3f});')
    js.append(f'tl.to("#{i}c",{{x:-500,duration:0.25,ease:"power2.in"}},{start + dur - 0.25:.3f});')




def _odd(n):
    n = max(1, int(n)); return n if n % 2 == 1 else n - 1


def _even(n):
    n = max(2, int(n)); return n if n % 2 == 0 else n - 1


def talk(t, dur):   # gentle "speaking" pulse
    n = _odd(dur / 0.2)
    js.append(f'tl.fromTo("#h-squash",{{scaleY:1,scaleX:1}},{{scaleY:1.025,scaleX:0.99,duration:0.2,ease:"sine.inOut",yoyo:true,repeat:{n},immediateRender:false}},{t:.3f});')


def blink(t):
    pass


def wave(t, dur=1.6):   # friendly greeting: lean + little hop
    js.append(f'tl.to("#h-tilt",{{rotation:-6,duration:0.3,ease:"back.out(2)"}},{t:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:4,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:{_odd((dur - 0.6) / 0.35)}}},{t + 0.3:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:0,duration:0.3,ease:"power2.inOut"}},{t + dur - 0.3:.3f});')
    hop(t + 0.1)


def point(t, dur=2.0, angle=-115):   # lean toward the bubble / the place
    js.append(f'tl.to("#h-tilt",{{rotation:5,duration:0.3,ease:"back.out(2)"}},{t:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:0,duration:0.3,ease:"power2.inOut"}},{t + dur - 0.3:.3f});')


def both_arms_up(t, dur=1.4):   # joyful stretch
    js.append(f'tl.fromTo("#h-squash",{{scaleY:1,scaleX:1}},{{scaleY:1.07,scaleX:0.95,duration:0.18,ease:"power2.out",yoyo:true,repeat:3,immediateRender:false}},{t:.3f});')


def walk(t, dur):   # step bob + alternating sway (her pose is mid-stride)
    n = _even(dur / 0.25)
    js.append(f'tl.fromTo("#h-bob",{{y:0}},{{y:-18,duration:0.125,ease:"sine.out",yoyo:true,repeat:{2 * n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-tilt",{{rotation:-2.5}},{{rotation:2.5,duration:0.25,ease:"sine.inOut",yoyo:true,repeat:{n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:0,duration:0.2}},{t + n * 0.25:.3f});')


def dance(t, dur):
    n = _even(dur / BEAT)
    js.append(f'tl.fromTo("#h-tilt",{{rotation:-6}},{{rotation:6,duration:{BEAT},ease:"sine.inOut",yoyo:true,repeat:{n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-bob",{{y:0}},{{y:-34,duration:{BEAT / 2},ease:"power2.out",yoyo:true,repeat:{2 * n - 1},immediateRender:false}},{t:.3f});')
    js.append(f'tl.to("#h-tilt",{{rotation:0,duration:0.2}},{t + n * BEAT:.3f});')


def hop(t):
    js.append(f'tl.fromTo("#h-hop",{{y:0}},{{y:-70,duration:0.18,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')
    js.append(f'tl.fromTo("#h-shadow",{{scale:1,opacity:0.35}},{{scale:0.7,opacity:0.18,duration:0.18,yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')

# ------------------------------------------------------------------ background base
els.append('<div id="bg" class="clip full" data-start="0" data-duration="36" data-track-index="0"></div>')

# ================= 0-4  hello
els.append('<div id="logo" class="clip logo" data-start="0" data-duration="4" data-track-index="4"><img id="logo-i" src="assets/img/sello-dorado.png" alt=""></div>')
js.append('tl.fromTo("#logo-i",{scale:0.4,rotation:-90,opacity:0},{scale:1,rotation:0,opacity:1,duration:0.8,ease:"back.out(1.5)"},0.1);')
js.append('tl.to("#logo-i",{scale:0.85,opacity:0,y:-80,duration:0.4,ease:"power2.in"},3.6);')
js.append('tl.fromTo("#h-move",{y:1100},{y:0,duration:0.7,ease:"back.out(1.3)"},0.5);')
bubble(1.2, 2.7, "¡hola! bienvenidos a renacer")
wave(1.3, 2.2)

# ================= 4-9  walk through the garden
photo("panoramica-noche.jpg", 4.0, 5.0, 1, (1.25, 1.25, 260, -260, 0, 0), "50% 50%", 0.3)
chip(4.0, 5.0, "01", "el jardín")
walk(4.1, 2.6)
bubble(4.6, 4.2, "te invito a conocer nuestro jardín", "entre encinos de décadas")
point(6.9, 1.9, -120)
FLASH.append(4.0)

# ================= 9-14 dance floor
photo("pista-led.jpg", 9.0, 5.0, 2, (1.3, 1.1, 0, 0, 0, 0), "50% 50%", 0.2)
chip(9.0, 5.0, "02", "la pista")
bubble(9.3, 4.5, "aquí está la pista… ¡lista para bailar!")
point(9.4, 1.6, -110)
dance(11.0, 3.0)
both_arms_up(11.5, 2.2)
FLASH.append(9.0)

# ================= 14-19 grill
photo("parrilla-barra.jpg", 14.0, 2.5, 1, (1.25, 1.1, 0, 0, 0, 0), "40% 50%", 0.25)
photo("carne-asada.jpg", 16.5, 2.5, 2, (1.05, 1.25, 0, 0, 0, -40), "50% 40%", 0.3)
chip(14.0, 5.0, "03", "la parrilla")
bubble(14.3, 4.5, "y la parrilla siempre encendida", "el sabor de casa")
point(14.4, 1.8, -95)
hop(16.5)
FLASH.extend([14.0, 16.5])

# ================= 19-24 spaces with history
photo("arco-columnas.jpg", 19.0, 2.5, 1, (1.1, 1.28, 0, 0, 0, 0), "50% 45%", 0.25)
photo("escalera-luces.jpg", 21.5, 2.5, 2, (1.2, 1.2, 160, -160, 0, 0), "50% 50%", 0.25)
chip(19.0, 5.0, "04", "los rincones")
bubble(19.3, 4.5, "espacios con historia y luz cálida", "como llegar a casa")
walk(19.2, 1.5)
point(21.6, 1.8, -125)
FLASH.extend([19.0, 21.5])

# ================= 24-30 events carousel
photo("kiosco-escalera.jpg", 24.0, 6.0, 1, (1.15, 1.3, 0, 0, 0, 0), "50% 55%", 0.5)
bubble(24.2, 5.6, "celebra aquí lo que vuelve a empezar")
events = ["bodas", "xv años", "bautizos", "convivios"]
for k, ev in enumerate(events):
    t = 24.6 + k * 1.2
    i = nid("ev")
    els.append(f'<div id="{i}" class="clip evwrap" data-start="{t:.3f}" data-duration="{30 - t:.3f}" data-track-index="{3 + k % 2 if False else 9}">'
               f'<div class="evcard" id="{i}c" style="top:{250 + k * 130}px">{html.escape(ev)}</div></div>')
    js.append(f'tl.fromTo("#{i}c",{{x:900,rotation:12}},{{x:0,rotation:{(-3, 2, -2, 3)[k]},duration:0.45,ease:"back.out(1.7)"}},{t:.3f});')
    js.append(f'tl.to("#{i}c",{{x:-1100,duration:0.3,ease:"power2.in"}},{29.6:.3f});')
    hop(t)
    FLASH.append(t)
both_arms_up(28.4, 1.4)

# ================= 30-36 goodbye
els.append('<div id="outro-bg" class="clip full outro-bg" data-start="30" data-duration="6" data-track-index="3"></div>')
js.append('tl.fromTo("#outro-bg",{opacity:0},{opacity:1,duration:0.35},30.0);')
els.append('<div id="seal" class="clip logo top" data-start="30" data-duration="6" data-track-index="4"><img id="seal-i" src="assets/img/sello-dorado.png" alt=""></div>')
js.append('tl.fromTo("#seal-i",{scale:0.3,rotation:-120,opacity:0},{scale:1,rotation:0,opacity:1,duration:0.7,ease:"back.out(1.5)"},30.1);')
js.append('tl.to("#seal-i",{rotation:10,duration:5,ease:"sine.inOut"},30.8);')
bubble(30.6, 5.4, "¿qué estás celebrando?", "escríbenos por whatsapp|san josé el vidrio, edo. de méxico")
wave(31.0, 2.6)
hop(34.0)
FLASH.append(30.0)

for t in [0.9, 3.4, 5.9, 8.1, 10.6, 13.3, 15.7, 18.2, 20.6, 23.1, 25.3, 27.8, 31.8, 34.6]:
    blink(t)

# flash layer + audio
els.append('<div id="flash" class="clip full" data-start="0" data-duration="36" data-track-index="10"></div>')
for t in sorted(FLASH):
    js.append(f'tl.fromTo("#flash",{{opacity:0.45}},{{opacity:0,duration:0.3,ease:"power2.out",immediateRender:false}},{t:.3f});')
els.append('<audio id="bgm" src="assets/music.wav" data-start="0" data-duration="36" data-track-index="11" data-volume="1"></audio>')

CSS = """
@font-face{font-family:'Josefin Sans';font-weight:200;src:url(assets/fonts/josefin-sans-latin-200-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:300;src:url(assets/fonts/josefin-sans-latin-300-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:400;src:url(assets/fonts/josefin-sans-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:600;src:url(assets/fonts/josefin-sans-latin-600-normal.woff2) format('woff2')}
@font-face{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;src:url(assets/fonts/cormorant-garamond-latin-500-italic.woff2) format('woff2')}
html,body{margin:0;background:#1A2214}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Josefin Sans',sans-serif;color:#F0EBE0}
.full{position:absolute;inset:0;width:1080px;height:1920px}
#bg{background:radial-gradient(ellipse at 50% 40%,#2b3822 0%,#1A2214 60%,#10160c 100%)}
.outro-bg{background:radial-gradient(ellipse at 50% 35%,#2b3822 0%,#1A2214 65%,#0f150b 100%)}
#flash{background:#F0EBE0;opacity:0}
.photo{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden}
.photo .pw,.photo img{position:absolute;inset:0;width:1080px;height:1920px}
.photo img{object-fit:cover;display:block}
.photo .shade{position:absolute;inset:0;background:#1A2214}
.photo .grad{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,34,20,.5) 0%,rgba(26,34,20,0) 20%,rgba(26,34,20,0) 50%,rgba(26,34,20,.75) 85%,rgba(26,34,20,.9) 100%)}
.hostclip{position:absolute;left:0;top:0;width:1080px;height:1920px}
#h-move{position:absolute;left:60px;top:975px;width:340px;height:910px;display:block}
#h-shadow{position:absolute;left:30px;top:870px;width:280px;height:44px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(0,0,0,.6) 0%,rgba(0,0,0,0) 70%);opacity:.35;display:block}
#h-hop,#h-bob,#h-tilt,#h-squash{position:absolute;inset:0;width:340px;height:910px;display:block}
#h-tilt,#h-squash{transform-origin:50% 100%}
#h-img{position:absolute;left:0;top:0;width:340px;height:908px;display:block;filter:drop-shadow(0 6px 18px rgba(0,0,0,.35))}
.hostsvg{width:100%;height:100%;display:block;overflow:visible}
.logo{position:absolute;inset:0;width:1080px;height:1920px;display:flex;justify-content:center;align-items:flex-start;padding-top:300px;box-sizing:border-box}
.logo img{width:520px;height:520px;border-radius:50%;display:block}
.logo.top{padding-top:250px}
.logo.top img{width:460px;height:460px}
.bubblewrap{position:absolute;inset:0;width:1080px;height:1920px}
.bubble{position:absolute;left:440px;top:790px;width:600px;box-sizing:border-box;padding:40px 46px 42px;background:#F0EBE0;color:#1A2214;border-radius:44px;transform-origin:8% 100%;box-shadow:0 18px 50px rgba(0,0,0,.35);display:block}
.btext{font-size:58px;font-weight:400;line-height:1.14}
.wd{display:inline-block}
.bsub{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:42px;color:#5A4818;margin-top:10px;white-space:nowrap;line-height:1.1}
.tail{position:absolute;left:-26px;bottom:44px;width:0;height:0;border-top:22px solid transparent;border-bottom:22px solid transparent;border-right:44px solid #F0EBE0}
.chipwrap{position:absolute;inset:0;width:1080px;height:1920px}
.chip{position:absolute;left:0;top:250px;padding:20px 40px 16px 60px;background:#1A2214;border:3px solid #C4B480;border-left:none;border-radius:0 60px 60px 0;display:flex;gap:22px;align-items:baseline}
.cn{font-size:40px;color:#C4B480;font-weight:300;letter-spacing:.1em}
.cl{font-size:52px;font-weight:300;letter-spacing:.08em;color:#F0EBE0}
.evwrap{position:absolute;inset:0;width:1080px;height:1920px}
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
