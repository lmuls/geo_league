FROM node:16-alpine as build
WORKDIR /app
COPY . .
ENV REACT_APP_DATABASE_URL=http://deplo-loadb-50h0hx1kbfw1-4c9f648e705d62b7.elb.us-east-1.amazonaws.com:8000
RUN npm ci
RUN npm run build
# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]