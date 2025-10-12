# 🍴 TasteBuddy – MVP React Native (Expo Offline, JSX)

Asistente de sabor personalizado con IA local, desarrollado con **React Native + Expo** para validación rápida con usuarios reales.

---

## 🚀 Características principales

- Perfil de sabor dinámico (7 dimensiones: Dulce, Salado, Ácido, Amargo, Umami, Picante, Crujiente).
- Radar de sabor visual (SVG interactivo).
- Recomendaciones locales basadas en similitud coseno e ingredientes disponibles.
- Sistema de feedback adaptativo con actualización EWMA.
- Modo **100% offline** (sin backend).
- Persistencia local con AsyncStorage.
- Estructura modular (componentes, hooks, pantallas, estilos).
- Listo para publicación en **GitHub / Expo Web**.

---

## 🧩 Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- [Node.js ≥ 18](https://nodejs.org)
- npm ≥ 9 o [Yarn](https://yarnpkg.com/)
- [Expo CLI](https://docs.expo.dev/get-started/installation/)

Instálalo con:

```bash
npm install -g expo-cli
```

---

## 📦 Instalación

1️⃣ **Descarga o clona el proyecto:**

```bash
git clone https://github.com/tu-usuario/tastebuddy-mvp-jsx.git
cd tastebuddy-mvp-jsx
```

(Si descargaste el ZIP, simplemente descomprímelo y entra a la carpeta).

2️⃣ **Instala las dependencias:**

```bash
npm install
```

---

## 🧠 Estructura del proyecto

```
tastebuddy-mvp-jsx/
├── app/
│   ├── App.js                 # Punto de entrada principal
│   ├── screens/               # Pantallas principales
│   │   ├── OnboardingScreen.js
│   │   ├── RadarScreen.js
│   │   ├── RecipesScreen.js
│   │   └── FeedbackScreen.js
│   ├── components/            # UI reutilizable (Button, Chip, RadarChart, RecipeCard)
│   ├── hooks/                 # Lógica del perfil (useTasteProfile)
│   ├── utils/                 # Funciones matemáticas (cosine, ewmaUpdate)
│   ├── data/                  # Dataset local de recetas
│   ├── storage/               # Persistencia local (AsyncStorage)
│   └── styles/                # Estilos globales y tema
│
├── assets/                    # Íconos y splash (placeholders)
├── package.json               # Dependencias y scripts
├── babel.config.js            # Configuración de alias
├── metro.config.js            # Configuración Metro bundler
├── .eslintrc.js / .prettierrc # Linter y formato
├── .gitignore / .eslintignore # Exclusiones
└── README.md                  # Documentación
```

---

## ⚙️ Ejecución local

### 1️⃣ Inicia el entorno Expo

```bash
npx expo start
```

Esto abrirá Expo Developer Tools en tu navegador.  
Desde ahí puedes ejecutar la app de tres formas:

| Plataforma | Comando | Descripción |
|-------------|----------|-------------|
| **Web** | `w` | Abre la app en el navegador |
| **Android** | `a` | Abre en emulador o Expo Go |
| **iOS** | `i` | Abre en simulador o Expo Go |

---

## 📱 Flujo de uso

1. Inicia la app y completa el **quiz de sabores**.
2. Visualiza tu **Radar de sabor personalizado**.
3. En la sección **Recetas**, escribe ingredientes (por ejemplo: `pollo, limón`).
4. TasteBuddy recomendará platos basados en tu perfil e inventario.
5. Califica una receta (1–5 estrellas) → tu perfil se ajusta dinámicamente.

El perfil se guarda automáticamente en **AsyncStorage**, por lo que se conservará al reiniciar.

---

## 🧠 Lógica de IA local

### Vector de usuario

Cada usuario tiene un vector `vUser ∈ [0,1]^7` que representa su gusto.

### Similaridad de receta

Cada receta tiene un vector `vRecipe`.  
Se calcula la compatibilidad con:

```
score = 0.75 * cosine(vUser, vRecipe) + 0.25 * ingredient_match
```

### Feedback adaptativo

Al calificar (1–5), el perfil se actualiza mediante promedio exponencial (EWMA):

```
vUser_new = EWMA(vUser, vRecipe, rating)
α = 0.35 (peso reciente)
```

Esto simula un aprendizaje progresivo del gusto del usuario.

---

## 🧪 Validación con usuarios reales

Flujo sugerido para pruebas de validación:

| Paso | Acción del usuario | Resultado |
|------|--------------------|------------|
| 1 | Completa el quiz inicial | Se genera el perfil inicial |
| 2 | Observa el radar | Visualiza preferencias personales |
| 3 | Escribe ingredientes | Recibe recomendaciones adaptadas |
| 4 | Califica una receta | Perfil ajustado automáticamente |
| 5 | Observa cambios en el radar | IA evoluciona según gusto |

Preguntas recomendadas para feedback cualitativo:
- “¿Las sugerencias coincidieron con tus gustos?”  
- “¿El radar refleja tu estilo culinario?”  
- “¿Cambiarías algo de las recomendaciones?”

---

## 🧩 Comandos útiles

| Comando | Descripción |
|----------|--------------|
| `npm run lint` | Ejecuta ESLint para revisar estilo de código |
| `npm run web` | Inicia directamente en modo web |
| `npm run android` | Lanza en emulador Android |
| `npm run ios` | Lanza en emulador iOS |

---

## 💡 Publicación en GitHub Pages (Expo Web)

1. Asegúrate de tener instalado `gh-pages`:
```bash
npm install --save-dev gh-pages
```

2. Agrega a tu `package.json`:
```json
"homepage": "https://<tu-usuario>.github.io/tastebuddy-mvp-jsx"
```

3. Publica:
```bash
npx expo export:web
npx gh-pages -d dist
```

---

## 🧩 Roadmap evolutivo

| Fase | Objetivo | Descripción |
|------|-----------|-------------|
| 1 | Conectar Backend (FastAPI) | Recomendaciones dinámicas multiusuario |
| 2 | API real de recetas | Dataset etiquetado por sabor |
| 3 | Planificador semanal | Evitar fatiga de sabor |
| 4 | Maridaje IA | Combinar vinos y comidas |
| 5 | Integración con wearables | IA contextual (humor, clima, etc.) |

---

## 🧰 Stack técnico

| Capa | Tecnología |
|------|-------------|
| Frontend | React Native (Expo) |
| Estado persistente | AsyncStorage |
| Gráficos | react-native-svg |
| Linter/Formato | ESLint + Prettier |
| Lenguaje | JavaScript (JSX) |

---

## 📄 Licencia

MIT © 2025 — Desarrollado por **makeAutomatic Lab** 🧠⚙️  
Enfocado en innovación en **IA aplicada a la automatización y la experiencia sensorial**.

---
