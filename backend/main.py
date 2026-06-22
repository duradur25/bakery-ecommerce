from fastapi import FastAPI, Depends
from services import register, login, checkout, tambah_keranjang, get_produk, get_keranjang, update_keranjang, hapus_item_keranjang, kosongkan_keranjang, kirim_saran
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import User, Pesanan, Saran
from connector import get_current_user, session
from sqlalchemy import select


app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://lapatisserie-frontend.onrender.com",
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

class SaranIn(BaseModel):
    nama_lengkap: str
    email: str
    subjek: str = ""
    rating: str = ""
    pesan: str


@app.get('/')
def root():
    return {"message": "Bakery Ecommerce API is running"}

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
        produk_id= data.produk_id,
        jumlah= data.jumlah
    )

@app.get('/keranjang')
def get_keranjang_api(current_user: User = Depends(get_current_user)):
    return get_keranjang(current_user=current_user)

@app.put('/keranjang/item/{item_id}')
def update_keranjang_api(item_id: int, data: KeranjangItemUpdate, current_user: User = Depends(get_current_user)):
    return update_keranjang(
        current_user=current_user,
        item_id=item_id,
        jumlah=data.jumlah
    )

@app.delete('/keranjang/item/{item_id}')
def hapus_item_api(item_id: int, current_user: User = Depends(get_current_user)):
    return hapus_item_keranjang(current_user=current_user, item_id=item_id)

@app.delete('/keranjang')
def kosongkan_keranjang_api(current_user: User = Depends(get_current_user)):
    return kosongkan_keranjang(current_user=current_user)

@app.get('/produk')
def get_produk_api():
    return get_produk()

@app.post('/saran')
def kirim_saran_api(data: SaranIn):
    return kirim_saran(
        nama_lengkap= data.nama_lengkap,
        email= data.email,
        subjek= data.subjek,
        rating= data.rating,
        pesan= data.pesan
    )

@app.get('/admin/pesanan')
def admin_pesanan():
    pesanan = session.execute(select(Pesanan)).scalars().all()
    return {
        "pesanan": [
            {
                "id": p.id,
                "user_id": p.user_id,
                "catatan": p.catatan,
                "total": sum(d.harga * d.jumlah for d in p.details)
            }
            for p in pesanan
        ]
    }

@app.get('/admin/saran')
def admin_saran():
    saranList = session.execute(select(Saran)).scalars().all()
    return {
        "saran": [
            {"nama": s.nama_lengkap, "subjek": s.subjek, "rating": s.rating, "pesan": s.pesan}
            for s in saranList
        ]
    }

@app.get('/admin/users')
def admin_users():
    from sqlalchemy import func
    total = session.execute(select(func.count()).select_from(User)).scalar()
    return {"total": total}