set foreign_key_checks = 0;

drop table if exists university_object;
drop table if exists person;
drop table if exists department;
drop table if exists faculty;
drop table if exists division;
drop table if exists link;

create table university_object (
    id bigint auto_increment,
    name varchar(256) not null,
    class varchar(256) not null,
    major_id bigint,
    primary key(id),
    foreign key(major_id) references university_object(id) on update cascade on delete cascade
);

create table person (
    id bigint,
    birth_date date not null,
    foreign key (id) references university_object(id) on update cascade on delete cascade
);

create table department (
    id bigint,
    head_of_id bigint not null,
    email varchar(256) not null,
    creation_date date not null,
    foreign key (id) references university_object(id) on update cascade on delete cascade,
    foreign key (head_of_id) references person(id) on update cascade on delete cascade
);

create table faculty (
    id bigint,
    address varchar(256) not null,
    foreign key (id) references department(id) on update cascade on delete cascade
);

create table division (
    id bigint,
    room_number varchar(256) not null,
    foreign key (id) references department(id) on update cascade on delete cascade
);

create table link (
    id bigint,
    url varchar(256) not null,
    foreign key (id) references university_object(id) on update cascade on delete cascade
);

insert into university_object (id, name, class, major_id) values
(1, 'Faculty of Applied Mathematics', 'FACULTY', null),
(2, 'Division of Information Systems', 'DIVISION', 1),
(3, 'Division of Discrete Analysis and Intelligent System', 'DIVISION', 1),
(4, 'Division of Computational Mathematics', 'DIVISION', 1),
(5, 'Heorhiy Shynkarenko', 'PERSON', 2),
(6, 'Yaroslav Sokolovskyy', 'PERSON', 2),
(7, 'Petro Venherskyi', 'PERSON', 2),
(8, 'Mykola Prytula', 'PERSON', 3),
(9, 'Nadiya Kolos', 'PERSON', 3);

insert into person (id, birth_date) values
(5, '1957-12-03'),
(6, '1964-11-04'),
(7, '1978-02-12'),
(8, '1934-04-05'),
(9, '1977-11-02');

insert into department (id, head_of_id, email, creation_date) values
(1, 5, 'ami@lnu.edu.ua', '1899-04-03'),
(2, 5, 'information-system@lnu.edu.ua', '1955-05-11'),
(3, 8, 'discrete-analysis@lnu.edu.ua', '1986-11-03'),
(4, 6, 'computational-mathematics@lnu.edu.ua', '1997-06-01');

insert into division (id, room_number) values
(2, '145'),
(3, '119a'),
(4, '245');

insert into faculty (id, address) values
(1, 'Universytetska, 1');

set foreign_key_checks = 1;
