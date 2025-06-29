FROM node:16-alpine

WORKDIR /app

# Copiar package.json e instalar dependências
COPY package*.json ./
RUN npm install

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 5173

# Comando para executar em desenvolvimento
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"] 