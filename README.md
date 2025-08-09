# Django REST API с CI/CD и деплоем
## Развёртывание на сервере
### 1. Подключитесь к серверу по SSH:
#### ssh -i ~/.ssh/id_ed25519 test@158.160.185.151
### 2. Клонируйте репозиторий:
#### git clone https://github.com/TsiganovDS/DjangoDRF
#### cd DjangoDRF
### 3. Скопируйте переменные окружения:
#### cp .env.sample .env
### 4. Запустите проект:
#### docker-compose up -d --build
#  CI/CD через GitHub Actions
## Проект использует автоматическую систему CI/CD:
### При push в ветку develop:
#### запускается GitHub Actions
#### выполняются тесты с помощью pytest
#### если тесты прошли — выполняется деплой на сервер


