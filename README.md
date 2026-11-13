# Diogenes: creador de libros para colorear

Paquete de agente que reproduce las capacidades analizadas: dibujos para colorear, portada a juego y
PDF listo para imprimir o publicar, en tres modos (estándar, publicación, cuento).

## Cómo está hecho el agente original y qué replica cada pieza

| Capacidad observada | Pieza de este paquete |
|---|---|
| LLM que conversa y planifica | [SKILL.md](SKILL.md): instrucciones del agente, válidas para cualquier LLM con ejecución de comandos |
| Tres modos con presupuesto de intercambios | [modes/](modes/): un guion turno a turno por modo |
| Generación de páginas con API de imágenes | `colorbook/imagegen.py` + `colorbook/prompts.py` |
| Imagen de referencia para definir el estilo | `init --reference` → endpoint de edición con la referencia |
| Estilo uniforme en todo el libro | `style_lock` y preset de audiencia repetidos en cada prompt |
| Personajes que mantienen su aspecto | Ficha de personaje literal + hoja de personajes como referencia visual |
| Muestras → revisión → libro completo | `generate --pages`, `revise`, `style --redo` |
| Portada a juego | `cover`: ilustración a color, título tipografiado |
| PDF listo para imprimir | `colorbook/pdf.py`: interior a 300 ppp |
| Formato por plataforma | [config/platforms.json](config/platforms.json): tamaños, mínimos, márgenes, lomo |
| Reverso en blanco | `single_sided` (activado por defecto) |
| Claves del lado del desarrollador | `.env`: el usuario final nunca introduce credenciales |

Añadidos respecto al original: limpieza a blanco y negro puro, control de calidad automático por
página (color, grises, exceso de negro) y PDF de cubierta completa con lomo y zona de código de barras.

## Las dos discrepancias de la revisión, corregidas

[agent.json](agent.json) es la ficha pública. Declara `api.openai.com` y qué datos recibe, y separa el
modelo orquestador del modelo de imagen, que en el original aparecían mezclados u omitidos.

## Uso

```bash
pip install -r requirements.txt
```

```bash
cp .env.example .env
```

Prueba completa sin API ni coste (dibujos de relleno):

```bash
python -m colorbook init projects/demo --title "Animales adorables" --platform kdp --author "Tu Nombre"
```

```bash
python -m colorbook plan projects/demo --file plan.example.json
```

```bash
python -m colorbook generate projects/demo --mock
```

```bash
python -m colorbook cover projects/demo --mock
```

```bash
python -m colorbook build projects/demo
```

Quita `--mock` y exporta `OPENAI_API_KEY` para generar ilustraciones reales.

Para usarlo como skill de Claude Code, copia esta carpeta a `.claude/skills/coloring-book-maker/`.
En otra plataforma de agentes, carga `SKILL.md` como instrucciones y expón `python -m colorbook` como herramienta.

## Estado de las pruebas

- Probado de punta a punta en modo `--mock`: los tres modos, KDP y Lulu, tamaños y número de páginas de los PDF.
- **No probado contra la API real de OpenAI** (no había clave en el entorno de construcción).
- Medidas de imprenta revisadas en noviembre de 2026; el detalle de qué se confirmó está en el campo
  `checked` de cada plataforma en [config/platforms.json](config/platforms.json).
  - **KDP:** leído directamente en sus páginas de ayuda el 13 de noviembre de 2026; todo coincide.
  - **Lulu:** confirmado salvo la tabla de medianil, que varía entre versiones de su guía.
  - **IngramSpark y B&N Press:** no publican fórmula de lomo; `build` avisa de usar su plantilla oficial.
