FROM node:carbon-slim

RUN apt-get update && apt-get install -y git && apt-get clean
ENV NODE_ENV=production
COPY package.json .
RUN npm install --only=prod && npm install --only=dev && npm cache clean --force

CMD ["node"]
