FROM node:18-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 5173

# Usamos --host para que Docker exponga la IP
CMD ["npm", "run", "dev", "--", "--host"]