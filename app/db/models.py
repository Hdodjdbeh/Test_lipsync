from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String, Column, Text

from app.db.database import Base


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task(Base):
    def __repr__(self):
        return (
            f"Task("
            f"id={self.id}, "
            f"status={self.status}"
            f")"
        )
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True)

    text_hash = Column(
        String(64),
        nullable=False,
        index=True,
    )

    status = Column(
        SqlEnum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING,
    )

    video_path = Column(
        String,
        nullable=True,
    )

    error = Column(
        Text,
        nullable=True,
    )