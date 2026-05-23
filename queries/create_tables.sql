DROP TABLE IF EXISTS "PricesXCollections", "Items", "Prices", "Hazard", "Collections", "Halls" CASCADE;

CREATE TABLE IF NOT EXISTS "Collections" ( id serial, name character varying(32), description character varying(512), start date, "end" date, PRIMARY KEY (id), CONSTRAINT coll_alt_key UNIQUE (name), CONSTRAINT end_after_start CHECK ("end" > start) );

CREATE TABLE IF NOT EXISTS "Items" ( id serial, name character varying(64) NOT NULL, description text, insurance numeric CHECK (insurance >= 0), century integer, collection_id integer, hall_id integer, height double precision CHECK (height >= 0), width double precision CHECK (width >= 0), length double precision CHECK (length >= 0), temperature double precision, wetness double precision CHECK (wetness >= 0), safety_level integer, PRIMARY KEY (id), CONSTRAINT items_alt_key UNIQUE (name, description) );

ALTER TABLE IF EXISTS "Items" ADD CONSTRAINT collection_fk FOREIGN KEY (collection_id) REFERENCES "Collections" (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE NOT VALID;
