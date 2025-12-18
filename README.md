# DMED Medical Platform - Backend API

FastAPI asosidagi tibbiy platforma backend servisi. Bemorlar, tibbiy kartalar, hodimlar va autentifikatsiya uchun to'liq RESTful API.

## Texnologiyalar

- **FastAPI** - Async web framework
- **PostgreSQL** - Ma'lumotlar bazasi
- **SQLAlchemy** - ORM (async)
- **Alembic** - Database migrations
- **JWT** - Token-based authentication
- **Pydantic v2** - Data validation

## Tizim Arxitekturasi

```
app/
├── api/v1/          # API endpoints
├── models/          # Database models
├── schemas/         # Pydantic schemas (request/response)
├── repositories/    # Database queries
├── services/        # Business logic
├── core/            # Config, security, exceptions
├── db/              # Database connection
└── utils/           # Helper functions
```

## O'rnatish va Ishga Tushirish

### 1. Repository ni clone qilish

```bash
git clone <repository-url>
cd DMED_2
```

### 2. Virtual environment yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Environment variables sozlash

`.env` faylini yarating va quyidagi ma'lumotlarni kiriting:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/dmed_db

# Security
SECRET_KEY=your-secret-key-here-min-32-characters
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Application
APP_NAME=DMED Medical Platform
APP_VERSION=1.0.0
DEBUG=True
```

### 5. Database yaratish

PostgreSQL da database yarating:

```sql
CREATE DATABASE dmed_db;
```

### 6. Migration ishga tushirish

```bash
alembic upgrade head
```

### 7. Serverni ishga tushirish

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

API endi quyidagi manzillarda mavjud:
- **API:** http://localhost:8080
- **Swagger UI (API Documentation):** http://localhost:8080/docs
- **ReDoc:** http://localhost:8080/redoc

## API Endpoints

### Authentication

#### Login (Hodimlar uchun)
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "jshshir": "12345678901234",
  "password": "123456"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "full_name": "Alisher Navoiy",
    "jshshir": "12345678901234",
    "roles": ["shifokor", "manager"],
    "phone": "+998901234567"
  }
}
```

### Locations (Hududlar)

#### Hududlar va shaharlarni import qilish (Admin)
```http
POST /api/v1/locations/admin/import
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json

{
  "regions": [
    {
      "name": "Toshkent shahri",
      "code": "TOS",
      "cities": ["Toshkent"]
    }
  ]
}
```

#### Barcha hududlarni olish
```http
GET /api/v1/locations/regions

Response:
[
  {
    "id": 1,
    "name": "Toshkent shahri",
    "code": "TOS"
  }
]
```

#### Hudud bo'yicha shaharlarni olish
```http
GET /api/v1/locations/regions/1/cities

Response:
[
  {
    "id": 1,
    "name": "Toshkent",
    "region_id": 1
  }
]
```

### Patients (Bemorlar)

#### Yangi bemor yaratish
```http
POST /api/v1/patients
Content-Type: application/json

{
  "first_name": "Alisher",
  "last_name": "Navoiy",
  "father_name": "Ahmadovich",
  "birth_date": "1990-05-15",
  "gender": "male",
  "phone": "+998901234567",
  "address": "Toshkent, Yunusobod tumani",
  "city_id": 1
}

Response:
{
  "id": 1,
  "first_name": "Alisher",
  "last_name": "Navoiy",
  "father_name": "Ahmadovich",
  "full_name": "Navoiy Alisher Ahmadovich",
  "birth_date": "1990-05-15",
  "gender": "male",
  "phone": "+998901234567",
  "address": "Toshkent, Yunusobod tumani",
  "city_id": 1,
  "medical_card_number": "AB1234",
  "created_at": "2025-12-18T10:30:00Z"
}
```

#### Bemorlarni qidirish
```http
GET /api/v1/patients?search=Alisher&gender=male&limit=10&offset=0

Parameters:
- search: Ism, familiya yoki tibbiy karta raqami
- gender: male/female
- city_id: Shahar ID
- limit: Nechta natija (default: 100)
- offset: Nechta o'tkazish (default: 0)
```

#### Bemorni yangilash
```http
PUT /api/v1/patients/1
Content-Type: application/json

{
  "phone": "+998901234568",
  "address": "Yangi manzil"
}
```

#### Bemorni o'chirish
```http
DELETE /api/v1/patients/1
```

### Users (Hodimlar) - Admin Only

**Barcha user endpoints uchun Admin authentication kerak:**
```
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

#### Hodim yaratish
```http
POST /api/v1/admin/users
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json

{
  "full_name": "Alisher Navoiy",
  "jshshir": "12345678901234",
  "roles": ["shifokor", "manager"],
  "gender": "male",
  "birth_date": "1985-03-20",
  "phone": "+998901234567"
}

Response:
{
  "id": 1,
  "full_name": "Alisher Navoiy",
  "jshshir": "12345678901234",
  "password": "483726",
  "roles": ["shifokor", "manager"],
  "gender": "male",
  "birth_date": "1985-03-20",
  "phone": "+998901234567",
  "created_at": "2025-12-18T10:30:00Z"
}
```

**Muhim:** Agar bir hil JSHSHIR bilan qayta hodim yaratmoqchi bo'lsangiz, yangi rol oldingi rollarga qo'shiladi (yangi hodim yaratilmaydi).

#### Barcha hodimlarni ko'rish
```http
GET /api/v1/admin/users
Authorization: Basic YWRtaW46YWRtaW4xMjM=

Response:
[
  {
    "full_name": "Alisher Navoiy",
    "jshshir": "12345678901234",
    "password": "483726",
    "roles": ["shifokor", "manager"],
    "phone": "+998901234567"
  }
]
```

#### Hodimni yangilash
```http
PUT /api/v1/admin/users/1
Authorization: Basic YWRtaW46YWRtaW4xMjM=
Content-Type: application/json

{
  "roles": ["shifokor", "manager", "royhatga_oluvchi"],
  "phone": "+998901234568"
}
```

#### Hodimni o'chirish
```http
DELETE /api/v1/admin/users/1
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

## Rollar (User Roles)

Tizimda quyidagi rollar mavjud:

- **manager** - Menejer
- **shifokor** - Shifokor
- **amaliyot_hamshirasi** - Amaliyot hamshirasi
- **royhatga_oluvchi** - Ro'yhatga oluvchi
- **patronaj_hamshirasi** - Patronaj hamshirasi

Bir hodimda bir nechta rol bo'lishi mumkin.

## Authentication

### Admin Authentication
Admin endpoints uchun HTTP Basic Auth ishlatiladi:
- Username: `admin`
- Password: `admin123`

### User Authentication
Hodimlar uchun JWT token-based authentication:
1. `/api/v1/auth/login` orqali login qiling (JSHSHIR + password)
2. Javobda `access_token` qaytadi
3. Keyingi requestlarda header ga qo'shing:
   ```
   Authorization: Bearer <access_token>
   ```

Token amal qilish muddati: **24 soat**

## Validatsiyalar

### JSHSHIR (Passport Number)
- 14 ta raqamdan iborat bo'lishi kerak
- Unique (takrorlanmasligi kerak)

### Phone Number
- `+998` bilan boshlanishi kerak
- Jami 13 ta belgi

### Medical Card Number
- Avtomatik generatsiya qilinadi
- Format: 2 ta harf + 4 ta raqam (masalan: AB1234)
- Unique (takrorlanmasligi kerak)

### Password
- Hodim yaratilganda avtomatik 6 raqamli parol generatsiya qilinadi
- Parollar ochiq ko'rinishda saqlanadi (hash qilinmaydi)
- Admin barcha parollarni ko'ra oladi

### Gender
- `male` yoki `female` bo'lishi kerak

## Error Responses

API quyidagi error formatini qaytaradi:

```json
{
  "detail": "Error message here"
}
```

HTTP Status Codes:
- `200` - Success
- `201` - Created
- `204` - No Content (deleted)
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `404` - Not Found
- `409` - Conflict (duplicate)
- `500` - Internal Server Error

## Database Schema

### Users (Hodimlar)
- `id` - Integer (Primary Key)
- `full_name` - String (255)
- `jshshir` - String (14, Unique)
- `password` - String (6)
- `roles` - Array of Strings
- `gender` - String (10)
- `birth_date` - Date
- `phone` - String (20, Nullable)
- `created_at` - DateTime
- `updated_at` - DateTime

### Patients (Bemorlar)
- `id` - Integer (Primary Key)
- `first_name` - String (100)
- `last_name` - String (100)
- `father_name` - String (100, Nullable)
- `birth_date` - Date
- `gender` - String (10)
- `phone` - String (20, Nullable)
- `address` - Text (Nullable)
- `city_id` - Integer (Foreign Key)
- `created_at` - DateTime
- `updated_at` - DateTime

### Medical Cards (Tibbiy kartalar)
- `id` - Integer (Primary Key)
- `patient_id` - Integer (Foreign Key, Unique)
- `card_number` - String (6, Unique)
- `created_at` - DateTime

### Regions (Hududlar)
- `id` - Integer (Primary Key)
- `name` - String (100, Unique)
- `code` - String (10, Unique)

### Cities (Shaharlar)
- `id` - Integer (Primary Key)
- `name` - String (100)
- `region_id` - Integer (Foreign Key)

## Development

### Migration yaratish

Model o'zgartirsangiz, yangi migration yarating:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Loglar

Loglar `logs/app.log` faylida saqlanadi. Log level: INFO

### Testing

Swagger UI orqali barcha endpointlarni test qilishingiz mumkin:
http://localhost:8080/docs

## Frontend Integration Misol

### Axios bilan ishlatish

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080/api/v1';

// Login
const login = async (jshshir, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/login`, {
    jshshir,
    password
  });

  // Token ni saqlash
  localStorage.setItem('token', response.data.access_token);
  localStorage.setItem('user', JSON.stringify(response.data.user));

  return response.data;
};

// Axios instance with auth
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Har bir request ga token qo'shish
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Bemorlarni olish
const getPatients = async (searchParams) => {
  const response = await api.get('/patients', { params: searchParams });
  return response.data;
};

// Yangi bemor yaratish
const createPatient = async (patientData) => {
  const response = await api.post('/patients', patientData);
  return response.data;
};

// Hududlarni olish
const getRegions = async () => {
  const response = await api.get('/locations/regions');
  return response.data;
};

// Shaharlarni olish
const getCities = async (regionId) => {
  const response = await api.get(`/locations/regions/${regionId}/cities`);
  return response.data;
};
```

### Fetch API bilan ishlatish

```javascript
const API_BASE_URL = 'http://localhost:8080/api/v1';

// Login
async function login(jshshir, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ jshshir, password }),
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  } else {
    throw new Error(data.detail);
  }
}

// Helper function for authenticated requests
async function fetchWithAuth(url, options = {}) {
  const token = localStorage.getItem('token');

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}

// Bemorlarni olish
async function getPatients(params = {}) {
  const queryString = new URLSearchParams(params).toString();
  return fetchWithAuth(`/patients?${queryString}`);
}

// Yangi bemor yaratish
async function createPatient(patientData) {
  return fetchWithAuth('/patients', {
    method: 'POST',
    body: JSON.stringify(patientData),
  });
}
```

## CORS

Backend CORS ni ochiq holda sozlangan (barcha origin larga ruxsat berilgan). Production da buni cheklang:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Muammolarni Hal Qilish

### Database connection error
`.env` faylida `DATABASE_URL` to'g'ri ekanligini tekshiring va PostgreSQL ishlab turganiga ishonch hosil qiling.

### Migration error
```bash
alembic downgrade -1
alembic upgrade head
```

### Port band
Agar 8080 port band bo'lsa, boshqa port ishlatishingiz mumkin:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production

Production muhitida quyidagilarni o'zgartiring:

1. `.env` faylida `DEBUG=False`
2. Secret key ni xavfsiz qiymatga o'zgartiring
3. CORS ni cheklang
4. HTTPS ishlatish
5. Gunicorn bilan ishga tushirish:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
```

## License

MIT

## Muallif

[Turabek](https://github.com/jorabeknazarmatov)
