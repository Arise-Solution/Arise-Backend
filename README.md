# Arise Solution API

This repository contains the source code for the Arise Solution API. The API is built using Django and includes API documentation using `drf_yasg`.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Arise-Solution/Arise-Backend.git
    cd Arise-Backend
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - **Linux/Mac:**
        ```bash
        source venv/bin/activate
        ```

    - **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional):**

    ```bash
    python manage.py createsuperuser
    ```

## Running the API

```bash
python manage.py runserver
```

## Documentation of drf_yasg

The API documentation is available at `http://localhost:8000/swagger/` and `http://localhost:8000/redoc/`.


### Incomplete tasks

- [x] https://www.rootstrap.com/blog/how-to-integrate-google-login-in-your-django-rest-api-using-the-dj-rest-auth-library
