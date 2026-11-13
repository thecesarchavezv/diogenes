# Modo cuento

Convierte una historia en un cuento para colorear. Objetivo: 6 intercambios o más.

## Flujo

1. **Historia.** Acepta lo que traiga (una idea, un borrador, un texto largo). Resume y adapta a 10-16
   escenas. Enseña el guion como tabla (página · qué se ve · texto) y espera el visto bueno.
2. **Personajes.** Escribe una ficha fija por personaje (especie, tamaño, ropa, rasgo distintivo).
   Esa ficha va en `characters` y la herramienta la repite literal en todas las páginas.
3. **Muestras.** Genera 2 páginas con personajes. La primera generación crea además una hoja de
   personajes (`refs/characters.png`) que se usa como referencia visual en el resto.
4. **Libro.** Aprobado el aspecto, genera todo + portada.
5. **Coherencia.** Revisa que cada personaje se vea igual en todas las páginas; rehaz las que no.
6. **PDF.** `build`.

## Reglas del guion

- Una acción clara por página; el dibujo debe entenderse sin leer el texto.
- Texto de página (`caption`): 1-2 frases, máximo unas 25 palabras, en el idioma del usuario.
- En `prompt` describe la escena en inglés y nombra a los personajes por su nombre de la ficha.
- El texto se tipografía bajo la ilustración. Solo si el usuario quiere letras dibujadas dentro de la
  imagen, pon `"text_mode": "in_image"` en el plan y revisa la ortografía de cada página.
- Si cambia el aspecto de un personaje: edita su ficha, borra `character_sheet` de `book.json` y usa
  `style --set "<mismo estilo>" --redo`.
- Para publicar el cuento, usa `--mode storybook` junto con `--platform kdp` (u otra): se aplican las
  mismas reglas de formato del modo publicación.
