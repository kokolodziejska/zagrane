FROM node:20-bullseye
WORKDIR /app

# zainstaluj zależności
COPY package*.json package-lock.json ./
RUN npm install

# reszta źródeł
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
