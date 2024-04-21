# Use a specific version instead of 'latest' to ensure consistency
FROM python:3.8.13-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

# Copy from the current directory of the Dockerfile to /backend in the image
COPY . .

# Install the Python dependencies directly from the requirements.txt file
RUN pip install -r requirements.txt

EXPOSE 9002

CMD ["python"]