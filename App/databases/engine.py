from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv, find_dotenv
import os
from App.config import DB

load_dotenv(find_dotenv())

engine = create_async_engine(url=DB)

main_session = async_sessionmaker(bind=engine)