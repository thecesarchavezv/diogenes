# Plan completo: infoproducto de juego/guía para parejas (PDF + App)

> **Referencias:** `lachispasecreta.impultienda.ar` y `eljuegodeldeseo.impultienda.ar`.
> **Ojo:** ambos sitios están detrás de un control anti-bots de Cloudflare y no se pudieron leer desde este entorno. El análisis se basa en el modelo conocido de las tiendas *impultienda.ar* (infoproductos de bajo precio en ARS, una landing por producto, tráfico pagado desde Meta) y en lo que sugieren los nombres. Hay que validar los datos marcados con **[VALIDAR]** abriendo los sitios en un navegador común (ver §13).

---

## 0. Criterio clave: copiar el modelo, no la marca

Se replica **el modelo de negocio, el formato, la estructura de la oferta y el embudo**. **No** se copian nombres, textos, ilustraciones, diseño ni testimonios. Hay tres motivos:
1. **Legal:** copiar textos y diseño viola derechos de autor y marca, y además genera reclamos y bloqueos en Hotmart, Mercado Pago y Meta.
2. **Anuncios:** Meta detecta creatividades duplicadas y penaliza la entrega.
3. **Ventaja:** un producto mejor que el original (con app interactiva) se puede posicionar como superior y no como copia.

Nombres originales propuestos (verificar dominio, @ en redes y marca en INPI):
- **"Noches de Complicidad"**: juego + guía, tono cálido y romántico.
- **"Código Fuego"**: más picante y lúdico.
- **"30 Noches"**: enfocado en el reto de 30 días.

---

## 1. Diagnóstico del modelo de referencia

| Elemento | Lo que casi seguro usan | Qué hacemos |
|---|---|---|
| Producto | PDF de guía o juego erótico/romántico para parejas (retos, cartas, posiciones, juegos de rol) **[VALIDAR contenido exacto]** | PDF premium **+ app web interactiva** |
| Precio | Bajo precio en ARS, con "precio tachado" y descuento del 70-90% **[VALIDAR monto]** | Equivalente a USD 5-9, con escalera de precios |
| Landing | Una sola página larga para móvil, contador regresivo, testimonios con capturas de WhatsApp, sección de bonos, garantía y preguntas frecuentes | Igual de larga, con copy y diseño propios y prueba social real |
| Checkout | Hotmart, Mercado Pago o pasarela de la tienda **[VALIDAR]** | Hotmart (afiliados, área de miembros) o Mercado Pago + entrega automática |
| Tráfico | Meta Ads (Facebook/Instagram), sobre todo Reels | Meta + TikTok + orgánico + afiliados |
| Entrega | Email con enlace de descarga | Email + área de miembros + app con código de acceso |
| Ticket medio | Order bump y upsell de 1 clic | Bump + upsell + downsell + recompra |

**Por qué funciona:** compra impulsiva de bajo riesgo, un dolor emocional fuerte ("se apagó la pasión", "la rutina") y un regalo fácil (aniversarios, San Valentín, Día de los Enamorados).

---

## 2. El producto

### 2.1 Público objetivo (avatares)
1. **Laura, 28-45 años, en pareja hace más de 5 años:** siente rutina, quiere reavivar sin que sea incómodo, compra desde el celular de noche. Es el **público principal (≈70%)**.
2. **Martín, 25-40:** quiere sorprender a su pareja o regalar algo distinto.
3. **Parejas jóvenes o recién mudadas (22-30):** buscan diversión y complicidad.

Objeciones a resolver: *"me da vergüenza"*, *"mi pareja no va a querer"*, *"¿es vulgar?"*, *"¿es una estafa?"*, *"¿quién ve mi compra?"*.

### 2.2 Contenido del PDF principal (60-80 págs, diseño editorial, modo oscuro y claro)
1. **Introducción:** cómo usar el juego, reglas de consentimiento y la "palabra pausa".
2. **Test de pareja:** 20 preguntas para descubrir su "perfil de deseo" (4 perfiles).
3. **Juego de 120 cartas en 4 niveles:**
   - 🟢 *Conexión* (30): preguntas íntimas y recuerdos.
   - 🟡 *Coqueteo* (30): retos suaves, masajes, besos.
   - 🟠 *Fuego* (30): retos sensuales.
   - 🔴 *Secreto* (30): fantasías, juegos de rol (sin contenido explícito gráfico).
4. **Reto de 30 noches:** calendario con una actividad por día.
5. **10 citas en casa:** guiones paso a paso (cena a ciegas, spa en casa, "desconocidos en un bar").
6. **Guía de comunicación del deseo:** cómo proponer cosas sin incomodar.
7. **Cartas imprimibles:** páginas para recortar o imprimir.

### 2.3 Bonos (valor percibido alto, costo marginal cero)
- 🎁 **Dados del deseo imprimibles** (acción × zona).
- 🎁 **Playlist "Noche perfecta"** (enlace a Spotify).
- 🎁 **40 mensajes para calentar el día** (para enviar por WhatsApp).
- 🎁 **Guía de masajes en pareja** (10 técnicas ilustradas).
- 🎁 **Edición especial para fechas:** San Valentín y aniversario.

### 2.4 Versión App interactiva (diferencial competitivo)
**Formato:** PWA (app web instalable en iOS y Android sin pasar por las tiendas, que suelen rechazar contenido para adultos).

**Funciones:**
- Ingreso de los nombres de la pareja → personaliza cada carta ("Laura, besá a Martín…").
- Elegir nivel → mazo aleatorio con animación de giro de carta.
- Modo "ruleta" y "dados" animados.
- Temporizador para retos.
- Reto de 30 noches con progreso guardado y rachas.
- Favoritas, "saltar" y "nunca más mostrar".
- Modo discreto: ícono y nombre neutros, PIN de bloqueo.
- Funciona sin conexión una vez instalada.

**Stack recomendado:**
- **Opción rápida (1-2 semanas):** Lovable o Vite + React + Tailwind, contenido en un JSON, `localStorage` para el progreso y hosting en Netlify o Vercel.
- **Control de acceso:** código de licencia único por compra (webhook de Hotmart o Mercado Pago → base Supabase → email con el código), o *magic link* de Supabase Auth.
- **Fase 2:** sincronizar entre los dos celulares (sala compartida por código), cartas nuevas mensuales (suscripción).

### 2.5 Producción (con IA + revisión humana)
| Tarea | Herramienta | Tiempo |
|---|---|---|
| Redacción de cartas y guía | Claude + edición humana (tono, consentimiento) | 4-5 días |
| Revisión por sexólogo/a o terapeuta de pareja | Freelance (Workana) | 2-3 días. **Sirve como argumento de venta** |
| Diseño del PDF | Canva Pro o Figma (plantilla editorial, ilustraciones lineales elegantes, nada explícito) | 3-4 días |
| Mockups 3D del producto | Canva o Higgsfield (celular + libro + cartas) | 1 día |
| App PWA | Lovable o desarrollo propio | 5-10 días |

**Identidad visual sugerida:** bordó/vino `#5B0F2E`, dorado suave `#D4A373`, crema `#F6EFE7` y negro `#141014`. Tipografías Playfair Display (títulos) e Inter (texto). Estética "sexy elegante", no vulgar. Esto también es clave para aprobar anuncios.

---

## 3. Oferta y precios

> Ajustar al tipo de cambio del día. Con la inflación en ARS conviene fijar el precio en USD y convertir.

| Escalón | Contenido | Precio sugerido |
|---|---|---|
| **Principal** | PDF completo + 5 bonos | ~USD 6-7 (precio "tachado" ~USD 29) |
| **Order bump** (casilla en el checkout) | **App interactiva** con acceso de por vida | +USD 4 |
| **Upsell 1 clic** | "Pack Fantasías": 50 juegos de rol con guion + audio-guías | USD 9 |
| **Downsell** (si rechaza el upsell) | Versión reducida del pack | USD 5 |
| **Combo regalo** | Versión imprimible con tarjeta de regalo personalizada | USD 9 |
| **Recurrente (fase 2)** | Cartas nuevas mensuales en la app | USD 2,99/mes |

**Meta de ticket medio:** USD 9-11 (el bump convierte un 30-40% y el upsell un 10-15%).

**Garantía:** 7 días incondicional (Hotmart). En Argentina además corre el **derecho de arrepentimiento de 10 días** (Ley 24.240, art. 34) y la tienda debe tener el **"Botón de arrepentimiento"** (Res. 424/2020).

**Urgencia honesta:** precio de lanzamiento por tiempo limitado con fecha real. Nada de contadores que se reinician: Meta y las leyes de consumo lo sancionan.

---

## 4. Stack técnico del embudo

| Pieza | Opción A (simple) | Opción B (control total) |
|---|---|---|
| Dominio | `nochesdecomplicidad.com` o similar | igual |
| Landing | Lovable, Webflow o Hotmart Pages | WordPress + Elementor |
| Checkout | **Hotmart** (pagos LATAM, afiliados, área de miembros, bump/upsell nativos) | Mercado Pago + Stripe + webhook propio |
| Entrega | Área de miembros de Hotmart + email | Supabase + Resend (email con PDF y código de la app) |
| Email marketing | Brevo o MailerLite | ActiveCampaign |
| Medición | Meta Pixel + **API de Conversiones**, GA4, Microsoft Clarity | + UTM + Looker Studio |
| WhatsApp | WhatsApp Business (soporte) | + recuperación de carritos |
| Protección del PDF | Marca de agua con el email del comprador (Hotmart lo hace) | PDF con marca de agua generada al vuelo |

---

## 5. La landing, sección por sección (pensada para móvil)

1. **Barra superior:** "🔥 Precio de lanzamiento hasta el [fecha]".
2. **Hero:** titular centrado en el resultado.
   - *"El juego que convierte cualquier noche de rutina en una noche que no van a olvidar"*.
   - Subtítulo: "120 cartas, 30 noches de retos y una app para jugar desde el celular. Sin vergüenza, a su ritmo."
   - Mockup del producto + botón **"QUIERO EMPEZAR ESTA NOCHE"**.
3. **Identificación del dolor:** "¿Les pasa que…?" (rutina, celular en la cama, siempre lo mismo).
4. **La causa:** "No es falta de amor, es falta de juego" (reencuadre sin culpa).
5. **La solución:** presentación del producto y cómo funciona en 3 pasos (Eligen nivel → Sacan carta → Juegan).
6. **Qué incluye:** módulos con íconos + valor de cada uno.
7. **Demo de la app:** GIF o video de 10 segundos girando cartas.
8. **Los 4 niveles:** explican que avanzan solo si ambos quieren (baja la objeción "mi pareja no va a querer").
9. **Bonos:** con su valor tachado.
10. **Prueba social:** testimonios reales de la preventa (con permiso, sin fotos explícitas), cantidad de parejas y puntuación.
11. **Respaldo profesional:** "Contenido revisado por [Lic. X], sexóloga".
12. **Comparativa de valor:** "Una cena afuera: USD 40. Esto: menos que un café."
13. **Oferta y precio:** con lista final de lo que incluye y botón de compra.
14. **Garantía:** sello de 7 días.
15. **Privacidad:** "El cobro aparece como [nombre neutro]. Entrega solo a tu email."
16. **Preguntas frecuentes:** ¿Es explícito? ¿Cómo lo recibo? ¿Sirve para parejas del mismo sexo? (sí, lenguaje inclusivo) ¿Necesito imprimir? ¿Funciona en iPhone?
17. **Botón final + pie legal:** +18, términos, privacidad, botón de arrepentimiento y datos fiscales.

**Rendimiento esperado:** carga en menos de 2,5 s en 4G, imágenes WebP y botón de compra visible cada 2 o 3 pantallas.

---

## 6. Posicionamiento

- **Promesa:** *"Vuelvan a jugar."* Complicidad, diversión y deseo, sin vulgaridad.
- **Diferenciales frente a la competencia:** (1) app interactiva y personalizada, (2) revisión profesional, (3) progresión por niveles con consentimiento, (4) inclusiva, (5) estética premium y regalable.
- **Tono:** cálido, pícaro, cómplice, en segunda persona ("ustedes"), con voseo para Argentina y versión neutra para LATAM.
- **Categoría:** no es "contenido para adultos" sino **"juego de pareja / bienestar de la relación"**. Este encuadre es clave para Meta y para las pasarelas de pago.

---

## 7. Campaña de marketing digital

### 7.1 Políticas de anuncios (lo que más tumba cuentas en este nicho)
Meta prohíbe en anuncios la desnudez, las posiciones sugerentes, el enfoque en partes del cuerpo y los textos sexuales explícitos. Reglas propias:
- Imágenes: parejas vestidas riendo, manos y cartas, mockups, nada de cama con poses.
- Palabras prohibidas en los anuncios: "sexo", "erótico", "orgasmo", "caliente". Usar en cambio "pasión", "complicidad", "chispa", "noches", "juego de pareja".
- Segmentar a **mayores de 18**, ideal 25-50.
- Tener **2 cuentas publicitarias y 2 páginas de respaldo** y un Business Manager verificado.
- La landing también debe ser "apta para anuncios" (lo explícito queda dentro del producto).

### 7.2 Estructura de campañas en Meta
**Fase 1: Testeo (días 1-14), presupuesto USD 20-30/día**
- Campaña de **Ventas** (optimización: Compra) con conjuntos de anuncios ABO.
- 3 conjuntos: (a) abierto, solo +25 años, AR; (b) intereses: relaciones, matrimonio, citas, regalos de San Valentín; (c) Advantage+ audiencia.
- 5-8 anuncios por conjunto: 3 ángulos × formatos.
- **Criterio de corte:** apagar el anuncio si gasta 1,5× el CPA objetivo sin ventas. Escalar si el CPA es menor al ticket medio.

**Fase 2: Escala (desde el día 15)**
- Campaña **Advantage+ de Compras** con los 5 anuncios ganadores.
- Subir el presupuesto un 20-30% cada 48 h si el ROAS es mayor a 1,5.
- Expandir a 🇲🇽 México, 🇨🇴 Colombia, 🇨🇱 Chile, 🇵🇪 Perú y 🇺🇸 hispanos (versión en español neutro y precio en USD).

**Fase 3: Remarketing (siempre activo, 10-15% del presupuesto)**
- Visitas de la landing en los últimos 7 días → testimonios + garantía.
- Checkout iniciado → "Te guardamos el precio 24 h".

### 7.3 Ángulos creativos (10 ganchos para los primeros 3 segundos)
1. "Mi pareja y yo llevábamos 8 años… hasta que probamos esto 👇"
2. "POV: sacás una carta y tu pareja se pone roja 😳"
3. "No es falta de amor. Es falta de juego."
4. "El regalo de aniversario que NO es un perfume"
5. "Carta nivel rojo: ¿se animan?" (reacción de una pareja)
6. "Dejen el celular. Bueno, úsenlo para ESTO."
7. "30 noches, 30 retos. Noche 1:…"
8. "Lo que me recomendó mi terapeuta de pareja" (solo si es real)
9. "3 juegos para esta noche que no cuestan nada" (valor → CTA)
10. "Probamos el juego de pareja que todos están comprando"

**Formatos:**
- **UGC**: 60% del presupuesto. Parejas reales o creadores de Billo o Collabstr, video vertical de 15-30 s con reacción.
- **Estáticos**: mockup + beneficio + precio.
- **Carrusel**: "Carta 1, Carta 2, Carta 3…".
- **Demo de la app** grabando la pantalla.

**Producción:** 15-20 creatividades iniciales y 5 nuevas por semana. La fatiga creativa es el principal enemigo.

### 7.4 Orgánico (TikTok, Instagram y Pinterest)
- Cuenta de marca + 1 o 2 cuentas "de pareja" (personajes reales).
- 1-2 videos diarios: "carta del día", retos, reacciones, preguntas de *Conexión* (son las más virales y seguras).
- Pinterest: pines de "ideas de cita en casa" y "regalos para mi novio", que generan tráfico duradero.
- Enlace en la bio a la landing con UTM.

### 7.5 Influencers y afiliados
- Microinfluencers de pareja y estilo de vida (10-100 mil seguidores): canje + código con comisión.
- **Hotmart Afiliados** con comisión del 50-60% en el producto principal. Darles un kit con creatividades, textos y reglas de Meta.
- Psicólogos y sexólogos en Instagram: alianza de contenido + comisión.

### 7.6 Email y WhatsApp
**Secuencia posterior a la compra:**
- D0: acceso + cómo empezar (nivel 🟢).
- D1: "¿Ya sacaron la primera carta?"
- D3: tips del reto de 30 noches.
- D5: oferta del Pack Fantasías.
- D7: pedido de testimonio a cambio de un bono extra.
- D14 y D30: recompra o suscripción.

**Carrito abandonado:** emails a los 30 min, 24 h y 48 h (el último con un bono extra). WhatsApp opcional con consentimiento.

**Lead magnet** para captar emails sin compra: "5 cartas gratis del nivel Conexión" (PDF) → secuencia de 5 emails → oferta.

### 7.7 SEO y contenido (posicionamiento a mediano plazo)
Blog en el mismo dominio con 2 artículos por semana. Palabras clave de cola larga (validar volumen con Semrush):
- "juegos para parejas en casa", "retos para parejas", "preguntas para parejas",
- "ideas para una cita en casa", "cómo recuperar la pasión en la pareja",
- "regalo original para mi novio/novia", "juegos de pareja para San Valentín",
- "cartas para parejas imprimibles".

Cada artículo ofrece valor real + CTA al lead magnet y al producto. Agregar schema de Producto y de Preguntas frecuentes. Conseguir enlaces con guest posts en blogs de bienestar.

### 7.8 Calendario estacional (picos de venta)
- **14 de febrero (San Valentín):** el pico del año. Empezar a calentar el 20 de enero.
- **Día de los Enamorados en Argentina, 3.ª semana de septiembre** (y en Brasil el 12/6).
- **Black Friday / Cyber Monday** (noviembre).
- **Fiestas de fin de año:** "regalo para tu pareja".

---

## 8. Métricas objetivo (KPI)

| Métrica | Objetivo |
|---|---|
| CTR del anuncio (enlace) | > 1,5% |
| CPC | < USD 0,25 (AR) |
| Conversión de la landing | 2-4% |
| Conversión del bump | 30-40% |
| Conversión del upsell | 10-15% |
| CPA | < ticket medio (≈ USD 9-10) |
| ROAS | ≥ 1,5 para mantener, ≥ 2 para escalar |
| Reembolsos | < 5% |

**Economía de la unidad (ejemplo):** ticket USD 10 − comisión de la plataforma (~10%) − impuestos (~5%) = **USD 8,5 netos**. Con un CPA de USD 6 queda **USD 2,5 de ganancia por venta** en la primera compra; la ganancia real está en la escala, los upsells, la recompra y el orgánico.

---

## 9. Entrega del producto (automatizada)

1. Pago aprobado → Hotmart o el webhook dispara la entrega.
2. Email inmediato con: (a) enlace al área de miembros, (b) PDF con marca de agua, (c) **código de acceso a la app** + botón "Instalar en mi celular".
3. La app valida el código contra Supabase (máximo 2 dispositivos por código, uno por cada miembro de la pareja).
4. Soporte por WhatsApp Business y email con respuestas guardadas (no llegó el email, cómo instalar en iPhone, reembolso).

---

## 10. Cuestiones legales y operativas (Argentina)
- Inscripción en **ARCA (ex AFIP)** como monotributista o responsable inscripto, y factura electrónica (Hotmart factura su comisión, pero la venta es tuya).
- Términos y condiciones, política de privacidad (Ley 25.326), aviso +18 y **Botón de arrepentimiento**.
- Registro de la marca en el **INPI** (clase 16 para impresos/PDF, 9 para la app y 41 para entretenimiento).
- Descriptor de cobro neutro (privacidad del cliente).
- Revisión de contenido: consentimiento explícito, nada que involucre a terceros o sustancias, lenguaje inclusivo.

---

## 11. Hoja de ruta (6 semanas)

| Semana | Entregables |
|---|---|
| 1 | Validar la competencia (§13), elegir nombre, dominio y marca, y redactar el 100% del contenido |
| 2 | Revisión profesional, diseño del PDF y mockups |
| 3 | App PWA (MVP), landing, checkout y emails automatizados, pixel + API de Conversiones |
| 4 | **Preventa suave** a una lista o al orgánico a un precio especial → primeros 20-50 testimonios. Grabar 15-20 creatividades |
| 5 | Lanzamiento en Meta (fase de testeo) + TikTok orgánico diario |
| 6 | Escala de ganadores, remarketing, afiliados y primeros artículos de SEO |
| 7+ | Expansión a LATAM, Pack Fantasías, suscripción en la app y versión física (cartas impresas) |

## 12. Presupuesto inicial estimado
| Rubro | USD |
|---|---|
| Dominio + hosting + herramientas (primer mes) | 50-80 |
| Revisión profesional del contenido | 100-200 |
| Diseño (si se terceriza) | 150-300 |
| UGC (8-10 videos) | 150-400 |
| Anuncios de testeo (14 días) | 300-450 |
| **Total para arrancar** | **≈ 750-1.400** |

---

## 13. Pendientes y preguntas abiertas
- **Validar los sitios de referencia** desde un navegador común: precio exacto, contenido, bonos, checkout que usan, testimonios. Se puede revisar la **Biblioteca de anuncios de Meta** (facebook.com/ads/library) buscando "impultienda", "La Chispa Secreta" y "El Juego del Deseo" para ver sus creatividades activas y cuánto tiempo llevan corriendo (si un anuncio tiene más de 30 días activo, es rentable).
- Definir: ¿solo Argentina al principio o LATAM desde el día 1?
- Definir: ¿Hotmart (más rápido) o checkout propio (más margen)?
- Elegir el nivel de picante del producto (afecta la marca y los anuncios).
