# Specify Base image: Uses a lightweight Python 3.9 image as the foundation.
FROM python:3.9-slim

# Install system dependencies
# Install ffmpeg, required for audio processing (especially by torchaudio or pydub).
# rm -rf /var/lib/apt/lists/* clears apt cache to keep the image small.
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container to /app
# All following paths (e.g., COPY, RUN) are relative to /app.
WORKDIR /app

# Copy requirements and install
# Copies requirements.txt from your host to the container’s /app directory.
COPY requirements.txt .

# Upgrades pip.
# Installs Python dependencies from requirements.txt.
# --no-cache-dir avoids storing wheel/cache files to keep image size smaller.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copies codes for FastAPI app (main.py) to the container.
COPY main.py .

# Expose the container port. 
# Declares that the container will listen on port 8001.
EXPOSE 8001

# Defines the default command to run when the container starts.
# main:app: Tells uvicorn to run app from the main.py file.
# --host 0.0.0.0: Makes the app accessible outside the container.
# --reload: Enables auto-reload on code changes (good for development).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
