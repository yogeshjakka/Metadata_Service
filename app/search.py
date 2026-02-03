from sqlalchemy.orm import Session
from sqlalchemy import case
from .models import Dataset, ColumnMeta

def search_datasets(db: Session, q: str):
    q_like = f"%{q}%"

    score = case(
        (Dataset.table.like(q_like), 4),
        (ColumnMeta.name.like(q_like), 3),
        (Dataset.schema.like(q_like), 2),
        (Dataset.database.like(q_like), 1),
        else_=0,
    ).label("score")

    results = (
        db.query(Dataset, score)
        .outerjoin(ColumnMeta)
        .filter(
            Dataset.table.like(q_like)
            | ColumnMeta.name.like(q_like)
            | Dataset.schema.like(q_like)
            | Dataset.database.like(q_like)
        )
        .order_by(score.desc())
        .all()
    )
    return [r[0] for r in results]
