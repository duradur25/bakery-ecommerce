from fastapi import FastAPI
from services import register, login
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)


class RegisterRequest(BaseModel):
    nama_lengkap: str
    email: str
    password: str
    conf_pass: str

class LoginRequest(BaseModel):
    email: str
    password: str

class KeranjangItemIn(BaseModel):
    produk_id: int
    jumlah: int

class KeranjangItemUpdate(BaseModel):
    jumlah: int


@app.post('/register')
def register_api(data: RegisterRequest):
    return register(
        nama_lengkap= data.nama_lengkap,
        email= data.email,
        password= data.password,
        conf_pass= data.conf_pass
        )

@app.post('/login')
def login_api(data: LoginRequest):
    return login(
        email= data.email,
        password= data.password
    )

