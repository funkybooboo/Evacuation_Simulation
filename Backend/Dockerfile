# Use node LTS version for the backend
FROM node:14-alpine

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json for backend
COPY Api/package*.json ./

# Install backend dependencies
RUN npm install

# Copy the rest of the backend application code
COPY Api .

# Install Python and dependencies for Simulation
RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip

# Set working directory for Simulation
WORKDIR /usr/src/app/Simulation

# Copy requirements.txt and install Python dependencies
COPY Simulation/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the Python application code
COPY Simulation .

# Build TypeScript backend
RUN npm run build

# Expose port for the Express backend
EXPOSE 3000

# Command to run both backend and Python script
CMD ["npm", "start"]
