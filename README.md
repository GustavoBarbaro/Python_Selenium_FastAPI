[![GitHub Repo](https://img.shields.io/badge/GustavoBarbaro-Python__Selenium__FastAPI-blue?style=flat&logo=github)](https://github.com/GustavoBarbaro/Python_Selenium_FastAPI) [![License](https://img.shields.io/badge/License-MIT-yellow)](#license) [![Made with Python](https://img.shields.io/badge/Python-=3.12.3-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")

# Python Selenium FastAPI Web Scraper

## Overview

This project integrates FastAPI with Selenium to automate web interactions through a RESTful API. It is containerized using Docker and orchestrated with Docker Compose for streamlined deployment and scalability.


---

# Technologies

* ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
* ![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)
* ![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
* ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
* ![Google Chrome](	https://img.shields.io/badge/Google_chrome-4285F4?style=for-the-badge&logo=Google-chrome&logoColor=white)

---

# Features

* **FastAPI**: Serves as the web framework for building the API endpoints.
* **Selenium**: Automates browser interactions for tasks like web scraping or testing.
* **Docker & Docker Compose**: Facilitates containerization and service orchestration.
* **Modular Architecture**: Organized into distinct modules for Automation, Builder, Execution, models, and testing.


---

# Functional Specification

The project do the scraping in this site:

* [https://selenium-html-test.replit.app/](https://selenium-html-test.replit.app/)

It uses 4 Chrome WebDriver instances to handle multiple async calls. If all instances are busy, responds with **HTTP 429** with body:

```json
{"detail": "no worker available"}
```

## Endpoint

```
GET /scrape?category=<name>
```

For example:

```bash
curl 'http://localhost:8000/scrape?category=Cosmetics'
```

It should return a JSON like this in case the category exists.

```json
[{
    "ID": "#032",
    "Name": "Advanced Facial Cleanser",
    "Category": "Cosmetics",
    "Price": 126,
    "Stock": "In Stock (8)"
}]
```

If the category does not exist it return:

```json
{
	"detail": "category not found"
}
```

---

# Project Hierarchy

```
your_repo/
├── automation/           FastAPI entry points, thread-pool bootstrap
│   ├── app.py
│   ├── logger.py
│   └── settings.py
├── builder/              Selenium scraping & parsing logic
│   ├── pool.py
│   └── scraper.py
├── executer/             Service layer between API and pool
│   └── service.py
├── models/               pydantic
│   └── product.py
├── tests/                pytest suite
│   └── test_scraping.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```


---


# Getting Started

## Prerequisites

* Linux OS or WSL2 with Windows
* Docker

## Running the Aplication

**1. Clone the repository**

```bash
git clone https://github.com/GustavoBarbaro/Python_Selenium_FastAPI
cd Python_Selenium_FastAPI
```

**2. Build the container and start services**

```bash
docker compose up --build
```

This command will build the Docker images and start the FastAPI application along with any other defined services.


**3. Access the API**

```bash
curl 'http://localhost:8000/scrape?category=Cosmetics'
```

**4. (Optional) Run lint and tests**

```bash
docker compose exec api pytest -q
docker compose exec api ruff check .
```

**5. Shutdown container**

```bash
docker compose down
```

---

# Assumptions

* **Headless Browser**: The Selenium WebDriver is configured to run in headless mode for performance and compatibility in containerized environments.
* **Single Responsibility**: Each module in the project serves a distinct purpose, adhering to the single responsibility principle.

# Trade-Offs

* **Complexity**: Integrating FastAPI with Selenium introduces complexity, especially in handling asynchronous operations and browser sessions.
* **Resource Consumption**: Containerizing the application ensures consistency across environments but may increase resource usage compared to running the application natively.
* **Performance vs. Flexibility**: Running Selenium in headless mode improves performance but may limit debugging capabilities compared to a full browser.


# Keywords

FastAPI; Selenium; Python; Docker; Docker Compose; REST API; Web Automation; Headless Browser; Web Scraping; API Testing; Swagger UI; Async Programming; Backend Development; Automation Scripts; Containerization; Pyproject; Modular Architecture
