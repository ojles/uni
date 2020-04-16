create table action (
    id bigint auto_increment primary key,
    type varchar(100) not null,
    source varchar(255) not null,
    destination varchar(255) not null
);