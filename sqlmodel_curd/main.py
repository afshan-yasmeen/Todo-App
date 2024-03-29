from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional

class Diary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True)
    secret_name: str



sqlite_url = f"postgresql://ToDoApp_owner:cP03BKAnNGrv@ep-silent-block-a5mktk6i.us-east-2.aws.neon.tech/ToDoApp?sslmode=require"


engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app:FastAPI = FastAPI(lifespan=lifespan)


@app.post("/diary/")
def create_diary(diary: Diary):
    with Session(engine) as session:
        session.add(diary)
        session.commit()
        session.refresh(diary)
        return diary


@app.put("/diary/")
def update_diary(diary:Diary):
    with Session(engine) as session:
        statement = select(Diary).where(Diary.id == diary.id)
        results = session.exec(statement)
        db_diary = results.one()

        db_diary.content = diary.content
        session.add(db_diary)
        session.commit()
        session.refresh(db_diary)
        return db_diary


@app.get("/diary/")
def read_diary():
    with Session(engine) as session:
        diaries = session.exec(select(Diary)).all()
        return diaries
    

@app.delete("/diary/")
def delete_diary(diary:Diary):
    with Session(engine) as session:
        statement = select(Diary).where(Diary.id == diary.id)
        results = session.exec(statement)
        db_diary = results.one()

        session.delete(db_diary)
        session.commit()
        return "Diary Deleted!"