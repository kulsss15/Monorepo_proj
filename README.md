Monorepo Project: AI Service & Weather Service
  This repository contains two microservices:
    Weather Service - Provides weather-related data.
    AI Service - Performs AI-related computations.
  Both services are managed within a monorepo structure, utilizing Poetry for dependency management, Docker for containerization, and Makefile for simplified commands.

  Table of Contents
    Project Structure
    Prerequisites
    Project Setup
    Local Development
    Running with Docker
    Running AI & Weather Services Separately or Together
    Environment Configuration
    Deployment
    Makefile Commands
    GitHub Workflow
    Troubleshooting
    Contributing

  Project Structure:
    monorepo_proj/
    │── ai_service/                 # AI microservice
    │   ├── src/
    │   │   ├── ai_service/
    │   │   │   ├── main.py         # Entry point for AI service
    │   │   │   ├── config.py       # Configuration settings
    │   │   │   ├── models.py       # Data models
    │   │   │   ├── routes.py       # API endpoints
    │   ├── tests/
    │   ├── Dockerfile
    │   ├── pyproject.toml
    │   ├── poetry.lock
    │
    │── weather_service/             # Weather microservice
    │   ├── src/
    │   │   ├── weather_service/
    │   │   │   ├── main.py         # Entry point for Weather service
    │   │   │   ├── config.py       # Configuration settings
    │   │   │   ├── models.py       # Data models
    │   │   │   ├── routes.py       # API endpoints
    │   ├── tests/
    │   ├── Dockerfile
    │   ├── pyproject.toml
    │   ├── poetry.lock
    │
    │── Makefile                     # Automation tasks
    │── docker-compose.yml            # Running services together
    │── README.md                     # Documentation
    │── .gitignore                     # Ignored files

Prerequisites:
  Ensure you have the following installed:
    Python 3.10+
    Poetry
    Docker & Docker Compose
    Make
    Git

Project Setup:
  Clone the Repository:
  
      git clone https://github.com/your-org/monorepo_proj.git
      cd monorepo_proj
 
  Setup Virtual Environments with Poetry:
   
      make install
 
  Local Development:
   
    To run services without Docker (Any individual service):
       
          make dev
          
    Access APIs:

      Weather Service Swagger Docs: http://localhost:8001/docs
      AI Service Swagger Docs: http://localhost:8000/docs
    
    Running with Docker:
    
      Building Docker Images:
        
        Development:
            
            make build-dev
       
        Production:
            
            make build-prod
     
      Running Services in Docker:
      
        make run-weather-docker
        make run-ai-docker
    
    Running AI & Weather Services Separately or Together:
    
        Run AI Service Only:
        
            docker-compose up -d ai_service
       
        Run Weather Service Only:

            docker-compose up -d weather_service
        
        Run Both Services Together:
        
            docker-compose up -d
   
    Environment Configuration:
    
    `Environment	Description:
        DEV	Local development mode with hot reload
        PROD	Production mode with optimizations
    
    Set environment:
        export ENV=development  # Local development
        export ENV=production   # Production
   
    Deployment:
        Build and Push Docker Image:
          Authenticate with DockerHub:
            docker login
          Tag the Image:
            docker tag ai_service:prod your-dockerhub-username/ai_service:latest
            docker tag weather_service:prod your-dockerhub-username/weather_service:latest
          Push the Image:
            docker push your-dockerhub-username/ai_service:latest
            docker push your-dockerhub-username/weather_service:latest
          Deploy with Docker Compose:
            docker-compose up -d
            Makefile Commands
      To automate tasks, use the Makefile: 

          Make install
          Or
           poetry install
          
          Run Services
         
          Make dev 
          or
            For Weather:  poetry run uvicorn src.weather_service.main:app --host 0.0.0.0 --port 8001 --reload
       
             For ai_service:  poetry run uvicorn src.ai_service.main:app --host 0.0.0.0 --port 8002 --reload
          Docker Commands
            build-dev:
                docker build -t ai_service:dev -f ai_service/Dockerfile .
                docker build -t weather_service:dev -f weather_service/Dockerfile .
            
            build-prod:
                docker build -t ai_service:prod -f ai_service/Dockerfile --build-arg ENV=production .
                docker build -t weather_service:prod -f weather_service/Dockerfile --build-arg ENV=production .

            run-weather-docker:
                docker run -p 8001:8001 --name weather_service_container weather_service:dev
            
            run-ai-docker:
                docker run -p 8002:8002 --name ai_service_container ai_service:dev
      GitHub Workflow:
          Create a New Feature Branch:
                git checkout -b feature/new-feature
          Make Changes & Commit:
                git add .
                git commit -m "Added new feature"
          Push Changes:
                git push origin feature/new-feature
    Check logs:
          docker logs weather_service_container
          docker logs ai_service_container
