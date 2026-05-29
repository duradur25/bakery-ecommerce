from connector import engine
from connector import Base
from sqlalchemy.orm import Mapped,  mapped_column, relationship
from sqlalchemy import String, ForeignKey

class Admin(Base):
    __tablename__ = "admin_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    def __repr__(self) -> str:
        return f"Id: {self.id}, Email: {self.email}, Password: {self.password}"


class User(Base):
    __tablename__ = "user_table"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nama_lengkap: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    saran: Mapped[str] = mapped_column(String(100), nullable=True)

    keranjang = relationship("Keranjang", back_populates="user")
    pesanan = relationship("Pesanan", back_populates="user")

    def __repr__(self) -> str:
        return f"id: {self.id}, Fullname: {self.nama_lengkap}, Email: {self.email}, Password: {self.password}\nSaran: {self.saran}"


class Product(Base):
    __tablename__ = "product_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    nama: Mapped[str] = mapped_column(String(40))
    harga: Mapped[int]

    keranjang = relationship("Keranjang", back_populates="produk")

    def __repr__(self) -> str:
        return f"Fullname: {self.id}, Email: {self.nama}, Password: {self.harga}"


class Keranjang(Base):
    __tablename__ = "keranjang"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=False)
    produk_id: Mapped[int] = mapped_column(ForeignKey("product_table.id"), nullable=False)
    jumlah: Mapped[int] = mapped_column(default=1)

    user  = relationship("User",    back_populates="keranjang")
    produk = relationship("Product", back_populates="keranjang")


class Pesanan(Base):
    __tablename__ = "pesanan"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user_table.id"), nullable=False)
    catatan: Mapped[str] = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="pesanan")
    details = relationship("PesananDetail", back_populates="pesanan")

class PesananDetail(Base):
    __tablename__ = "pesanan_detail"

    id         : Mapped[int] = mapped_column(primary_key=True)
    pesanan_id : Mapped[int] = mapped_column(ForeignKey("pesanan.id"))
    produk_id  : Mapped[int] = mapped_column(ForeignKey("product_table.id"))
    jumlah     : Mapped[int] 
    harga      : Mapped[int] 

    pesanan = relationship("Pesanan", back_populates="details")
    produk  = relationship("Product")

Base.metadata.create_all(engine)

