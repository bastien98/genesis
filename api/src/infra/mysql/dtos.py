from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class UserDTO(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)

    kbs = relationship("KnowledgeBaseDTO", back_populates="user", cascade="all, delete-orphan")


class KnowledgeBaseDTO(Base):
    __tablename__ = 'knowledge_bases'

    kb_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)

    user = relationship("UserDTO", back_populates="kbs")

    docs = relationship("DocumentDto", back_populates="knowledge_base", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('user_id', 'name', name='unique_user_kb_name'),)


class DocumentDto(Base):
    __tablename__ = 'documents'

    doc_id = Column(Integer, primary_key=True, autoincrement=True)
    kb_id = Column(Integer, ForeignKey('knowledge_bases.kb_id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    source = Column(String(255), nullable=True)

    knowledge_base = relationship("KnowledgeBaseDTO", back_populates="docs")

    __table_args__ = (UniqueConstraint('kb_id', 'name', name='unique_kb_doc_name'),)
