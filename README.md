
# Coderr Backend

This project is a backend for a freelance developer platform built with **Django** and **Django REST Framework**.  
It provides a RESTful API for managing offers, offer details, orders and user reviews.


## Documentation

[API Documentation](https://github.com/Marcel-Goehn/coderr_backend/blob/main/API_DOCUMENTATION.md)


## Tech Stack

**Server:** Python, Django, Django REST Framework


## Features

- User authentication and profile adjustment
- Board-based permission system (owner and members)
- Business users can create offers and 3 different offer types per offer
- Customer users can create orders based on the offers
- Customers have the ability to give reviews about business users
- RESTful API design


## Installation



Clone the repository:
```bash
git clone https://github.com/Marcel-Goehn/coderr_backend
```
Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

Migrate the database:
```bash
python manage.py migrate
```

Start development server:
```bash
python manage.py runserver
```

    
## Related

Here is the related frontend

[Coderr Frontend](https://github.com/Developer-Akademie-Backendkurs/project.Coderr)


## Authors

- [@Marcel-Goehn](https://github.com/Marcel-Goehn)


## License


This project is licensed under the MIT License.


## Feedback

If you have any feedback, feel free to reach out: 
marcelgoehn@googlemail.com