FROM node:10-buster-slim
# timezone environment
ENV TZ Asia/Shanghai

# language environment
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
EXPOSE 3515
# ENV SASS_BINARY_SITE https://npm.taobao.org/mirrors/node-sass/
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
# 	&& apk update \
# 	&& apk upgrade \
# 	&& apk add --no-cache bash curl wget nginx openssh

ADD ./package.json  /app/package.json
WORKDIR /app
RUN npm install -g yarn npx --force --registry=https://registry.npm.taobao.org  \
	&& yarn install --registry=https://registry.npm.taobao.org 

ADD . /app
CMD ["node", "server.js"]
