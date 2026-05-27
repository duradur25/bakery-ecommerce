from fastapi import HTTPException
from connector import session
from sqlalchemy import select
from models import User, Product
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

def checkout():
    produk = session.execute(select(Product).filter_by(id=id)).first()

    