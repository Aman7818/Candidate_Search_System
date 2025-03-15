# ATS API - Django REST Framework

## Overview
This project is an Applicant Tracking System (ATS) for recruiters, built using Django REST Framework (DRF). It allows recruiters to manage candidate records efficiently with the following features:

- Create, update, and delete candidates
- Search candidates based on name with relevancy-based sorting
- Uses Django ORM for optimized searching

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- MySQL
- Django & Django REST Framework

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file with database credentials:
   ```ini
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   ```

5. Apply migrations:
   ```bash
   python manage.py makemigrations ATS_Api
   python manage.py migrate
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

| Method | Endpoint                  | Description |
|--------|---------------------------|-------------|
| POST   | `/candidates/`            | Create a new candidate |
| PUT    | `/candidates/<id>/`       | Update candidate details |
| DELETE | `/candidates/<id>/delete/`| Delete a candidate |
| GET    | `/candidates/search/?q=<query>` | Search candidates by name |



## Sample API Requests & Responses

### 1. Create a Candidate
**Request:**
```json
POST /api/candidates/
{
    "name": "John Doe",
    "age": 28,
    "gender": "M",
    "email": "johndoe@example.com",
    "phone_number": "1234567890"
}
```
**Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "age": 28,
    "gender": "M",
    "email": "johndoe@example.com",
    "phone_number": "1234567890"
}
```

### 2. Update a Candidate
**Request:**
```json
PUT /api/candidates/1/
{
    "name": "John Smith",
    "age": 29
}
```
**Response:**
```json
{
    "id": 1,
    "name": "John Smith",
    "age": 29,
    "gender": "M",
    "email": "johndoe@example.com",
    "phone_number": "1234567890"
}
```

### 3. Delete a Candidate
**Request:**
```json
DELETE /api/candidates/1/delete/
```
**Response:**
```json
{
    "message": "Candidate deleted successfully."
}
```

### 4. Search Candidates
**Request:**
```json
GET /api/candidates/search/?q=John Doe
```
**Response:**
```json
[
    {
        "id": 1,
        "name": "John Doe",
        "age": 28,
        "gender": "M",
        "email": "johndoe@example.com",
        "phone_number": "1234567890"
    },
    {
        "id": 2,
        "name": "John Smith",
        "age": 29,
        "gender": "M",
        "email": "johnsmith@example.com",
        "phone_number": "9876543210"
    }
]
```

## Searching Mechanism
- The search query is split into words.
- Candidates are filtered based on partial matches in their names.
- Results are sorted based on the number of matching words (relevancy).

## Technologies Used
- **Django REST Framework**: API development
- **MySQL**: Database
- **Django ORM**: Query optimization

## Contribution
Feel free to fork the repository, make changes, and create a pull request!

## License
This project is licensed under the MIT License.

