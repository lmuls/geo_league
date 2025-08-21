FROM node:16-alpine as build
WORKDIR /app
COPY . .
ENV REACT_APP_DATABASE_URL=/api

RUN apk add --no-cache python3 make g++ \
    && npm config set python python3
RUN npm ci
RUN npm run build
# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]