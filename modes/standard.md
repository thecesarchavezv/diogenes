# Modo estándar

Para libros de casa, clase o regalo. Objetivo: de 2 a 5 intercambios.

| Turno | Tú haces |
|---|---|
| 1 | Con la idea del usuario: `init --platform personal`, plan de 8-12 escenas, generas **3 muestras** y las enseñas. Pregunta solo: ¿te gusta el estilo? ¿cuántas páginas? |
| 2 | Ajustas (`style --set ... --redo` o `revise`) o, si aprueba, generas el resto + `cover`. |
| 3 | Enseñas el libro completo. Corriges páginas sueltas con `revise --page N --note`. |
| 4 | `build` y entregas el PDF. |

Valores por defecto si no dice nada: 12 páginas, `kids_4_8`, carta (8.5x11), una cara.
Si el usuario es de un país con A4, usa `--trim A4`.

Peticiones habituales y cómo traducirlas:

- «líneas más gruesas» / «más sencillo» → baja una audiencia (`kids_4_8` → `toddlers_2_4`) o añade la nota al `style_lock`.
- «fondos más simples» → añade «minimal background» al `style_lock` y usa `--redo`.
- Sube una imagen de referencia → `init --reference` (o cópiala a `refs/` y añádela a `references` en `book.json`).
