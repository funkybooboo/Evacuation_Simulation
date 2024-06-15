# Use node LTS version for the client
FROM node:14-alpine as client

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the application code
COPY . .

# Build TypeScript React application
RUN npm run build

# Serve the build output using nginx
FROM nginx:alpine

# Copy built React app from previous stage
COPY --from=client /usr/src/app/build /usr/share/nginx/html

# Expose port 80 for nginx
EXPOSE 80

# Start nginx to serve the React app
CMD ["nginx", "-g", "daemon off;"]
