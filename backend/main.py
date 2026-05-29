from fastapi import FastAPI, Depends
from services import register, login, checkout, tambah_keranjang, get_produk
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import User
from connector import get_current_user


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

class PesananIn(BaseModel):
    catatan: str = ""


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

@app.post('/pesanan')
def checkout_api(data: PesananIn, current_user: User = Depends(get_current_user)):
    return checkout(
        current_user = current_user,
        catatan = data.catatan
    )
    
@app.post('/keranjang/item')
def tambah_keranjang_api(data: KeranjangItemIn, current_user: User = Depends(get_current_user)):
    return tambah_keranjang(
        current_user= current_user,
        produk_id= data.produk_id
    )

@app.get('/produk')
def get_produk_api():
    return get_produk()

