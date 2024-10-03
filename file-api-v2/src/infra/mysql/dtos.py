from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# User Model
class UserDTO(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)

    knowledge_bases = relationship("KnowledgeBaseDTO", back_populates="user")


# KnowledgeBase Model
class KnowledgeBaseDTO(Base):
    __tablename__ = 'knowledge_base'

    kb_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    kb_name = Column(String(255), nullable=False)
    bm25_index_location = Column(String(255), nullable=False)

    user = relationship("UserDTO", back_populates="knowledge_bases")
    pdf_documents = relationship(
        "PdfDocumentDTO",
        back_populates="knowledge_base",
        primaryjoin="KnowledgeBaseDTO.kb_id == PdfDocumentDTO.kb_id"
    )


    __table_args__ = (
        UniqueConstraint('user_id', 'kb_id', name='uq_user_kb'),
    )


# PdfDocument Model
class PdfDocumentDTO(Base):
    __tablename__ = 'pdf_document'

    doc_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('knowledge_base.user_id'), nullable=False)
    kb_id = Column(Integer, ForeignKey('knowledge_base.kb_id'), nullable=False)
    document_name = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False)
    raw_location = Column(String(255), nullable=False)
    chunked_location = Column(String(255), nullable=False)

    knowledge_base = relationship("KnowledgeBaseDTO", back_populates="pdf_documents", primaryjoin="PdfDocumentDTO.kb_id == KnowledgeBaseDTO.kb_id")

    __table_args__ = (
        UniqueConstraint('user_id', 'kb_id', 'doc_id', name='uq_user_kb_doc'),
    )
