# 🇨🇦 Canadian PIPEDA Intelligence Bot by Prashant Nigam

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20ECR-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Status](https://img.shields.io/badge/Status-Live-success)

## 🔴 Live Demo
**Try the bot here:** [http://98.83.26.77:8080/](http://98.83.26.77:8080/) 
---

## 📖 Project Overview
The **PIPEDA Intelligence Bot** is a RAG-based (Retrieval-Augmented Generation) legal assistant designed to answer complex questions regarding the *Personal Information Protection and Electronic Documents Act* (PIPEDA).

Unlike standard LLMs which may hallucinate legal facts, this system uses a **Vector Database (Pinecone)** to ground every answer in the actual text of the Canadian statute. It retrieves precise legal clauses and uses **Google Gemini 2.5 Flash** to synthesize a clear, accurate response.



---

## 🛠️ Tech Stack

### **AI & NLP**
* **LangChain:** For orchestrating the RAG pipeline.
* **Google Gemini 2.5 Flash:** The LLM used for reasoning and answer generation.
* **HuggingFace Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` for converting legal text into vector embeddings.
* **Pinecone:** Serverless Vector Database for storing and retrieving document chunks.

### **Backend & Web**
* **Flask:** Lightweight Python web server.
* **HTML/CSS/JS:** Responsive chat interface.

### **DevOps & Cloud**
* **Docker:** Containerization for consistent deployment.
* **AWS ECR (Elastic Container Registry):** Storage for Docker images.
* **AWS EC2 (Elastic Compute Cloud):** Virtual server for hosting the application.
* **GitHub Actions:** CI/CD pipeline for automated testing and deployment.

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/PIPEDA-Intelligence-Bot.git](https://github.com/your-username/PIPEDA-Intelligence-Bot.git)
cd PIPEDA-Intelligence-Bot
```
### 2. Create a Virtual Environment
```bash
conda create -n legalbot python=3.10 -y
conda activate legalbot
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
```bash
PINECONE_API_KEY=your_pinecone_key
GOOGLE_API_KEY=your_google_gemini_key
```

### 5. Index the Data (Run Once)

```bash
python store_index.py

```

### 6. Start the Application
```bash
python app.py
```
Open your browser to http://localhost:8080

# Deployment Architecture: AWS CI/CD Pipeline

This project is deployed using a robust CI/CD pipeline with **GitHub Actions** and **AWS**. Every time code is pushed to the `main` branch, the application is automatically built, tested, and deployed to the live server.

---

## Step 1: AWS Configuration (IAM User)
We created a dedicated IAM user to allow GitHub Actions to interact with AWS securely.

**Policies Attached:**
- `AmazonEC2ContainerRegistryFullAccess` – To push Docker images to ECR  
- `AmazonEC2FullAccess` – To manage the server instance  

---

## Step 2: Container Registry (ECR)
AWS ECR acts as the **“Garage”** for our code.

- Private repository name: `legalbot`  
- **URI:** `315865595366.dkr.ecr.us-east-1.amazonaws.com/legalbot`

The CI pipeline builds the Docker image and pushes it here.

---

## Step 3: The Server (EC2)
We launched an Ubuntu EC2 instance (`t3.micro`) to host the application.

**Security Group:**
- Port `8080` – Application traffic  
- Port `22` – SSH access  

---

## Step 4: Docker Installation on EC2
To run the container, Docker was installed on the Ubuntu server:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

---

## Step 5: GitHub Self-Hosted Runner
Instead of using a generic GitHub server, the EC2 instance was configured as a **Self-Hosted Runner**.

This creates a direct bridge between the GitHub repository and the AWS server.  
When a deployment is triggered, the EC2 instance:
1. Receives the signal  
2. Pulls the latest image from ECR  
3. Updates itself  

---

## Step 6: GitHub Secrets Management
To keep API keys secure, the following secrets were added to the GitHub repository:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `ECR_REPO`
- `PINECONE_API_KEY`
- `GOOGLE_API_KEY`

Secrets are injected into the container at runtime.

---

## ⚖️ Sample Queries
Try asking the bot these questions to test its legal reasoning:

- *What are the 10 fair information principles under Schedule 1?*  
- *Can an organization disclose personal information without consent in an emergency?*  
- *What are the rules for individual access to personal information?*  
- *How does PIPEDA define “commercial activity”?*  

---

## 📂 Project Structure
```
PIPEDA-Intelligence-Bot/
├── .github/workflows/
│   └── cicd.yaml          # CI/CD pipeline configuration
├── data/
│   └── PIPEDA_Act.pdf     # Source legal document
├── src/
│   ├── helper.py          # Data processing & embedding logic
│   └── prompt.py          # System prompt engineering
├── templates/
│   └── chat.html          # Frontend interface
├── app.py                 # Flask backend
├── store_index.py         # Data ingestion script
├── Dockerfile             # Container instructions
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```
