from datetime import datetime

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON, Boolean, Date

metadata = MetaData()

user = Table("user", metadata,
             Column("id", Integer, primary_key=True, autoincrement=True),
             Column("email", String, nullable=False),
             Column("username", String, nullable=False),
             Column("hashed_password", String, nullable=False),
             Column("registered_at", TIMESTAMP, default=datetime.utcnow),
             Column("is_active", Boolean, default=True, nullable=False),
             Column("is_superuser", Boolean, default=False, nullable=False),
             Column("is_verified", Boolean, default=False, nullable=False)
             )

film = Table("film", metadata,
             Column("id", Integer, primary_key=True),
             Column("name", String, nullable=False),
             Column("genre", String, nullable=False),
             Column("short_description", String, nullable=False),
             Column("full_description", String, nullable=False),
             Column("date", Date, nullable=False),
             )

review = Table("review", metadata,
               Column("film_id", Integer),
               Column("comment", String),
               Column("grade", Integer),
               )
