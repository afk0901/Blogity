# User-Generated Content Management API

This API provides a comprehensive platform for managing user-generated content, 
tailored specifically for applications that involve creation, update, and deletion 
of posts and comments initally inteded for a blog site, but after a realization, it's actually multipurpose.

This platform is designed to facilitate community interactions without the need 
for authentication to view content, making it perfect for open forums, 
comment sections, and social apps.

# Table of contents

1. [Features](#features)
2. [Local installation](#local-installation)
3. [Access the API](#access-the-api)
4. [API-documentation](#api-documentation)
5. [Contribution](#contribution)
6. [Feature requests](#feature-requests)
7. [Bug Reports](#bug-reports)
8. [Contact](#contact)


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

### Installation
  
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
   - ALLOWED_HOSTS=localhost,127.0.0.1 **Note:** You may need to change these to your allowed hosts if used on a diffrent host than localhost.
     
5. **Database Initialization**
    
    Run the following command to setup the database:
   
    ```python manage.py migrate```

7. **Install Pre-commit Hooks** (Optional but highly recommended)
   Set up pre-commit hooks to ensure code style and standards are verified before each commit, if the intention is to commit to the repository:

   Run the following command to set up pre-commit hooks:
   
   ```pre-commit install```
   

7. **Start the Development Server**

    Run the following command to run the development server:
    ```python manage.py runserver```

## Access the API ##
   
   The API can be accessed at ```/api/``` (place it after the base URL), which will direct you to the Swagger (drf-spectacular) UI page.
   Do not hesitate to fiddle around with it to get a feeling of how the API works.

## API documentation
Swagger UI provides detailed documentation for all API endpoints, including descriptions, parameter requirements, and example responses. 
This feature simplifies the process of integrating and testing the API.

## Contribution
Contributors are always welcome! If you wish to contribute:

1. Fork or clone the repository.
2. Make your changes in a separate branch.
3. Ensure your code adheres to the existing style and passes quality checks. We are using Black, Isort, Mypy and flake8.
   You should have installed pre-commit already if you followed the local installation steps which will take care of these
   if it's hooks are installed correctly.
5. Submit a pull request with your changes and a detailed description of the changes to this repository.
6. In your pull request, explain the value your contribution brings to the project and how it enhances/improves the game.


## Feature requests ##
If you have any feature requests in mind that could enhance the API please make an issue here in the repository and use the feature request template.

## Bug Reports ##
If you encounter any bugs please make an bug report in the issues here in this repository and use the feature bug report template.

## Contact ##
For further support regarding to this project or collaboration, don't hesitate to send me an <a href="mailto:arnarfkr@gmail.com">email</a> and I will try to help you.


  
