SQLite version 3.41.1 2023-03-10 12:13:52
Enter ".help" for usage hints.
sqlite> drop table if exists users;
    create table users (
    email email not null,
    password text not null
);
