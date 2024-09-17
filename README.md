# Setup
1. Create venv
- `python -m venv venv`

2. Activate venv:

- `venv\bin\activate`

3. Install dependencies
- `pip install -r requirements.txt`

4. Create env variables:
- `export SECRET_KEY="secret_key"`

5. Create admin user
 - `flask --app src.initialize_db`


  6. For testing it, install pytest and run the suite
  - `pytest /tests`

# Project overview

This repository contains the structure for a Flask app that implements the basic functionality of an e-commerce shopping cart. It includes the following main components:

- Data Models: Basic data structures created using SQLAlchemy. Their primary purpose is to encapsulate business rules.
- Ports: Contracts/interfaces for connections through external entities.
- Adapters: Actual implementations of the logic defined by the Ports.
- Application Services: Business rules that are not data models but are necessary for the correct operation of the application, such as encryption and route definitions.
- Others: Configuration and database-related files.


Project tree:

├── README.md
├── instance
│   └── database.db
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 1df5a3e3b367_initial_migration.py
├── requirements.txt
├── setup.py
├── src
│   ├── adapters
│   │   ├── __init__.py
│   │   ├── cart_adapter.py
│   │   ├── cart_item_adapter.py
│   │   ├── order_adapter.py
│   │   ├── order_item_adapter.py
│   │   ├── product_adapter.py
│   │   └── user_adapter.py
│   ├── core
│   │   ├── application
│   │   │   ├── __init__.py
│   │   │   ├── order_service.py
│   │   │   ├── password_service.py
│   │   │   └── routes.py
│   │   ├── domain
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   └── ports
│   │ │       ├── __init__.py
│   │ │    ├── cart_item_port.py
│   │ │       ├── cart_port.py
│   │ │       ├── order_item_port.py
│   │ │       ├── order_port.py
│   │ │       ├── product_port.py
│   │ │       └── user_port.py
│   ├── initialize_db.py
│   └── main.py
├── tests
│   ├── integration
│   │   ├── conftest.py
│   │   ├── test_cart_adapter_in_memory.py
│   │   ├── test_cart_item_adapter_in_memory.py
│   │   ├── test_order_adapter_in_memory.py
│   │   ├── test_order_item_adapter_in_memory.py
│   │   ├── test_order_service_in_memory.py
│   │   ├── test_product_adapter_in_memory.py
│   │   ├── test_routes.py
│   │   └── test_user_adapter_in_memory.py
│   └── unit
│       ├── test_core_models.py
│       └── test_password_service.py

# Use case overview
A shopping cart is a collection of products selected from a user from a product catalog. This user can view that catalog and choose which products they want to buy. Additionally, the user should be able to edit his cart by removing already added products. After selecting the products, the user can place an order and empy the cart for future purchases.

Admin users should be able to add, remove and update products, while regular users cannot. This simulates a typical e-commerce cart.

# Methodology

When starting this project, it was noted that the case was framed as a basic initial application, which would allow for future improvements, including the integration of different types of external entities, such as various databases (including NoSQL). Considering that, I chose to implement the project following Hexagonal Architecture,  a common approach to web applications that enforces the use of Python objects. This was a great opportunity to study this type of architecture, which had been on my radar for some time..

I began the implementation with the data models, which helped me better organize my ideas. Initially, I used basic Python classes, but soon realized that it would require a lot of additional work to integrate with a database. Therefore, I switched to using Flask with the SQLAlchemy framework, following industry standards. This approach allowed me to leverage existing libraries and avoid redundant implementation. For the database, I used SQLite and employed bcrypt to hash passwords before persisting them in the database.

I utilized Black and Flake8 configured in pre-commit to ensure code quality and cleanliness. For version control, I adopted Conventional Commit patterns. Following Test Driven Development (TDD), I added tests using pytest for each new feature implementation, in a red-green-refactor fashion. Tests were conducted with an in-memory database, while the application interacts with a database during runtime.

For authentication, I used JWTManager from Flask-JWT, which simplifies session token and privilege management. Admin roles are managed during application runtime and in tests, following my decision not to allow the creation of admin users through endpoints. In the future, the ability for admin users to create other admin users could be considered if needed.

# Considerations
Aside from clean coding and testing practices in Python, almost every other aspect of this project involved learning. This web application was one of my first complete implementations, so each step required extensive research and reflection on the best approach. My previous experience was mainly with machine learning applications using basic Flask apps or Amazon SageMaker, which handles much of the project structuring, leaving the developer to focus on data processing pipelines and machine learning aspects. My research was primarily conducted through software engineering forums like Stack Overflow, blog posts, and library documentation.

For future improvements, I would consider using the Django framework, as it simplifies the development of web application specifics like data models, migrations, and authentication. Given my previous experience with Flask, I chose it for this project. However, based on my research, I believe starting with Django could have been easier. Nevertheless, I believe I achieved a similar result to what I would have with Django.

Regarding project features, it would be interesting to implement a restriction allowing each user to have only one active cart. This would simplify route calls, as the internal logic of the application would handle retrieving the user's cart by their user ID. Orders should also have their status updated to "concluded" once the user confirms payment (assuming payment logic is implemented, which would be a valuable addition). Development and production configurations would also be necessary in a real-world scenario to handle different environments effectively.
