# base image
FROM node:8

# copy files to docker image
RUN mkdir -p /src
ADD /src /src
ADD package-lock.json .
ADD package.json .
ADD webpack .
ADD webpack.config.js .
ADD npm .

WORKDIR .

# npm installs
RUN npm install --no-optional
RUN npm i
RUN npm run build

# start app
CMD ["npm", "start"]