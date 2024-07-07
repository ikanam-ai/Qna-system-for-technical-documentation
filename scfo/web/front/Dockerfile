FROM node:20-alpine

ARG VITE_HOST
ENV VITE_HOST=$VITE_HOST

RUN npm install -g pnpm

WORKDIR /app

COPY . ./

RUN pnpm install

RUN pnpm build

EXPOSE 4173

CMD [ "pnpm", "preview", "--host" ]
