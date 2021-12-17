PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE urls(id integer primary key autoincrement, original_url text not null, short_url text not null unique, visitors text default 0, url_creation_time text not null);
COMMIT;