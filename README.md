# User-Generated Content Management API

This API provides a comprehensive platform for managing user-generated content, 
tailored specifically for applications that involve creation, update, and deletion 
of posts and comments. 
This platform is designed to facilitate community interactions without the need 
for authentication to view content, making it perfect for open forums, 
comment sections, and social apps.

## Features

- **Public Content Viewing:** All posts and comments are publicly visible without the need for authentication.
- **Secure User Registration:** Users can register to the platform to contribute to the content.
- **Token-based Authentication:** Actions such as posting, updating, and deleting content are secured with JWT authentication.
- **CRUD Operations:** Full support for creating, reading, updating, and deleting content through standard HTTP methods.
- **Swagger UI Documentation:** Interactive API documentation provided via Swagger UI for real-time testing and endpoint exploration.

## Local installation

### Prerequisites

- Python 3.11.4 or higher
- PostgreSQL (latest version should work) 
- A REST client like Postman or curl (optional, if not using Swagger UI directly)

## Installation
  
1. **Clone the Repository to your local machine**
   
   Run the following command to clone the project:
   ```
   git clone https://github.com/afk0901/Blogity
   ```
2. **Set Up a Virtual Environment**

   Run the following command to create a virtual environment:
   ```
   python -m venv venv
   ```
3. **Install Dependencies**
   
   Run the following command to install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Run the following command to install development dependencies such as Linters, pre-commit and Mypy:
   ```
   pip install -r requirements-dev.txt
   ```
   
4. **Environment Setup**
   
   Create a .env file in the root directory of the project with following variables:
   
   - DEBUG=True/False depending on if debug mode should be activated or not in the base settings
   - PATH_TO_DJANGO_SETTINGS='Bloggity.settings.local'
   
     **Note:** if the intention is to run with the production or staging settings then replace .local with .staging or.production
   - DJANGO_SECRET_KEY=django-insecure-kih$vse%bf+e9%4=ii7yye+s120^r8ug!5$4@k@3hnfsk+@i%r
   - DB_NAME=Bloggity
   - DB_USER=postgres
   - DB_PASS=```<your postgres password>```
   - DB_HOST=localhost
   - DB_PORT=5432
   - STATIC_URL=static/
   - ALLOWED_HOSTS=localhost,127.0.0.1
5. **Database Initialization**
    
    Run the following command to setup the database:
   
    ```python manage.py migrate```

7. **Install Pre-commit Hooks** (Optional)
   Set up pre-commit hooks to ensure code style and standards are verified before each commit, if the intention is to commit to the repository:

   Run the following command to set up pre-commit hooks:
   
   ```pre-commit install```
   

7. **Start the Development Server**

    Run the following command to run the development server:
    ```python manage.py runserver```

8. **Access the API**
   
   The API can be accessed at ```/api/``` (place it after the base URL), which will direct you to the Swagger (drf-spectacular) UI page.

## Documentation
Swagger UI provides detailed documentation for all API endpoints, including descriptions, parameter requirements, and example responses. 
This feature simplifies the process of integrating and testing the API.


  
