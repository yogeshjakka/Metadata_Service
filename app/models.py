from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Dataset(Base):
    __tablename__ = "datasets"

    fqn = Column(String(255), primary_key=True)
    connection = Column(String(100))
    database = Column(String(100))
    schema = Column(String(100))
    table = Column(String(100))
    source_type = Column(Enum("MySQL", "MSSQL", "PostgreSQL"))

    columns = relationship("ColumnMeta", back_populates="dataset", cascade="all, delete")
    upstream = relationship("Lineage", foreign_keys='Lineage.downstream_fqn', back_populates="downstream")
    downstream = relationship("Lineage", foreign_keys='Lineage.upstream_fqn', back_populates="upstream")


class ColumnMeta(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_fqn = Column(String(255), ForeignKey("datasets.fqn"))
    name = Column(String(100))
    data_type = Column(String(100))

    dataset = relationship("Dataset", back_populates="columns")


class Lineage(Base):
    __tablename__ = "lineage"

    id = Column(Integer, primary_key=True)
    upstream_fqn = Column(String(255), ForeignKey("datasets.fqn"))
    downstream_fqn = Column(String(255), ForeignKey("datasets.fqn"))

    upstream = relationship("Dataset", foreign_keys=[upstream_fqn])
    downstream = relationship("Dataset", foreign_keys=[downstream_fqn])
