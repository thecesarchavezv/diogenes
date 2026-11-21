"""Generates the HyperFrames composition (index.html) for the Renacer reel.

Atelier composition: hand-authored scenes, brand palette and type from the
Renacer brand book, every cut and text hit locked to the 120 BPM music grid.
"""
import html
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
W, H, DUR = 1080, 1920, 30.0
BEAT = 0.5

# ------------------------------------------------------------------ helpers
els = []      # html for clips (direct children of root)
js = []       # timeline statements
uid = [0]


def nid(prefix):
    uid[0] += 1
    return f"{prefix}{uid[0]}"


def letters(text, cls="l"):
    out = []
    for ch in text:
        if ch == " ":
            out.append('<span class="sp"> </span>')
        else:
            out.append(f'<span class="{cls}">{html.escape(ch)}</span>')
    return "".join(out)


def words(text):
    return " ".join(
        f'<span class="wm"><span class="wi">{html.escape(w)}</span></span>' for w in text.split(" ")
    )


def photo(img, start, dur, track=1, kb=(1.18, 1.0, 0, 0, 0, 0), pos="50% 50%", dim=0.0, punch=True):
    """Full-bleed photo clip. kb = (scale_from, scale_to, x_from, x_to, y_from, y_to)."""
    i = nid("ph")
    els.append(
        f'<div id="{i}" class="clip photo" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{track}">'
        f'<div class="pw" id="{i}w"><img id="{i}i" src="assets/img/{img}" style="object-position:{pos}" alt=""></div>'
        f'<div class="shade" style="opacity:{dim}"></div><div class="grad"></div></div>'
    )
    s0, s1, x0, x1, y0, y1 = kb
    js.append(f'tl.fromTo("#{i}i",{{scale:{s0},x:{x0},y:{y0}}},{{scale:{s1},x:{x1},y:{y1},duration:{dur:.3f},ease:"none"}},{start:.3f});')
    if punch:
        # beat punch on the wrapper (separate element from the Ken Burns)
        t = start
        k = 0
        while t < start + dur - 0.01:
            js.append(f'tl.fromTo("#{i}w",{{scale:1.055}},{{scale:1,duration:0.42,ease:"power3.out"}},{t:.3f});')
            t += BEAT
            k += 1
    return i


FLASHES = []


def flash(t, strength=0.75, dur=0.35):
    FLASHES.append((t, strength, dur))


# ------------------------------------------------------------------ base layers
els.append('<div id="bg" class="clip full" data-start="0" data-duration="30" data-track-index="0"></div>')

# ================================================================== 0-4 INTRO
# Leaf grows like a sprout, text "algo volvió a nacer" pops letter by letter.
LEAF = (
    '<svg viewBox="0 0 54 74" class="leafsvg">'
    '<path d="M27 5 Q33 5,36 10 Q42 13,40 19 Q44 24,40 30 Q44 36,39 42 Q38 50,30 56 Q28 58,27 58 '
    'Q26 58,24 56 Q16 50,15 42 Q10 36,14 30 Q10 24,14 19 Q12 13,18 10 Q21 5,27 5 Z" fill="#C4B480"/>'
    '<line x1="27" y1="7" x2="27" y2="56" stroke="#1A2214" stroke-width="1" stroke-linecap="round" opacity="0.5"/>'
    '<path d="M27 17 Q33 19 37 16 M27 17 Q21 19 17 16 M27 27 Q34 29 38 26 M27 27 Q20 29 16 26 '
    'M27 37 Q33 39 37 37 M27 37 Q21 39 17 37" fill="none" stroke="#1A2214" stroke-width="0.6" '
    'stroke-linecap="round" opacity="0.4"/>'
    '<line x1="27" y1="58" x2="27" y2="70" stroke="#C4B480" stroke-width="2" stroke-linecap="round"/></svg>'
)
els.append(
    f'<div id="intro-photo" class="clip photo" data-start="1.9" data-duration="2.1" data-track-index="1">'
    f'<div class="pw"><img id="intro-photo-i" src="assets/img/panoramica-noche.jpg" style="object-position:38% 50%" alt=""></div>'
    f'<div class="shade" style="opacity:.45"></div><div class="grad"></div></div>'
)
js.append('tl.fromTo("#intro-photo",{opacity:0},{opacity:1,duration:1.2,ease:"power2.out"},1.9);')
js.append('tl.fromTo("#intro-photo-i",{scale:1.45,x:120},{scale:1.15,x:-60,duration:2.1,ease:"none"},1.9);')

els.append(f'<div id="leaf" class="clip center-abs" data-start="0" data-duration="4" data-track-index="5"><div id="leaf-in">{LEAF}</div></div>')
js.append('tl.fromTo("#leaf-in",{scale:0,rotation:-35,y:-300},{scale:1,rotation:0,y:-400,duration:1.1,ease:"back.out(1.6)"},0.15);')
js.append('tl.to("#leaf-in",{y:-520,scale:0.6,duration:0.9,ease:"power3.inOut"},1.7);')
js.append('tl.to("#leaf-in",{rotation:8,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:2},2.6);')

els.append(
    f'<div id="intro-t1" class="clip textblock mid" data-start="0.7" data-duration="3.3" data-track-index="6">'
    f'<div class="big thin">{letters("algo volvió")}</div><div class="big thin">{letters("a nacer")}</div>'
    f'<div class="rule" id="intro-rule"></div>'
    f'<div class="kicker" id="intro-k">entre los encinos</div></div>'
)
js.append('tl.from("#intro-t1 .l",{yPercent:120,opacity:0,rotation:12,duration:0.5,ease:"back.out(2)",stagger:0.045},0.75);')
js.append('tl.fromTo("#intro-rule",{scaleX:0},{scaleX:1,duration:0.6,ease:"power3.out"},1.9);')
js.append('tl.from("#intro-k",{y:30,opacity:0,duration:0.6,ease:"power3.out"},2.2);')
js.append('tl.to("#intro-t1",{opacity:0,y:-40,duration:0.3,ease:"power2.in"},3.7);')

# ================================================================== 4-8 BUILD
build1 = [
    ("escalera-luces.jpg", "luz", "50% 50%"),
    ("kiosco-escalera.jpg", "música", "50% 60%"),
    ("palmera-reunion.jpg", "familia", "50% 55%"),
    ("pista-noche-arboles.jpg", "fiesta", "30% 50%"),
]
for k, (img, word, pos) in enumerate(build1):
    t = 4.0 + k * BEAT
    photo(img, t, BEAT, track=1 + (k % 2), kb=(1.25, 1.12, 0, 0, 0, 0), pos=pos, dim=0.35, punch=False)
    i = nid("bw")
    els.append(f'<div id="{i}" class="clip textblock center" data-start="{t:.3f}" data-duration="{BEAT:.3f}" data-track-index="{6 + k % 2}"><div class="slam">{html.escape(word)}</div></div>')
    js.append(f'tl.fromTo("#{i} .slam",{{scale:2.6,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power4.out"}},{t:.3f});')
    js.append(f'tl.to("#{i} .slam",{{scale:0.92,duration:0.28,ease:"none"}},{t + 0.22:.3f});')
    flash(t, 0.55, 0.25)

build2 = [
    ("panoramica-noche.jpg", "una", "40% 50%"),
    ("parrilla-barra.jpg", "historia", "45% 50%"),
    ("arco-columnas.jpg", "que", "50% 50%"),
    ("pista-led.jpg", "vuelve", "50% 50%"),
    ("carne-asada.jpg", "a", "50% 40%"),
    ("encino-terraza.jpg", "empezar", "45% 50%"),
]
for k, (img, word, pos) in enumerate(build2):
    t = 6.0 + k * 0.25
    d = 0.25 if k < 5 else 0.5
    photo(img, t, d, track=1 + (k % 2), kb=(1.3, 1.2, 0, 0, 0, 0), pos=pos, dim=0.4, punch=False)
    i = nid("bw")
    els.append(f'<div id="{i}" class="clip textblock center" data-start="{t:.3f}" data-duration="{d:.3f}" data-track-index="{6 + k % 2}"><div class="slam sm">{html.escape(word)}</div></div>')
    js.append(f'tl.fromTo("#{i} .slam",{{scale:1.8,opacity:0}},{{scale:1,opacity:1,duration:0.12,ease:"power4.out"}},{t:.3f});')
    flash(t, 0.35, 0.15)
# 7.75-8.0: the music cuts to silence -> pure dark frame

# ================================================================== 8-10 DROP: brand slam
photo("pista-led.jpg", 8.0, 2.0, track=1, kb=(1.35, 1.12, 0, 0, 0, 0), pos="50% 50%", dim=0.62)
for r in range(3):
    i = nid("ring")
    els.append(f'<div id="{i}" class="clip center-abs" data-start="8" data-duration="2" data-track-index="4"><div class="ring" id="{i}r"></div></div>')
    js.append(f'tl.fromTo("#{i}r",{{scale:0.2,opacity:0.9}},{{scale:2.6,opacity:0,duration:1.2,ease:"power2.out"}},{8.0 + r * 0.5:.3f});')
els.append(
    f'<div id="brand" class="clip textblock center" data-start="8" data-duration="2" data-track-index="6">'
    f'<div id="brand-leaf">{LEAF}</div>'
    f'<div class="brandname">{letters("renacer", "bl")}</div>'
    f'<div class="rule wide" id="brand-rule"></div>'
    f'<div class="caps" id="brand-sub">JARDÍN DE EVENTOS</div></div>'
)
js.append('tl.fromTo("#brand-leaf",{scale:0,rotation:-90},{scale:1,rotation:0,duration:0.5,ease:"back.out(2.2)"},8.0);')
js.append('tl.from("#brand .bl",{scale:3,opacity:0,y:-40,duration:0.35,ease:"power4.out",stagger:0.06},8.05);')
js.append('tl.fromTo("#brand-rule",{scaleX:0},{scaleX:1,duration:0.5,ease:"power3.out"},8.5);')
js.append('tl.from("#brand-sub",{opacity:0,scaleX:0.6,duration:0.7,ease:"power3.out"},8.6);')
js.append('tl.to("#brand",{scale:1.06,duration:1.2,ease:"none"},8.6);')
flash(8.0, 0.95, 0.5)

# ================================================================== 10-24 FEATURE SCENES
scenes = [
    # (start, dur, img, pos, kb, kicker, line1, line2, style)
    (10.0, 2.0, "pista-noche-arboles.jpg", "35% 50%", (1.2, 1.05, 140, -140, 0, 0), "de noche,", "la pista", "brilla", "up"),
    (12.0, 2.0, "escalera-luces.jpg", "50% 50%", (1.1, 1.3, -80, 80, 0, -40), "cada rincón", "con luz", "cálida", "pop"),
    (14.0, 1.0, "parrilla-barra.jpg", "40% 50%", (1.25, 1.1, 0, 0, 0, 0), "el olor de", "la parrilla", "encendida", "side"),
    (15.0, 1.0, "carne-asada.jpg", "50% 45%", (1.05, 1.25, 0, 0, 30, -30), "DIM30", None, None, None),
    (16.0, 2.0, "molcajete.jpg", "50% 40%", (1.3, 1.08, 0, 0, -40, 40), "salsa de molcajete", "sabor", "de casa", "pop"),
    (18.0, 2.0, "arco-columnas.jpg", "50% 45%", (1.08, 1.28, 0, 0, 0, 0), "tu entrada", "bajo los", "encinos", "up"),
    (20.0, 2.0, "palmera-reunion.jpg", "50% 50%", (1.3, 1.1, 0, 0, 60, -20), "del bisabuelo a la nieta", "aquí cabe", "toda tu familia", "side"),
    (22.0, 2.0, "banca-fuente.jpg", "50% 50%", (1.1, 1.25, 40, -40, 0, 0), "detalles que cuentan", "espacios", "con historia", "pop"),
]
for (st, du, img, pos, kb, kicker, l1, l2, style) in scenes:
    photo(img, st, du, track=1 + int(st) % 2, kb=kb, pos=pos, dim=0.35 if kicker == "DIM30" else 0.15)
    if kicker == "DIM30":
        kicker = None
    flash(st, 0.6, 0.3)
    # sweeping gold line on each cut
    i = nid("sw")
    els.append(f'<div id="{i}" class="clip full" data-start="{st:.3f}" data-duration="0.6" data-track-index="8"><div class="sweep" id="{i}s"></div></div>')
    js.append(f'tl.fromTo("#{i}s",{{x:-1300}},{{x:1300,duration:0.55,ease:"power2.inOut"}},{st:.3f});')
    if l1 is None:
        continue
    tdur = du if st != 14.0 else 2.0  # parrilla text spans both photos
    i = nid("tx")
    els.append(
        f'<div id="{i}" class="clip textblock lower" data-start="{st + 0.05:.3f}" data-duration="{tdur - 0.05:.3f}" data-track-index="{6 + int(st) % 2}">'
        f'<div class="kicker">{html.escape(kicker)}</div>'
        f'<div class="head">{words(l1) if style != "pop" else letters(l1)}</div>'
        f'<div class="head accent">{words(l2) if style != "pop" else letters(l2)}</div>'
        f'<div class="rule" ></div></div>'
    )
    t0 = st + 0.05
    js.append(f'tl.from("#{i} .kicker",{{x:-60,opacity:0,duration:0.4,ease:"power3.out"}},{t0:.3f});')
    if style == "up":
        js.append(f'tl.from("#{i} .wi",{{yPercent:115,rotation:8,duration:0.45,ease:"back.out(1.9)",stagger:0.08}},{t0 + 0.1:.3f});')
    elif style == "side":
        js.append(f'tl.from("#{i} .wi",{{xPercent:-110,opacity:0,duration:0.4,ease:"power4.out",stagger:0.07}},{t0 + 0.1:.3f});')
    else:  # pop letters
        js.append(f'tl.from("#{i} .l",{{scale:0,opacity:0,y:40,duration:0.38,ease:"back.out(3)",stagger:0.035}},{t0 + 0.1:.3f});')
    js.append(f'tl.fromTo("#{i} .rule",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power3.out"}},{t0 + 0.45:.3f});')
    # accent line pulses on the beat
    js.append(f'tl.fromTo("#{i} .accent",{{scale:1.08}},{{scale:1,duration:0.35,ease:"power2.out"}},{st + 1.0:.3f});')
    js.append(f'tl.to("#{i}",{{opacity:0,y:-30,duration:0.18,ease:"power2.in"}},{st + tdur - 0.2:.3f});')

# ================================================================== 24-28 EVENT TYPES
events = [
    (24.0, "kiosco-escalera.jpg", "50% 55%", "bodas"),
    (25.0, "pista-noche-arboles.jpg", "60% 50%", "xv años"),
    (26.0, "fachada-dia.jpg", "50% 50%", "bautizos"),
    (27.0, "encino-terraza.jpg", "40% 50%", "convivios"),
]
for k, (st, img, pos, word) in enumerate(events):
    photo(img, st, 1.0, track=1 + k % 2, kb=(1.3, 1.1, 0, 0, 0, 0), pos=pos, dim=0.4)
    flash(st, 0.7, 0.3)
    i = nid("ev")
    els.append(
        f'<div id="{i}" class="clip textblock center" data-start="{st:.3f}" data-duration="1" data-track-index="{6 + k % 2}">'
        f'<div class="frame" id="{i}f"></div>'
        f'<div class="evword">{letters(word)}</div>'
        f'<div class="evnum">{k + 1:02d} / 04</div></div>'
    )
    js.append(f'tl.fromTo("#{i}f",{{scale:1.6,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:0,duration:0.35,ease:"power4.out"}},{st:.3f});')
    js.append(f'tl.from("#{i} .l",{{yPercent:-140,opacity:0,duration:0.3,ease:"back.out(2.5)",stagger:0.03}},{st + 0.05:.3f});')
    js.append(f'tl.from("#{i} .evnum",{{opacity:0,y:20,duration:0.3}},{st + 0.25:.3f});')
    js.append(f'tl.fromTo("#{i}f",{{scale:1.05}},{{scale:1,duration:0.3,ease:"power2.out"}},{st + 0.5:.3f});')

# ================================================================== 28-30 OUTRO
els.append('<div id="outro-bg" class="clip full outro-bg" data-start="28" data-duration="2" data-track-index="3"></div>')
js.append('tl.fromTo("#outro-bg",{opacity:0},{opacity:1,duration:0.25,ease:"power2.out"},28.0);')
els.append(
    '<div id="outro" class="clip textblock outro" data-start="28" data-duration="2" data-track-index="6">'
    '<img id="outro-seal" src="assets/img/sello-dorado.png" alt="">'
    '<div class="q" id="outro-q">¿qué estás celebrando?</div>'
    '<div class="rule wide" id="outro-rule"></div>'
    '<div class="caps sm" id="outro-cta">ESCRÍBENOS POR WHATSAPP</div>'
    '<div class="place" id="outro-place">jardín familiar entre encinos · monterrey, n.l.</div></div>'
)
js.append('tl.fromTo("#outro-seal",{scale:0.3,rotation:-120,opacity:0},{scale:1,rotation:0,opacity:1,duration:0.7,ease:"back.out(1.5)"},28.0);')
js.append('tl.to("#outro-seal",{rotation:6,duration:1.3,ease:"sine.inOut"},28.7);')
js.append('tl.from("#outro-q",{y:40,opacity:0,duration:0.5,ease:"power3.out"},28.35);')
js.append('tl.fromTo("#outro-rule",{scaleX:0},{scaleX:1,duration:0.5,ease:"power3.out"},28.6);')
js.append('tl.from("#outro-cta",{opacity:0,scaleX:0.6,duration:0.6,ease:"power3.out"},28.7);')
js.append('tl.from("#outro-place",{opacity:0,y:20,duration:0.5,ease:"power3.out"},28.9);')
flash(28.0, 0.8, 0.4)

# ------------------------------------------------------------------ flash layer + audio
els.append('<div id="flash" class="clip full" data-start="0" data-duration="30" data-track-index="9"></div>')
for (t, s, d) in sorted(FLASHES):
    js.append(f'tl.fromTo("#flash",{{opacity:{s}}},{{opacity:0,duration:{d},ease:"power2.out",immediateRender:false}},{t:.3f});')
els.append('<audio id="bgm" src="assets/music.wav" data-start="0" data-duration="30" data-track-index="10" data-volume="1"></audio>')

CSS = """
@font-face{font-family:'Josefin Sans';font-weight:100;src:url(assets/fonts/josefin-sans-latin-100-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:200;src:url(assets/fonts/josefin-sans-latin-200-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:300;src:url(assets/fonts/josefin-sans-latin-300-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:400;src:url(assets/fonts/josefin-sans-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:'Josefin Sans';font-weight:600;src:url(assets/fonts/josefin-sans-latin-600-normal.woff2) format('woff2')}
@font-face{font-family:'Cormorant Garamond';font-style:italic;font-weight:400;src:url(assets/fonts/cormorant-garamond-latin-400-italic.woff2) format('woff2')}
@font-face{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;src:url(assets/fonts/cormorant-garamond-latin-500-italic.woff2) format('woff2')}
:root{--encino:#1A2214;--ambar:#5A4818;--crema:#F0EBE0;--paja:#C4B480;--tierra:#8A7850}
html,body{margin:0;padding:0;background:#1A2214}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Josefin Sans',sans-serif;color:var(--crema)}
.full{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden}
#bg{background:radial-gradient(ellipse at 50% 40%,#26311d 0%,#1A2214 60%,#10160c 100%)}
#flash{background:var(--crema);opacity:0;mix-blend-mode:screen}
.photo{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden}
.photo .pw{position:absolute;inset:0;width:1080px;height:1920px}
.photo img{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;display:block}
.photo .shade{position:absolute;inset:0;background:var(--encino)}
.photo .grad{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,34,20,.55) 0%,rgba(26,34,20,0) 22%,rgba(26,34,20,0) 45%,rgba(26,34,20,.82) 78%,rgba(26,34,20,.92) 100%)}
.center-abs{position:absolute;inset:0;width:1080px;height:1920px;display:flex;align-items:center;justify-content:center}
#leaf-in{width:300px;height:411px;display:block}
.leafsvg{width:100%;height:100%;display:block}
.textblock{position:absolute;left:0;top:0;width:1080px;height:1920px;box-sizing:border-box;display:flex;flex-direction:column;padding:0 90px}
.textblock.mid{justify-content:center;align-items:center;text-align:center;padding-top:260px}
.textblock.center{justify-content:center;align-items:center;text-align:center}
.textblock.lower{justify-content:flex-end;align-items:flex-start;padding-bottom:470px}
.textblock.outro{justify-content:center;align-items:center;text-align:center;padding-bottom:120px}
.l,.bl{display:inline-block}
.sp{display:inline-block;width:.3em}
.big{font-size:132px;line-height:1.02;letter-spacing:.04em;font-weight:200;white-space:nowrap}
.kicker{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:62px;color:var(--paja);margin-top:18px;line-height:1.1}
.lower .kicker{margin:0 0 6px 4px}
.rule{width:220px;height:4px;background:var(--paja);margin-top:30px;transform-origin:0 50%;display:block}
.mid .rule,.center .rule,.outro .rule{transform-origin:50% 50%}
.rule.wide{width:420px}
.slam{font-size:230px;font-weight:300;letter-spacing:.02em;line-height:1;color:var(--crema);text-shadow:0 10px 60px rgba(0,0,0,.45);display:block;white-space:nowrap}
.slam.sm{font-size:170px}
#brand-leaf{width:170px;height:233px;margin-bottom:40px;display:block}
.brandname{font-size:190px;font-weight:200;letter-spacing:.2em;margin-right:-.2em;line-height:1;white-space:nowrap}
.caps{display:block;font-weight:200;font-size:44px;letter-spacing:.44em;margin-right:-.44em;color:var(--paja);margin-top:26px;white-space:nowrap}
.caps.sm{font-size:34px;font-weight:300;letter-spacing:.32em;margin-right:-.32em;color:var(--crema)}
.head{font-size:128px;font-weight:300;line-height:1.04;letter-spacing:.01em;white-space:nowrap;display:block;transform-origin:0 50%}
.head.accent{color:var(--paja);font-weight:400}
.wm{display:inline-block;overflow:hidden;vertical-align:top;padding:0 0 .08em}
.wi{display:inline-block}
.frame{position:absolute;left:50%;top:50%;width:860px;height:440px;margin:-220px 0 0 -430px;border:5px solid var(--paja);box-sizing:border-box;display:block}
.evword{font-size:160px;font-weight:300;letter-spacing:.06em;line-height:1;white-space:nowrap;position:relative}
.evnum{font-size:36px;letter-spacing:.3em;color:var(--paja);margin-top:40px;font-weight:300;position:relative}
.ring{width:700px;height:700px;border-radius:50%;border:6px solid var(--paja);box-sizing:border-box;display:block}
.outro-bg{background:radial-gradient(ellipse at 50% 42%,#27321e 0%,#1A2214 65%,#0f150b 100%)}
#outro-seal{width:640px;height:640px;display:block;border-radius:50%}
.q{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:500;font-size:88px;color:var(--crema);margin-top:56px;line-height:1.1}
.place{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:400;font-size:44px;color:var(--paja);margin-top:30px}
.sweep{position:absolute;top:0;left:0;width:340px;height:1920px;background:linear-gradient(90deg,rgba(196,180,128,0) 0%,rgba(196,180,128,.38) 50%,rgba(196,180,128,0) 100%);transform:skewX(-14deg);display:block}
"""

doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>renacer · jardín de eventos</title>
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style>
</head>
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
</body>
</html>
"""
import re
doc = re.sub(r'<div id="([^"]+)" class="clip([^"]*)"([^>]*?)data-track-index="(\d+)"', lambda m: f'<div id="{m.group(1)}" class="clip{m.group(2)}"{m.group(3)}data-track-index="{m.group(4)}" style="z-index:{m.group(4)}"', doc)
OUT.write_text(doc, encoding="utf-8")
print("wrote", OUT, len(els), "clips", len(js), "tweens")
