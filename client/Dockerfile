# define the node base image with your desired version node:<version>
FROM node:21 as builder

# set working directory
WORKDIR /app

# copies package.json and package-lock.json to Docker environment
COPY package*.json ./

# Install all Node dependencies
RUN npm install

# Copies everything over to Docker environment
COPY . .

# Build the application for production
RUN npm run build

# Stage 2: Serve app with Nginx server

# Use official nginx image. Use the `alpine` version for a smaller final image size
FROM nginx:alpine

# Copy built assets from the builder stage to nginx public facing directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 for the app
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
