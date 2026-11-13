# Modo publicación

Para vender el libro. Objetivo: de 3 a 7 intercambios. El usuario elige **dónde** vende; tú resuelves el formato.

## Preguntas del primer turno (todas juntas)

1. ¿Dónde lo vas a vender? (KDP, IngramSpark, Lulu, B&N Press, Etsy)
2. ¿Título y nombre de autor para la portada?
3. ¿Cuántos dibujos? (propón 30-50 en imprenta, 20-30 en Etsy)
4. ¿Una cara por hoja? (recomendado: evita que el rotulador traspase)

## Qué resuelve la herramienta por ti

| Tema | Comportamiento |
|---|---|
| Tamaño | El de `--trim` o el habitual de la plataforma (8.5x11) |
| Una cara | Cada dibujo en página derecha con reverso en blanco (`--double-sided` lo desactiva) |
| Mínimo de páginas | Rellena con blancos hasta el mínimo y hasta número par; `build` avisa si sobran muchos |
| Margen interior | Crece con el número de páginas según la tabla de la plataforma |
| Cubierta | Un PDF: contraportada + lomo + portada, con sangrado; lomo calculado por páginas y papel |
| Texto en el lomo | Solo si el libro tiene suficientes páginas |
| Código de barras | Zona blanca reservada en la contraportada |
| Etsy | Sin lomo ni sangrado: un PDF con la portada como primera página |

## Flujo

1. `init --mode publishing --platform <p> --author ...` → plan → 3 muestras.
2. Estilo aprobado → lote completo + `cover --blurb "texto de contraportada"`.
3. Revisión de páginas con avisos (`status`) y correcciones del usuario.
4. `build` → entrega **interior** y **cubierta** y repite al usuario las `warnings` tal cual.

## Lo que debes decirle al usuario al entregar

- Número final de páginas, tamaño y ancho de lomo.
- Si `verify_specs` es verdadero (IngramSpark, Lulu, B&N): que confirme lomo y márgenes con la plantilla oficial antes de subir.
- Que declare el contenido generado con IA si la plataforma lo pide, y que el ISBN lo gestiona la plataforma o él mismo.
