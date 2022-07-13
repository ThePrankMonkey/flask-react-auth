# pull official base image
FROM node:18-alpine

# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json .
COPY package-lock.json .
RUN npm ci
RUN npm install react-scripts@5.0.1 prettier@2.6.2 eslint@8.14.0 -g --silent
RUN npm install react-router-dom@6.3.0 -g --silent
RUN chown -R node:node /usr/src/app/node_modules

# start app
CMD ["npm", "start"]