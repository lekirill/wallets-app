from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Numeric, UUID, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.current_timestamp()
    )


class Wallet(BaseModel):
    __tablename__ = 'wallet'

    label = Column(String(255), nullable=False)
    balance = Column(Numeric(precision=18, scale=2), default=0)

    transactions = relationship('Transaction', back_populates='wallet')


class Transaction(BaseModel):
    __tablename__ = 'transaction'

    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    txid = Column(String(36))
    amount = Column(Numeric(precision=18, scale=2))

    wallet = relationship('Wallet', back_populates='transactions')
