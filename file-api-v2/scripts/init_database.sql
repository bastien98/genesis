CREATE TABLE user
(
    user_id  INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    CONSTRAINT unique_username UNIQUE (username)
);


CREATE TABLE knowledge_base
(
    kb_id               INT AUTO_INCREMENT,
    user_id             INT,
    kb_name             VARCHAR(255),
    bm25_index_location VARCHAR(255) NOT NULL ,
    PRIMARY KEY (kb_id),
    UNIQUE KEY (user_id, kb_id),
    FOREIGN KEY (user_id) REFERENCES User (user_id)
);


CREATE TABLE pdf_document
(
    user_id          INT,
    kb_id            INT,
    doc_id           INT,
    document_name    VARCHAR(255) NOT NULL,
    source           VARCHAR(255) NOT NULL,
    raw_location     VARCHAR(255) NOT NULL,
    chunked_location VARCHAR(255) NOT NULL,
    PRIMARY KEY (doc_id),
    UNIQUE KEY (user_id, kb_id, doc_id),
    FOREIGN KEY (user_id, kb_id) REFERENCES knowledge_base (user_id, kb_id)
);



INSERT INTO User (username)
VALUES ('Bastien');

INSERT INTO knowledge_base (user_id, kb_name, bm25_index_location)
VALUES (1, 'kb-1', '/Users/bmoenaert/repositories/super-rag/data/processed/1');




# select * from superRag.KnowledgeBase