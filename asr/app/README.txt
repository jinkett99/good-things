What are the benefits of using docker for product deployment workflows? 
- [Benefits to development teams] Docker standardizes the process of running services (by standardardizing source code, dependencies and configurations) on local development environments. 
- [Benefits to application deployment] Allows development teams to package src code, dependencies and configurations into for MLOps/operations team to test run their applications.
*Facilitates efficiency in product teams by standardizing the process of running services, facilitating workflows in development and app deployment teams. 

Explanation of Docker Commands for 
(1) Building Docker Image from Dockerfile, requirements.txt and main.py
(2) Running the Docker container - A running instance of the Docker Image. 

cd app: Go to your FastAPI project folder where Dockerfile and asr_api.py live.

docker build -t asr-api .:
-t asr-api: Tags the image with the name asr-api.
.: Tells Docker to use the current directory for the build context.
Docker reads the Dockerfile, installs dependencies, copies your app files, and packages everything into a deployable image.
📌 Make sure Docker Desktop / Docker daemon is running — it must be active for builds or container runs to work.

<Refer to Dockerfile for detailed annotations.>

docker run -p 8001:8001 asr-api
Spins up a container from the asr-api image.
-p 8001:8001: Maps your local port 8001 to the exposed container’s port 8001.
Once running, your FastAPI service is accessible at: http://localhost:8001/asr 