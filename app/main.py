from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Dataset, ColumnMeta, Lineage
from .schemas import DatasetCreate, LineageCreate
from .search import search_datasets
from .lineage import build_graph, has_cycle

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/datasets")
def create_dataset(data: DatasetCreate, db: Session = Depends(get_db)):
    conn, dbn, sch, tbl = data.fqn.split(".")
    dataset = Dataset(
        fqn=data.fqn,
        connection=conn,
        database=dbn,
        schema=sch,
        table=tbl,
        source_type=data.source_type,
    )
    db.add(dataset)
    for c in data.columns:
        db.add(ColumnMeta(dataset_fqn=data.fqn, name=c.name, data_type=c.data_type))
    db.commit()
    return {"msg": "Dataset created"}

@app.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    return search_datasets(db, q)

@app.post("/lineage")
def add_lineage(rel: LineageCreate, db: Session = Depends(get_db)):
    graph = build_graph(db)
    if has_cycle(graph, rel.upstream_fqn, rel.downstream_fqn):
        raise HTTPException(status_code=400, detail="Cycle detected in lineage")

    db.add(Lineage(**rel.dict()))
    db.commit()
    return {"msg": "Lineage added"}
