# 🍴 TasteBuddy – MVP React Native (Expo Offline, JSX)

Asistente de sabor personalizado para validar con usuarios reales, **sin backend**.

## 🚀 Arranque rápido
```bash
npm install
npx expo start
```
Abre en web o usa **Expo Go** en tu teléfono.

## 📁 Estructura
- `app/App.js` – Entry point
- `app/screens/*` – Onboarding, Radar, Recipes, Feedback
- `app/components/*` – RadarChart, RecipeCard, Button, Chip
- `app/hooks/useTasteProfile.js` – Estado + lógica de perfil
- `app/utils/math.js` – cosine + EWMA
- `app/data/recipes.js` – Recetas simuladas
- `app/styles/*` – theme + estilos globales

## 🧠 Recomendador
`score = 0.75 * cosine(vUser, vRecipe) + 0.25 * matching(ingredientes)`  
Feedback 1–5 actualiza el perfil con EWMA (`α=0.35`).

## 🧩 Roadmap
- Backend FastAPI (opcional)
- API real de recetas
- Planificador semanal (anti-fatiga)
