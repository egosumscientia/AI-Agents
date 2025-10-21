# Imagen base
FROM node:18-alpine

WORKDIR /app

# Copia los archivos base
COPY package.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

RUN npm install

# Copia el resto del código
COPY . .

# Compila Tailwind y genera los estilos
RUN npx tailwindcss -i ./app/globals.css -o ./public/output.css --minify || true

EXPOSE 3000

CMD ["npm", "run", "dev"]
