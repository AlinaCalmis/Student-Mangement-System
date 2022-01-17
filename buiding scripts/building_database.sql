drop table logedin;
drop table student_records;
drop table given_courses;
drop table courses;
drop table students;
drop table professors;
drop table departments;
drop table admins;

create table students(
    stud_id number(10) constraint stud_id_nn not null,
    CNP varchar2(13) constraint scnp_uq unique,
    f_name varchar2(50) constraint fn_nn not null,
    l_name varchar2(50) constraint ln_nn not null,
    birth_date DATE constraint bd_nn not null,
    phone varchar2(12),
    email varchar2(50),
    pass varchar2(10) constraint pass_nn not null,
    address varchar2(100) constraint add_nn not null,
    gender varchar2(7) constraint gn_nn not null,
    enrolment date constraint enr_nn not null,
    study_year number(1) default 1,
    dept_id number(4),
    constraint st_id_pk primary key(stud_id)
);

create table professors(
    prof_id number(10) constraint prof_id_nn not null,
    CNP varchar2(13) constraint pcnp_uq unique,
    f_name varchar2(50) constraint p_fn_nn not null,
    l_name varchar2(50) constraint p_ln_nn not null,
    birth_date DATE constraint p_bd_nn not null,
    phone varchar2(12),
    email varchar2(50),
    pass varchar2(10) constraint ppass_nn not null,
    gender varchar2(7) constraint p_gn_nn not null,
    dept_id number(4),
    constraint p_id_pk primary key(prof_id)
);

create table departments(
    dept_id number(5) constraint dept_id_nn not null,
    dept_name varchar2(50) constraint d_name_nn not null,
    constraint d_id_pk primary key(dept_id)
);

alter table students add(
    constraint d_id_fk foreign key(dept_id) references departments(dept_id)
);

alter table professors add(
    constraint p_d_id_fk foreign key(dept_id) references departments(dept_id)
);

create table courses(
    course_id number(5) constraint c_id_nn not null,
    course_name varchar2(50) constraint cn_nn not null,
    credit_pts number(2) default 1,
    units number(3) default 1,
    constraint c_id primary key(course_id)
);

create table given_courses(
    course_id number(5) constraint gc_id_nn not null,
    prof_id number(5) constraint gp_id_nn not null
);

alter table given_courses add(
    constraint gc_id_fk foreign key(course_id) references courses(course_id),
    constraint gp_id_fk foreign key(prof_id) references professors(prof_id)
);

create table student_records(
    stud_id number(10) constraint recs_id_nn not null,
    course_id number(5) constraint recc_id_nn not null,
    f_grade number(2),
    passed varchar2(3)
);

alter table student_records add(
    constraint recs_id_fk foreign key(stud_id) references students(stud_id),
    constraint recc_id_fk foreign key(course_id) references courses(course_id)
);

create table logedin(
    user_id number(10),
    constraint li_pk primary key(user_id)
);

create table admins(
    user_id number(10),
    pass varchar2(10),
    constraint u_pk primary key(user_id)
);

--create sequence sidInsert
--increment by 1
--start with 1000;
--
--create or replace trigger studInsert
--before insert on students for each row
--begin
--    :new.stud_id:=sidInsert.nextval;
--end;
--/

--insert into given_courses values();

select * from departments;
select * from students;
select * from professors;
select * from courses;
--drop table student_records;
--drop table given_courses;
--drop table courses;
--drop table students;
--drop table professors;
--drop table departments;
