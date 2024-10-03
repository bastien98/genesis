from file_api_v2.utills.document_manager import AbstractDocumentManager, LocalFileSystemDocumentManager


def get_document_manager() -> AbstractDocumentManager:
    return LocalFileSystemDocumentManager()
