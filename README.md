# news-collector

A Django-based application for collecting and processing news from various sources.

# Environment Settings

To set up the environment, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd news-collector
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv news-collector-env
    source news-collector-env/bin/activate
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Apply database migrations:**
    ```sh
    python manage.py migrate
    ```

2. **Run the development server:**
    ```sh
    python manage.py runserver
    ```