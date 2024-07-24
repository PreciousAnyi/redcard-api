Here’s a more detailed and structured README for the Red Card API, incorporating the provided API endpoints:

# Red Card API

The Red Card API is designed to combat examination malpractice in tertiary institutions by implementing a transparent, point-based system for students and faculty. This system encourages academic integrity and fairness by assigning points for various exam offenses and referring cases to the exam committee when a threshold is reached.

## Table of Contents
- [Project Purpose](#project-purpose)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Auth Endpoints](#auth-endpoints)
  - [Red Card Endpoints](#red-card-endpoints)
- [Authentication](#authentication)
- [Challenges Overcome](#challenges-overcome)
- [Contributors](#contributors)
- [License](#license)

## Project Purpose
The Red Card App was created to address the increasing issue of examination malpractice in tertiary institutions. Examination malpractice undermines academic integrity and fairness, allowing students to graduate without the necessary knowledge and skills. This project aims to curb such malpractice by introducing a clear, point-based system for tracking and penalizing offenses.

## Features
- **Point Allocation:** Assigns point values to different exam offenses based on their severity.
- **Accumulation and Threshold:** Tracks points for documented offenses and refers cases to the exam committee once a threshold is reached.
- **Transparency and Accountability:** Provides clear information about the point system and potential consequences.

## Technologies Used
- **Backend:** Django Rest Framework
- **Authentication:** JWT (JSON Web Tokens) with Simple JWT
- **API Documentation:** drf_yasg for Swagger UI

## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/PreciousAnyi/redcard-api.git
    cd redcard-api
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage
1. **Access the API documentation:**
    Visit `https://preciousanyi.pythonanywhere.com/swagger/` to view the Swagger UI for the API.

2. **Interact with the API endpoints** as per the documentation.

## API Endpoints

### Auth Endpoints

- **Login**
  - `POST /auth/login/` - Log in a user

- **Logout**
  - `POST /auth/logout/` - Log out a user

- **Register Invigilator**
  - `POST /auth/register/invigilator` - Register a new invigilator

- **Register Student**
  - `POST /auth/register/student` - Register a new student

### Red Card Endpoints

- **Blacklist**
  - `GET /api/blacklist/` - List all blacklisted users

- **Cards**
  - `GET /api/cards/` - List all cards

- **Past Exams**
  - `GET /api/past_exams/` - List all past exams

- **Red Cards**
  - `GET /api/redcards/` - List all red cards
  - `POST /api/redcards/` - Create a new red card
  - `GET /api/redcards/invigilator/{personnel_no}/` - Get red cards assigned by an invigilator
  - `GET /api/redcards/student/{personnel_no}/` - Get red cards received by a student
  - `DELETE /api/redcards/{id}/` - Delete a red card

- **Thresholds**
  - `GET /api/thresholds/` - List all thresholds
  - `GET /api/thresholds/{user}/` - Get threshold for a specific user

- **Upcoming Exams**
  - `GET /api/upcoming_exams/` - List all upcoming exams

## Authentication
The API uses JWT (JSON Web Tokens) for authentication. To interact with authenticated endpoints, include the following header in your requests:
```http
Authorization: Bearer <your_token_here>
```

## Challenges Overcome
1. **Model Design:** Initially struggled with defining the fields and relationships for the models.
2. **API Routes and HTTP Methods:** Determining the appropriate routes and methods for RESTful API design.
3. **Model Implementation:** Encountered errors during implementation, requiring adjustments to the initial design.
4. **Authentication:** Implementing secure and efficient user authentication.
5. **Authorization:** Ensuring proper access control for different user roles.

## Contributors
- **Precious Anyi:** Developer, Project Lead

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For any questions or contributions, feel free to contact us.
