from fastapi import HTTPException
from connector import session
from sqlalchemy import select
from models import User, Keranjang, Pesanan, Product, PesananDetail
from connector import hash_password, verify_password, create_token


def register(nama_lengkap, email, password, conf_pass):
    exist_data = session.execute(select(User).filter_by(email = email)).first()

    if exist_data:
        raise HTTPException(
            status_code=409, 
            detail="this email already exist!"
        )

    if len(password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password terlalu panjang"
        )

    if password != conf_pass:
        raise HTTPException(
            status_code=409,
            detail="password and configuration aren't same, please check it back"
        )
    
    hashed = hash_password(password)

    user = User(
        nama_lengkap = nama_lengkap,
        email = email,
        password = hashed
    )

    session.add(user)
    session.flush()
    session.commit()

    return{
        "message": "Create account success!"
    }

def login(email, password):
    user = session.execute(select(User).filter_by(email=email)).first()
                              
    if not user:
        raise HTTPException(
            status_code=409,
            detail="user tidak ditemukan"
        )
    
    valid = verify_password(password, user[0].password)
    
    if not valid:
        raise HTTPException(
            status_code=409,
            detail="Password salah"
        )
    
    access_token = create_token({
        "sub": str(user[0].id),
        "email": user[0].email,
        "nama": user[0].nama_lengkap
    })
    
    return{
        "access_token": access_token,
        "token_type": "bearer"
    }

def checkout(current_user: User, catatan: str):
    user_keranjang = session.execute(select(Keranjang).filter_by(user_id = current_user.id)).scalars().all()

    if not user_keranjang:
        raise HTTPException(
            status_code=409,
            detail="Keranjang Kosong!"
        )
    
    pesanan = Pesanan(
        user_id = current_user.id,
        catatan = catatan
    )

    for item in user_keranjang:
        session.delete(item)

    session.add(pesanan)
    session.flush()
    session.commit()

    return {
        "message": "Pesan Berhasil!",
        "detail": f"Id: {pesanan.id}"
    }

def tambah_keranjang(current_user: User, produk_id: int):


    keranjang = Keranjang(
        user_id= current_user.id,
        produk_id= produk_id,
        jumlah= 1
    )

    session.add(keranjang)
    session.flush()
    session.commit()

    return {
        "message": produk_id + "ditambahkan ke keranjang"
    }

def get_produk():
    products = session.execute(select(Product)).scalars().all()
    return {
        "produk": [
            {
                "id": p.id,
                "nama": p.nama,
                "harga": p.harga,
            }
            for p in products
        ]
    }

