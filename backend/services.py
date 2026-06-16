from fastapi import HTTPException
from connector import session
from sqlalchemy import select
from models import User, Keranjang, Pesanan, Product, PesananDetail, Saran
from connector import hash_password, verify_password, create_token


def register(nama_lengkap, email, password, conf_pass):
    exist_data = session.execute(select(User).filter_by(email=email)).first()

    if exist_data:
        raise HTTPException(status_code=409, detail="Email sudah terdaftar!")

    if len(password) > 72:
        raise HTTPException(status_code=400, detail="Password terlalu panjang")

    if password != conf_pass:
        raise HTTPException(status_code=409, detail="Password tidak cocok")

    hashed = hash_password(password)

    user = User(
        nama_lengkap=nama_lengkap, 
        email=email, 
        password=hashed
    )
    
    session.add(user)
    session.commit()
    return {"message": "Create account success!"}


def login(email, password):
    user = session.execute(select(User).filter_by(email=email)).first()

    if not user:
        raise HTTPException(status_code=409, detail="User tidak ditemukan")

    valid = verify_password(password, user[0].password)

    if not valid:
        raise HTTPException(status_code=409, detail="Password salah")

    access_token = create_token({
        "sub": str(user[0].id),
        "email": user[0].email,
        "nama": user[0].nama_lengkap
    })

    return {"access_token": access_token, "token_type": "bearer"}


def tambah_keranjang(current_user: User, produk_id: int, jumlah: int):
    existing = session.execute(
        select(Keranjang).filter_by(user_id=current_user.id, produk_id=produk_id)
    ).scalar_one_or_none()

    if existing:
        existing.jumlah += jumlah
    else:
        keranjang = Keranjang(
            user_id=current_user.id,
            produk_id=produk_id,
            jumlah=jumlah,
        )
        session.add(keranjang)

    session.commit()
    return {"message": f"{produk_id} ditambahkan ke keranjang"}


def get_keranjang(current_user: User):
    items = session.execute(
        select(Keranjang).filter_by(user_id=current_user.id)
    ).scalars().all()

    return {
        "items": [
            {
                "id": item.id,
                "jumlah": item.jumlah,
                "produk": {
                    "id": item.produk.id,
                    "nama": item.produk.nama,
                    "harga": item.produk.harga,
                }
            }
            for item in items
        ]
    }


def update_keranjang(current_user: User, item_id: int, jumlah: int):
    item = session.execute(
        select(Keranjang).filter_by(id=item_id, user_id=current_user.id)
    ).scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    item.jumlah = jumlah
    session.commit()
    return {"message": "Jumlah diperbarui"}


def hapus_item_keranjang(current_user: User, item_id: int):
    item = session.execute(
        select(Keranjang).filter_by(item_id=item_id, user_id=current_user.id)
    ).scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    session.delete(item)
    session.commit()
    return {"message": "Item dihapus"}


def kosongkan_keranjang(current_user: User):
    items = session.execute(
        select(Keranjang).filter_by(user_id=current_user.id)
    ).scalars().all()

    for item in items:
        session.delete(item)

    session.commit()
    return {"message": "Keranjang dikosongkan"}


def checkout(current_user: User, catatan: str):
    user_keranjang = session.execute(
        select(Keranjang).filter_by(user_id=current_user.id)
    ).scalars().all()

    if not user_keranjang:
        raise HTTPException(status_code=409, detail="Keranjang Kosong!")

    pesanan = Pesanan(user_id=current_user.id, catatan=catatan)
    session.add(pesanan)
    session.flush()

    for item in user_keranjang:
        detail = PesananDetail(
            pesanan_id=pesanan.id,
            produk_id=item.produk_id,
            jumlah=item.jumlah,
            harga=item.produk.harga,  # ambil harga dari produk, bukan keranjang
        )
        session.add(detail)
        session.delete(item)

    session.commit()
    return {"message": "Pesan Berhasil!", "id": pesanan.id}


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

def kirim_saran(nama_lengkap: str, email: str, subjek: str, rating: str, pesan: str):
    check_spam = session.execute(select(Saran).filter_by(email= email)).first()

    if check_spam:
        raise HTTPException(
            status_code=409,
            detail="email sudah pernah kirim saran"
        )

    saran = Saran(
        nama_lengkap = nama_lengkap,
        email = email,
        subjek = subjek,
        rating = rating,
        pesan = pesan
    )

    session.add(saran)
    session.commit()

    return{
        "message": "Kirim saran berhasil!"
    }