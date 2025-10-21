FROM node:18-alpine

WORKDIR /app

# Copiar dependencias
COPY package.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

RUN npm install

# Copiar el resto del código
COPY . .

# Compilar Tailwind (opcional)
RUN npx tailwindcss -i ./app/globals.css -o ./public/output.css --minify || true

# Importante: Next.js no usa --host
ENV HOST 0.0.0.0
EXPOSE 3000

CMD ["npm", "run", "dev"]
