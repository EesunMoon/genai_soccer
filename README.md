# Personalized Support Message Generation System using Generative AI

This project focuses on enhancing fan engagement through a Generative AI system that creates personalized support messages based on fan-inputted Q&A responses. The system was deployed at live photo booth events for a Korean professional soccer team (*Daejeon Hana Citizen*).

## 📄 Overview

- **Role:** Machine Learning Engineer at Humaner AI  
- **Initiative:** Korean Professional Soccer Team Fan Engagement  
- **Objective:**
  - Enhance fan interaction by generating personalized support messages.
  - Integrate generated messages with fan photos and player images for live events.

## 🚀 System Architecture
![System Architecture](https://github.com/user-attachments/assets/d6887e9f-e41c-4f9e-a898-3f076f745c7b)

- **Components:**
  - **Next.js**: Front-end server for user interaction.
  - **FastAPI**: Backend Generative AI server.
  - **LangChain & OpenAI**: Tools for processing Q&A responses and generating personalized messages.
  - **Docker & AWS EC2**: Deployment tools for scalability and reliability.

## 🛠️ Key Features

1. **Generative AI Pipeline**:
   - Built with **LangChain** and **OpenAI** for generating personalized support messages.
   - Integrated with **Retrieval-Augmented Generation (RAG)** for message optimization.
   - **Prompt-Tuning** to refine generated outputs

2. **Message Optimization**:
   - Enhanced message relevance and accuracy using **prompt-tuning** techniques.

3. **Deployment**:
   - Deployed on **AWS EC2** using **Docker** for scalability.
   - Seamlessly integrated with the **Next.js** front-end server.

4. **Live Event Integration**:
   - Generated messages were integrated with fan photos and player images for live photo booth events.

## 🧩 Technologies Used

- **Frontend**: Next.js  
- **Backend**: FastAPI, LangChain, OpenAI  
- **Deployment**: Docker, AWS EC2  
- **AI Techniques**: Prompt Tuning, Retrieval-Augmented Generation (RAG)

## 📈 Impact

- Enabled personalized fan interactions at live events.  
- Streamlined the integration of AI-generated content into multimedia outputs for professional sports events.

## 📂 Repository Structure

```plaintext
├── GenAI_Application/      # LangChain and OpenAI scripts, FastAPI backend server files
├── Dockerfile              # Docker configuration for deployment
├── requirements.txt        # Version
└── README.md               # Project documentation
