# Key-Value Store API

This project implements a Key-Value Store API with advanced features such as tenant isolation, JWT-based authentication, batch operations, and automatic TTL expiration. It is designed to be powerful, easy to use, and secure.

## Features

- **CRUD Operations**: Create, read, update, and delete key-value pairs.
- **Batch Operations**: Handle multiple key-value pairs in a single request.
- **Time-to-Live (TTL)**: Automatically expire keys after a certain period.
- **Multi-Tenancy**: Supports isolated data storage for multiple users.
- **JWT Authentication**: Secure the API with JSON Web Tokens.

## Prerequisites

- Python 3.8 or higher
- Virtual environment manager (e.g., virtualenv or conda)

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/melbinjp/Key_value_datastore
cd Key_value_datastore
```

### Environment Setup

Create and activate a virtual environment:

```bash
# On macOS and Linux:
python3 -m venv env
source env/bin/activate

# On Windows:
python -m venv env
.\env\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Initialize Database with Alembic

```bash
alembic upgrade head
```

### Running the Application

Start the Flask application:

```bash
flask run
```

## API Endpoints

Each endpoint is secured with JWT authentication, and a valid token must be included in the header of each request.

### Authenticate

- **POST `/login`**:
  - Input: `{"username": "user", "password": "password"}`
  - Returns: A JWT token used for authenticated requests.

### Create Key-Value Pair

- **POST `/api/object`**:
  - Header: `Authorization: Bearer YOUR_JWT_TOKEN`
  - Request:
    ```json
    {
      "key": "exampleKey",
      "data": {"info": "exampleData"},
      "ttl": 3600
    }
    ```
  - Response:
    ```json
    {
      "message": "Key-Value pair created"
    }
    ```

### Retrieve Key-Value Pair

- **GET `/api/object/<key>`**:
  - Header: `Authorization: Bearer YOUR_JWT_TOKEN`
  - Response:
    ```json
    {
      "key": "exampleKey",
      "data": {"info": "exampleData"}
    }
    ```

### Delete Key-Value Pair

- **DELETE `/api/object/<key>`**:
  - Header: `Authorization: Bearer YOUR_JWT_TOKEN`
  - Response:
    ```json
    {
      "message": "Key-Value pair deleted"
    }
    ```

