## Internship Matching Platform

A Django-based web application that connects **students** with **companies** offering internship opportunities.  
Includes features for:
- Student & Company Registration
- Profile Management
- Internship Applications
- PDF Receipts & Email Notifications
- Role-based Dashboards (Student / Company)
- Admin Management
- Dockerized Deployment with Nginx & PostgreSQL

---

## Features
 Student & company authentication  
Internship application management  
PDF receipt generation & email sending  
Profile photo & bio support  
Filter & search for opportunities  
Export data to Excel  
Docker + Nginx production-ready setup  

---

## Tech Stack
- **Backend**: Django 4.x
- **Frontend**: Bootstrap 5
- **Database**: PostgreSQL
- **Deployment**: Docker, Nginx, Gunicorn
- **Other**: Pandas, xhtml2pdf, Pillow

---

## Installation (Local Development)

###  Clone the repository
```bash
git clone https://github.com/yourusername/internship_platform.git
cd internship_platform


 Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
 Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Apply migrations
bash
Copy
Edit
python manage.py migrate
##Create a superuser
bash
Copy
Edit
python manage.py createsuperuser
## Run the development server
bash
Copy
Edit
python manage.py runserver
Visit: http://127.0.0.1:8000

Docker Deployment (Production-Ready)
## Build & run containers
bash
Copy
Edit
docker-compose build
docker-compose up -d
## Access the application
Visit: http://localhost

## Stop containers
bash
Copy
Edit
docker-compose down



internship_platform/
│── accounts/           # Authentication & profile management
│── applications/       # Internship applications
│── opportunities/      # Internship listings
│── templates/          # HTML templates
│── static/              # CSS, JS, images
│── media/               # Uploaded files
│── nginx/               # Nginx config
│── Dockerfile           # Django + Gunicorn build
│── docker-compose.yml   # Multi-container setup
│── requirements.txt
│── README.md
