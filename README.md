# Property Management System Using Django  

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Project Structure](#project-structure)  
6. [Database Models](#database-models) 
7. [Usage](#usage)
8. [Testing](#testing)  
9. [Command-Line Utilities](#command-line-utilities)  


---

## Overview  
The **Property Management System** is a Django-based application designed for managing property information with robust geospatial capabilities provided by PostgreSQL and PostGIS. The project focuses on enabling hierarchical location management, accommodation details, and localized descriptions, all accessible via the Django Admin interface.  

---

## Features  
- Hierarchical location management (e.g., continent, country, state, city).  
- Accommodation data storage, including geospatial center points.  
- Localization support for accommodation descriptions and policies.  
- Robust filtering and search capabilities in the Django Admin.  
- CLI utility for generating location-based sitemaps.  
- Role-based permissions for property owners.  

---

## Prerequisites  

Before starting, ensure the following tools are installed:  
1. **Docker** and **Docker Compose**  
   - Follow the official [Docker installation guide](https://docs.docker.com/desktop/) to install Docker on your system.  

2. Python 3.9+ (for local development)  
3. Git 

---

## Installation  

Follow these steps to set up the project:  

### 1. Clone the Repository  
```bash  
git clone https://github.com/SamiaAurin/inventory_management.git  
cd inventory_management
```
### 2. Set Up a Virtual Environment

**On Linux/macOS:**
```bash 
python3 -m venv venv  or python -m venv venv 
source venv/bin/activate  
```
**On Windows:**
```bash 
python -m venv venv  
venv\Scripts\activate  
```
Ensure Docker Desktop is running on your system, as it is required to manage the containers. Then, execute the following commands to build and run the application:  

```bash  
cd inventory_management
docker-compose build  
docker-compose up    
```
**Note:**
The Docker build process may take some time to complete. This is because the **Dockerfile** and **docker-compose.yml** are configured to automatically install all dependencies listed in the **requirements.txt** file during the build phase. Please be patient while the setup is finalized.

## Project Structure
The project structure should look like this below.

- `inventory_management/`
  - `inventory_management/`
    - `__pycache__/`
    - `__init__.py`
    - `asgi.py`
    - `settings.py`
    - `urls.py`
    - `wsgi.py`
  - `properties/`
    - `__pycache__/`
    - `management/commands`
      - `generate_sitemap.py`
    - `migrations/`
    - `static/`
  - `templates/`
    - `properties/`
      - `signup.html`
  - `__init__.py`
  - `admin.py`
  - `apps.py`
  - `forms.py`
  - `models.py`
  - `tests.py`
  - `urls.py`
  - `views.py`
- `.coverage`
- `docker-compose.yml`
- `Dockerfile`
- `manage.py`
- `requirements.txt`
- `sitemap.json`
- `.gitignore`
- `README.md`

## Database Models

### **Location**
- Manage hierarchical locations, such as countries, states, and cities.

### **Accommodation**
- Store details about properties, including geospatial location, amenities, and images.

### **LocalizeAccommodation**
- Support for localized descriptions and policies.

## Usage  

### Admin Interface  
- Navigate to: [http://localhost:8000/admin](http://localhost:8000/admin).  
- Log in using your superuser credentials. 
  - Set up a superuser for accessing the Django Admin (See the pdf)    
- Key actions you can perform in the Admin interface:   
  - Add, update, or delete **Locations**, **Accommodations** and **Localize accommodations**.  
  - Assign user roles and manage permissions.  

### Public Signup Page  
- Property owners can submit sign-up requests via the public-facing page:  
  [http://localhost:8000/properties](http://localhost:8000/properties).  

### Reference for Understanding Add, Update, Delete Operations, and User Management

For a comprehensive guide on managing the **Add**, **Update**, and **Delete** operations for all tables, as well as understanding the user management and role-based access control in this project, please download the **PDF document** titled **Assignment06**. This document provides detailed instructions on:

- How to add, update, and delete records in the system.  
- How the **Admin** can grant specific access to the **Property Owners** group, ensuring that users have appropriate permissions to manage their own properties.


### Importing Data from CSV

To import location data into the Locations table, you can use the provided CSV files. Import the CSV files in the following order: Locations - Country.csv, Locations - State.csv, and Locations - City.csv. 
However, please note that there is an issue where the `center` and `location_type` columns are not automatically populated with the correct values in the `POINT(long, lat)` format during import.

#### Steps to resolve this:

1. After importing the CSV data, you will need to manually update the `center` and `location_type` columns to ensure they are in the correct format.
2. For the `center` column, ensure the value is in the format `POINT(longitude latitude)`.
3. For the `location_type` column, assign the appropriate value (e.g., "City", "Country").


## Testing

To run unit tests, you must be inside the web container, and the container must be running. Follow the steps below to execute the tests and measure coverage:

```bash
docker exec -it inventory_management-web-1 bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```
In the `Assignment 06.pdf`, there are screenshots demonstrating this process. It provides a visual guide to accessing the web container, installing the necessary coverage tool, running unit tests, and generating the coverage report. These screenshots can be referenced for a more detailed, step-by-step walkthrough of executing tests and viewing coverage results.


## Command-Line Utilities

- `properties/`
    - `__pycache__/`
    - `management/commands`
      - `generate_sitemap.py`

```bash
docker exec -it inventory_management-web-1 bash
python manage.py generate_sitemap
```
It will generate a `sitemap.json` file in the main directory of the `inventory_management` project, where the `manage.py` file is located. The JSON file will resemble the example shown below.

```bash
[
  {
    "USA": "usa",
    "locations": [
      {
        "Florida": "usa/florida"
      },
      {
        "Texas": "usa/texas"
      }
    ]
  }
]
```
