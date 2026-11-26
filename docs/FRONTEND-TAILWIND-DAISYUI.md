# Frontend Modernizado: Tailwind CSS + DaisyUI

## 🎨 ¿Qué cambió?

Se ha reemplazado el sistema CSS personalizado por **Tailwind CSS + DaisyUI**, una combinación moderna que ofrece:

- ✨ **Componentes predefinidos** (botones, tarjetas, modales, dropdowns, etc.)
- 🎯 **Diseño responsive** automático
- 🌙 **Soporte de temas** (claro/oscuro)
- 📱 **Mobile-first** por defecto
- 🚀 **Desarrollo más rápido** (clases utilitarias)

---

## 📦 Instalación y Build

### Instalar dependencias

```bash
cd ~/Cursos/certificaciones
npm install
```

### Compilar CSS

```bash
npm run build:css      # Compilación única
npm run watch:css      # Modo watch (para desarrollo)
```

Esto genera `app/static/app.css` a partir de `app/static/input.css`.

---

## 🧩 Componentes Disponibles

### Botones

```html
<!-- Primario -->
<button class="btn btn-primary">Botón primario</button>

<!-- Secundario -->
<button class="btn btn-secondary">Botón secundario</button>

<!-- Outline -->
<button class="btn btn-outline">Outline</button>

<!-- Fantasma -->
<button class="btn btn-ghost">Fantasma</button>

<!-- Peligro -->
<button class="btn btn-error">Peligro</button>

<!-- Éxito -->
<button class="btn btn-success">Éxito</button>

<!-- Tamaños -->
<button class="btn btn-lg">Grande</button>
<button class="btn btn-md">Normal</button>
<button class="btn btn-sm">Pequeño</button>
<button class="btn btn-xs">Micro</button>

<!-- Con icono -->
<button class="btn">
  ⬇️ Descargar
</button>
```

### Tarjetas

```html
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Título</h2>
    <p>Contenido aquí</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Acción</button>
    </div>
  </div>
</div>
```

### Alertas

```html
<!-- Éxito -->
<div class="alert alert-success">
  <svg class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
  <span>¡Operación exitosa!</span>
</div>

<!-- Error -->
<div class="alert alert-error">
  <svg class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4v2m0 0a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
  <span>¡Algo salió mal!</span>
</div>

<!-- Warning -->
<div class="alert alert-warning">
  <span>⚠️ Advertencia</span>
</div>

<!-- Info -->
<div class="alert alert-info">
  <span>ℹ️ Información</span>
</div>
```

### Modales

```html
<!-- Trigger button -->
<button class="btn" onclick="my_modal_1.showModal()">Abrir modal</button>

<!-- Modal -->
<dialog id="my_modal_1" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Título</h3>
    <p class="py-4">Contenido del modal</p>
    <div class="modal-action">
      <form method="dialog">
        <button class="btn">Cerrar</button>
      </form>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
```

### Dropdowns

```html
<div class="dropdown">
  <button tabindex="0" class="btn m-1">Menú</button>
  <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
    <li><a>Opción 1</a></li>
    <li><a>Opción 2</a></li>
  </ul>
</div>
```

### Formularios

```html
<input type="text" placeholder="Nombre" class="input input-bordered w-full max-w-md" />

<textarea class="textarea textarea-bordered w-full" placeholder="Mensaje"></textarea>

<select class="select select-bordered w-full max-w-md">
  <option disabled selected>Elige una opción</option>
  <option>Opción 1</option>
  <option>Opción 2</option>
</select>

<label class="form-control w-full max-w-md">
  <div class="label">
    <span class="label-text">¿Cuál es tu nombre?</span>
  </div>
  <input type="text" placeholder="Escribe aquí" class="input input-bordered w-full" />
</label>
```

### Badges

```html
<span class="badge">Défault</span>
<span class="badge badge-primary">Primario</span>
<span class="badge badge-secondary">Secundario</span>
<span class="badge badge-success">Éxito</span>
<span class="badge badge-error">Error</span>
<span class="badge badge-warning">Aviso</span>
<span class="badge badge-info">Info</span>

<!-- Con icono -->
<span class="badge badge-lg">
  AWS ✓
</span>
```

### Grid/Layout

```html
<!-- Grid automático -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Columna 1</div>
  <div>Columna 2</div>
  <div>Columna 3</div>
</div>

<!-- Flexbox -->
<div class="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

---

## 🌙 Temas

DaisyUI incluye temas predefinidos. Los disponibles son:

- `light`
- `dark`
- Y muchos más: nord, dracula, cyberpunk, etc.

Cambiar de tema dinámicamente:

```javascript
document.documentElement.setAttribute('data-theme', 'dark');
```

---

## 🎯 Clases Tailwind Comunes

| Clase | Uso |
|---|---|
| `container` | Contenedor máximo ancho (1280px) |
| `mx-auto` | Márgenes horizontales automáticos (centra) |
| `px-4`, `py-6` | Padding horizontal/vertical |
| `mb-4`, `mt-2` | Margen abajo/arriba |
| `text-xl`, `text-sm` | Tamaños de texto |
| `font-bold`, `font-semibold` | Pesos de fuente |
| `text-primary`, `text-error` | Colores de texto |
| `bg-base-100`, `bg-primary` | Colores de fondo |
| `border`, `rounded-lg` | Borde y esquinas |
| `shadow-lg`, `shadow-md` | Sombras |
| `flex`, `grid` | Layouts |
| `gap-4` | Espaciado entre items |
| `hidden`, `md:flex` | Responsive (oculto en móvil, visible en desktop) |

---

## 📱 Responsive

Tailwind usa breakpoints:

- `sm:` (640px)
- `md:` (768px)
- `lg:` (1024px)
- `xl:` (1280px)
- `2xl:` (1536px)

Ejemplo:

```html
<!-- Oculto en móvil, visible en md+ -->
<div class="hidden md:block">
  Visible solo en desktop
</div>

<!-- 1 columna en móvil, 2 en md, 3 en lg -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  ...
</div>
```

---

## 🔄 Migración desde CSS antiguo

### Antes (CSS personalizado)

```html
<button class="btn">Presionar</button>
```

### Ahora (Tailwind + DaisyUI)

```html
<button class="btn btn-primary">Presionar</button>
```

La mayoría de las clases antiguas siguen funcionando porque están mapeadas en `input.css`.

---

## 🎨 Personalización

Editar `tailwind.config.js` para:

- Agregar colores propios
- Cambiar temas
- Extender funcionalidad

Editar `app/static/input.css` para:

- Agregar clases personalizadas
- Personalizar componentes
- Sobrescribir estilos

---

## 🛠️ Desarrollo

### Recomendaciones

1. **Usa clases utilitarias** en lugar de CSS personalizado siempre que sea posible
2. **Naming semántico**: `btn-primary` vs `blue-button`
3. **Componentes reutilizables**: crea macros en Jinja2
4. **Responsive first**: diseña para móvil primero, luego expande

### Crear componente reutilizable

Archivo: `app/templates/_componentes.html`

```html
{%- macro card(titulo, contenido) -%}
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">{{ titulo }}</h2>
    <p>{{ contenido }}</p>
  </div>
</div>
{%- endmacro -%}
```

Usar en template:

```html
{% from "_componentes.html" import card %}

{{ card("Mi título", "Mi contenido") }}
```

---

## 🚀 Próximos pasos

- Reorganizar templates antiguos para usar DaisyUI
- Crear biblioteca de macros para componentes comunes
- Mejorar dashboard de estadísticas
- Agregar iconos de Heroicons (ya incluidos en base.html)

---

## 📚 Recursos

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [DaisyUI Docs](https://daisyui.com/docs/install/)
- [Heroicons](https://heroicons.com/)

---

## 🤝 Integración con HTMX

Tailwind + DaisyUI funciona perfecto con HTMX. Ejemplo:

```html
<button class="btn btn-primary" hx-get="/endpoint" hx-target="#resultado">
  Cargar datos
</button>

<div id="resultado"></div>
```

¡Ningún cambio especial necesario! Los estilos se aplican automáticamente.

