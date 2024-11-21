from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


engine = create_engine("sqlite:///posts.db")
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(bind=engine)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String())
