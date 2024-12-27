from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, BigInteger, ForeignKey


class Base(DeclarativeBase):
    def __repr__(self):
        return f'{self.__class__.__name__}'


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    history: Mapped['ChatHistory'] = relationship('ChatHistory', back_populates='user', lazy='joined')


class ChatHistory(Base):
    __tablename__ = "chat_history"

    history_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    messages: Mapped[str] = mapped_column(Text, server_default="")

    user: Mapped['User'] = relationship('User', back_populates='history', lazy='joined')