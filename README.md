# bakery-ecommerce

An artisan bakery e-commerce website called **La Pâtisserie** — built as a final project for a Web Programming course.

---

## Tech Stack

**Backend**
- Python + FastAPI
- SQLAlchemy (ORM)
- MySQL
- JWT (authentication)
- Passlib + bcrypt (password hashing)

**Frontend**
- HTML, CSS, JavaScript
- Tailwind CSS

---

## Features

- Register & Login (JWT)
- Product catalog
- Shopping cart
- Checkout & order history
- Feedback form
- Admin dashboard

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/duradur25/bakery-ecommerce.git
cd bakery-ecommerce
```

### 2. Setup database
Create a new MySQL database:
```sql
CREATE DATABASE bakery_ecommerce;
```

### 3. Setup backend
```bash
cd backend
```

Create a `.env` file:
```
DATABASE_URL=mysql+pymysql://root:password@localhost/bakery_ecommerce
SECRET_KEY=your_random_secret_key
```

Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv passlib bcrypt==4.0.1 python-jose[cryptography]
```

Run the server:
```bash
uvicorn main:app --reload
```

### 4. Run frontend
```bash
cd frontend
npx http-server . -p 3000 -o
```

Open `http://127.0.0.1:3000/home.html`

---

## Project Structure

```
bakery-ecommerce/
├── backend/
│   ├── main.py
│   ├── services.py
│   ├── models.py
│   ├── connector.py
│   └── .env
└── frontend/
    ├── home.html
    ├── saran.html
    ├── admin.html
    ├── request.js
    └── style.css
```
