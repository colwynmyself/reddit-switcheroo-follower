CREATE SEQUENCE links_id_seq;

CREATE TABLE links(
   id INT PRIMARY KEY NOT NULL DEFAULT nextval('links_id_seq'),
   url VARCHAR(500) NOT NULL,
   text VARCHAR(100) NOT NULL,
   depth INT NOT NULL
);

ALTER SEQUENCE links_id_seq OWNED BY links.id;
