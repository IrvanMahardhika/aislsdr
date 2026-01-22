# --- Stage 1: Build the React application ---
FROM node:20-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app for production (creates /app/build or /app/dist)
RUN npm run build

# --- Stage 2: Serve the application with Nginx ---
FROM nginx:alpine

# Copy the built static files from the builder stage to Nginx's web root
COPY --from=builder /app/build /usr/share/nginx/html

# (Optional) Copy custom Nginx configuration if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (Nginx default)
EXPOSE 80

# Command to run Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
