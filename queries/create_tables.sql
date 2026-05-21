CREATE TABLE IF NOT EXISTS "Halls" ( id serial, name character varying(32), PRIMARY KEY (id), CONSTRAINT halls_alt_key UNIQUE (name) );

CREATE TABLE IF NOT EXISTS "Collections" ( id serial, name character varying(32), description character varying(512), start date, "end" date, PRIMARY KEY (id), CONSTRAINT coll_alt_key UNIQUE (name), CONSTRAINT end_after_start CHECK ("end" > start) );

CREATE TABLE IF NOT EXISTS "Items" ( id serial, name character varying(64) NOT NULL, description text, insurance numeric CHECK (insurance >= 0), century integer, collection_id integer, hall_id integer, height double precision CHECK (height >= 0), width double precision CHECK (width >= 0), length double precision CHECK (length >= 0), temperature double precision, wetness double precision CHECK (wetness >= 0), safety_level integer, PRIMARY KEY (id), CONSTRAINT items_alt_key UNIQUE (name, description) );

CREATE TABLE IF NOT EXISTS "Prices" ( id serial, type integer NOT NULL, cost numeric CHECK (cost >= 0), PRIMARY KEY (id) );

CREATE TABLE IF NOT EXISTS "Hazard" ( id serial, name character varying(32) NOT NULL, description text, PRIMARY KEY (id), CONSTRAINT hazard_alt_pk UNIQUE (name) );

CREATE TABLE IF NOT EXISTS "PricesXCollections" ( price_id integer NOT NULL, collection_id integer NOT NULL, PRIMARY KEY (price_id, collection_id) );

ALTER TABLE IF EXISTS "Items" ADD CONSTRAINT collection_fk FOREIGN KEY (collection_id) REFERENCES "Collections" (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID;

ALTER TABLE IF EXISTS "Items" ADD CONSTRAINT hall_fk FOREIGN KEY (hall_id) REFERENCES "Halls" (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID;

ALTER TABLE IF EXISTS "Items" ADD CONSTRAINT safety_fk FOREIGN KEY (safety_level) REFERENCES "Hazard" (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID;

ALTER TABLE IF EXISTS "PricesXCollections" ADD CONSTRAINT price_fk FOREIGN KEY (price_id) REFERENCES "Prices" (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID;

ALTER TABLE IF EXISTS "PricesXCollections" ADD CONSTRAINT collection_fk FOREIGN KEY (collection_id) REFERENCES "Collections" (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID;
