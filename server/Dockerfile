# Answering the Dark — share-code relay
FROM node:22-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY relay.js ./
COPY demo.mp4 ./
ENV PORT=8080
EXPOSE 8080
CMD ["node", "relay.js"]
