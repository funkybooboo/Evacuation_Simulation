# Use node LTS version for the backend
FROM node:14-alpine AS API

# Set working directory inside the container for API
WORKDIR /app/Api

# Copy package.json and package-lock.json for backend
COPY Api/package*.json ./

# Install backend dependencies
RUN npm install

# Copy the rest of the backend application code
COPY Api .

# Build TypeScript backend
RUN npm run build


# New stage for Python dependencies and runtime
FROM python:3.x-slim

# Set working directory inside the container for backend and simulation
WORKDIR /app/Simulation

# Install Poetry
RUN pip install poetry

# Copy only requirements files and install Python dependencies
COPY Simulation/pyproject.toml Simulation/poetry.lock ./Simulation/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the Python application code
COPY Simulation ./

# Copy API build from previous stage
COPY --from=API /app/Api/build /app/Api/build

# Expose port for the Express backend
EXPOSE 3000

# Command to run the Express server
CMD ["npm", "start"]
