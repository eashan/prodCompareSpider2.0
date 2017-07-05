from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

engine = create_engine("mysql://root:abc123@localhost/prodcompare2?charset=utf8")

Base = declarative_base()



# association_table= Table('productStore',Base.metadata,
#                 Column("product_id",String(200),ForeignKey("products.id")),
#                 Column("store_url",String(200),ForeignKey("store.id"))
#                 )
class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(2000))
    product_url = Column(String(2000), primary_key=True)
    product_specs = Column(String(2000))
    stores = relationship("ProductStore", back_populates="product")

    def __repr__(self):
        return "<Product(Id='%s', productName='%s')>" % (
                             self.id, self.product_name)

class Store(Base):
    __tablename__ = "store"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1000), primary_key=True)
    products = relationship("ProductStore", back_populates="store")

    def __repr__(self):
        return "<Store(StoreId='%s', StoreName='%s')>" % (
                             self.id, self.name)

class ProductStore(Base):
    __tablename__ = "productstore"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer,ForeignKey("product.id"),primary_key=True)
    store_id = Column(Integer, ForeignKey("store.id"),primary_key = True)
    store_shipping = Column(String(2000))
    store_delivery = Column(String(2000))
    store_cod = Column(String(2000))
    store_emi = Column(String(2000))
    store_url = Column(String(2000))
    store_price = Column(Integer)
    store = relationship("Store", back_populates="products")
    product = relationship("Product", back_populates="stores")

Base.metadata.create_all(engine)
