# Use a specific version instead of 'latest' to ensure consistency
FROM node:14 as builder

# Set the working directory in the Docker image
WORKDIR /frontend

# Copy package files first to leverage Docker cache
COPY ./package*.json .

# Install dependencies and vite globally
RUN npm install && npm install -g vite

# Then copy the rest of the files
COPY . .

RUN npm run build

# No need to expose ports in Dockerfile, it's done when running the container
# EXPOSE 5173

# For production, serve the built static files
CMD ["npm", "run", "dev"]