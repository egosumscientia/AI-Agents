export const RECIPES = [
  { id: 1, title: 'Brócoli asado con miso', ingredients: ['brócoli', 'miso', 'ajo'], tags: ['+umami', 'crujiente'], v: [0.1, 0.5, 0.2, 0.1, 0.85, 0.2, 0.7] },
  { id: 2, title: 'Curry de garbanzos', ingredients: ['garbanzos', 'curry', 'tomate'], tags: ['picante', '+umami'], v: [0.25, 0.45, 0.3, 0.1, 0.65, 0.6, 0.2] },
  { id: 3, title: 'Ensalada cítrica', ingredients: ['quinoa', 'naranja', 'menta'], tags: ['ácido alto', 'fresco'], v: [0.2, 0.35, 0.8, 0.1, 0.25, 0.1, 0.2] },
  { id: 4, title: 'Pollo al limón y hierbas', ingredients: ['pollo', 'limón', 'romero'], tags: ['ácido medio', 'bajo dulce'], v: [0.1, 0.5, 0.6, 0.1, 0.4, 0.1, 0.4] },
  { id: 5, title: 'Tofu glaseado teriyaki', ingredients: ['tofu', 'teriyaki', 'jengibre'], tags: ['dulce-salado', '+umami'], v: [0.55, 0.6, 0.2, 0.1, 0.8, 0.15, 0.3] },
  { id: 6, title: 'Tacos de pescado', ingredients: ['pescado', 'tortillas', 'tomate', 'chile'], tags: ['fresco', 'picante medio', 'crujiente'], v: [0.15, 0.55, 0.35, 0.1, 0.5, 0.45, 0.5] },
];

export function getRecipes() { return RECIPES; }
