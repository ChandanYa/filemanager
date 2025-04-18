# File Manager 🗂️

A modern full-stack file management system with React frontend and Django REST backend.

![Tech Stack](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tech Stack](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Tech Stack](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## 🚀 Getting Started

### Prerequisites

- Node.js ≥ 16.x
- Python ≥ 3.8
- PostgreSQL ≥ 12.x
- Yarn (recommended) or npm

### Installation

```bash
# Clone the repository
git clone https://github.com/ChandanYa/filemanager.git
cd filemanager

cd frontend

# Install dependencies using yarn (recommended)
yarn install

# Or using npm
npm install

# Create environment configuration
cp .env.example .env

# Start development server (http://localhost:3000)
yarn start

# Build for production
yarn build

# Run tests
yarn test

# Fix linting issues
yarn lint
cd ../backend

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate
# Install requirements
pip install -r requirements.txt

# Configure environment
cp .env.example .env
