from datetime import datetime,timezone
from sqlalchemy import String,Text,Boolean,DateTime,Integer,Float,JSON
from sqlalchemy.orm import Mapped,mapped_column
from pgvector.sqlalchemy import Vector
from .db import Base
from .config import settings
class Job(Base):
    __tablename__="jobs"
    id:Mapped[int]=mapped_column(primary_key=True)
    source_id:Mapped[str]=mapped_column(String(200),unique=True,index=True)
    title:Mapped[str]=mapped_column(String(300))
    company:Mapped[str]=mapped_column(String(200))
    location:Mapped[str]=mapped_column(String(200),index=True)
    description:Mapped[str]=mapped_column(Text)
    url:Mapped[str]=mapped_column(Text)
    level:Mapped[str]=mapped_column(String(50),default="mid")
    skills:Mapped[list]=mapped_column(JSON,default=list)
    responsibility_scope:Mapped[str]=mapped_column(Text,default="")
    manages_people:Mapped[bool]=mapped_column(Boolean,default=False)
    remote:Mapped[bool]=mapped_column(Boolean,default=False)
    active:Mapped[bool]=mapped_column(Boolean,default=True,index=True)
    content_hash:Mapped[str]=mapped_column(String(64))
    embedding=mapped_column(Vector(settings.embedding_dimensions))
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
class IngestionRun(Base):
    __tablename__="ingestion_runs"
    id:Mapped[int]=mapped_column(primary_key=True)
    status:Mapped[str]=mapped_column(String(20),default="running")
    source_count:Mapped[int]=mapped_column(Integer,default=0)
    created_count:Mapped[int]=mapped_column(Integer,default=0)
    updated_count:Mapped[int]=mapped_column(Integer,default=0)
    unchanged_count:Mapped[int]=mapped_column(Integer,default=0)
    closed_count:Mapped[int]=mapped_column(Integer,default=0)
    warning:Mapped[str]=mapped_column(Text,default="")
    estimated_cost_usd:Mapped[float]=mapped_column(Float,default=0)
    started_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    finished_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
