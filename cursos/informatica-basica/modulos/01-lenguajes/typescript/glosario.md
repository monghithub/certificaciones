# Glosario: TypeScript

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## E

- **Eliminación de tipos** (type stripping, strip-types). *Técnica.* Forma en que Node.js ejecuta ficheros .ts: sustituye la sintaxis de tipos por espacios, sin comprobarlos. Solo admite sintaxis borrable (no enum, por ejemplo).
  - Referencia: <https://nodejs.org/api/typescript.html>
- **Estrechamiento** (narrowing). *Técnica.* Reducción del tipo de una variable dentro de un bloque gracias a una comprobación (typeof, ===, in), de modo que el compilador sabe qué tipo concreto tiene.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/2/narrowing.html>

## G

- **Genéricos** (generics, keyof). *Concepto.* Tipos y funciones parametrizados por otros tipos (function primero<T>(lista: T[])), con restricciones como K extends keyof T.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/2/generics.html>

## N

- **never**. *Concepto.* Tipo sin valores posibles. Asignar a never lo que queda tras tratar todos los casos de una unión hace que el compilador avise si falta alguno.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/2/narrowing.html>

## S

- **satisfies**. *Herramienta.* Operador que comprueba que un valor cumple un tipo sin cambiar el tipo inferido del valor.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html>

## T

- **Tipado estructural** (structural typing). *Concepto.* Dos tipos son compatibles si tienen la misma forma (las mismas propiedades), sin importar su nombre ni si se declararon relacionados.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/type-compatibility.html>
- **Tipo unión** (union type, uniones). *Concepto.* Tipo que admite uno de varios tipos, como string | number.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/2/everyday-types.html>
- **Tipos utilitarios** (utility types, Partial, Pick, Omit, Record, Readonly). *Herramienta.* Tipos incluidos en TypeScript que derivan uno nuevo de otro: Partial, Pick, Omit, Record, Readonly…
  - Referencia: <https://www.typescriptlang.org/docs/handbook/utility-types.html>
- **tsc** (compilador de TypeScript). *Herramienta.* Compilador y comprobador de tipos de TypeScript. Desde TypeScript 7 es una versión nativa escrita en Go, unas diez veces más rápida.
  - Referencia: <https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/>
- **tsconfig.json** (strict, noUncheckedIndexedAccess). *Herramienta.* Fichero de configuración del compilador de TypeScript: módulos, rigor de la comprobación y ficheros incluidos.
  - Referencia: <https://www.typescriptlang.org/tsconfig/>
- **TypeScript**. *Lenguaje.* Lenguaje que añade tipos estáticos a JavaScript. Los tipos se comprueban al compilar y se borran: lo que se ejecuta es JavaScript.
  - Referencia: <https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/>

## U

- **Unión discriminada** (discriminated union). *Patrón.* Unión de objetos que comparten una propiedad literal (por ejemplo, tipo) cuyo valor indica de qué caso se trata.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/2/narrowing.html>
- **unknown** (any). *Concepto.* Tipo de un valor desconocido que obliga a comprobarlo antes de usarlo; a diferencia de any, no desactiva la comprobación de tipos.
  - Referencia: <https://www.typescriptlang.org/docs/handbook/2/everyday-types.html>

## Z

- **Zod** (z.infer, safeParse). *Herramienta.* Biblioteca de validación en ejecución para TypeScript: un esquema valida datos externos y de él se deduce el tipo estático con z.infer.
  - Referencia: <https://zod.dev/basics>
