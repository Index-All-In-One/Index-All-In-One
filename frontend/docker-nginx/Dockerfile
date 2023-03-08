# Use an Nginx production image as the base image
FROM nginx:alpine

# Remove the default Nginx configuration
RUN rm -rf /usr/share/nginx/html/*

# Copy the built Flutter web app into the Nginx directory
COPY build/web /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80
