drop table student_records;
drop table given_courses;
drop table courses;
drop table students;
drop table professors;
drop table departments;

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

insert into departments values(0,'Automatica');
insert into departments values(1,'Calculatoare');


insert into students values(1001, '2990528987667', 'Alina', 'Calmis', to_date('28-05-1999', 'dd-MM-yyyy'), '+40765445098', 'alina.calmis@stud.acs.upb.ro','student','Rep. Moldova, Chisinau, Stefan cel Mare 28/3, ap44', 'female', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1002, '2990528987667', 'Ana', 'Binzegger', to_date('16-10-1999', 'dd-MM-yyyy'), '+4074322443', 'ana.binzegger@gmail.com','student','Rep. Moldova, Straseni, Mihai Eminescu 53', 'female', to_date('25-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1003, '1981210000000', 'Ion', 'Popescu', to_date('01-12-1998', 'dd-MM-yyyy'), '+4071111111', 'popescui@yahoo.com','student','Romania, Constanta, Piata Brasov 3, ap2', 'male', to_date('22-07-2019', 'dd-MM-yyyy'), 3, 1); 
insert into students values(1004, '1000413000001', 'Cristian', 'Donici', to_date('13-04-2000', 'dd-MM-yyyy'), '+4071123111', 'cristi.x.don@gmail.com','student','Romania, Brasov,Emil Racovita 32, et4, ap44', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 2, 1); 
insert into students values(1005, '1990625000010', 'Robert', 'Ionut', to_date('25-06-1999', 'dd-MM-yyyy'), '+4079546575', 'ionut2000@gmail.com','student','Romania, Piatra Neamt, Basarab 34, c9, ap44', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1006, '2991128000009', 'Maria', 'Camilescu', to_date('28-11-1999', 'dd-MM-yyyy'), '+4075463837', 'mariuta99@gmail.com','student','Romania, Bucuresti, Baba Novac 93, a45, ap44', 'female', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1007, '1990417111118', 'Nicolae', 'Andronache', to_date('17-04-1999', 'dd-MM-yyyy'), '+4078888655', 'nico.andro@gmail.com','student','Romania, Cluj Napoca, Furtunei 28/3, ap44', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1008, '1990505111117', 'Stanislav', 'Panus', to_date('05-05-1999', 'dd-MM-yyyy'), '+4074555562', 'panusstas@gmail.com','student','Romania, Slobozia, Fagului 2, ap109', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1009, '1991231111116', 'Andy', 'Blanaru', to_date('31-12-1999', 'dd-MM-yyyy'), '+4071111123', 'blanaru.andy.0@gmail.com','student','Romania, Iasi, Onisifor Ghibu 77', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1010, '1991102000008', 'Vlad', 'Cristian', to_date('02-11-1999', 'dd-MM-yyyy'), '+4068989898', 'vladcris@gmail.com','student','Romania, Bucuresti, Nicolae Titulescu 102, ap33', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1011, '1980323000007', 'Bobi', 'Ivanov', to_date('23-03-1998', 'dd-MM-yyyy'), '+4079000090', 'ivanonb@gmail.com','student','Ucraina, Lvov, Stepan Velikii 34', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1012, '2991018111116', 'Rusalda', 'Savu', to_date('18-10-1999', 'dd-MM-yyyy'), '+4071111112', 'savurusi@gmail.com','student','Romania, Botosani, Nordului 76, ap 32', 'female', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1013, '2990106111115', 'Irina', 'Cotici', to_date('06-01-1999', 'dd-MM-yyyy'), '+4070202021', 'irina.cotici1@gmail.com','student','Romania, Alba Iulia, Bd. Natiunilor Unite 142, a5, ap6', 'female', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1014, '1990814000006', 'Corneliu', 'Calancea', to_date('14-08-1999', 'dd-MM-yyyy'), '+4079565985', 'cornelut99@gmail.com','student','Romania, Iasi, Eugen Bronte 56, i8, ap56', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1015, '2990707000005', 'Antonela', 'Ciudin', to_date('07-07-1999', 'dd-MM-yyyy'), '+4076490909', 'antonia.ciudin00@gmail.com','student','Rep. Moldova, Calarasi, Soarelui 56', 'female', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1016, '1991207111114', 'Gheorghe', 'Condorache', to_date('07-12-1999', 'dd-MM-yyyy'), '+4078298323', 'georgech@yahoo.com','student','Rep. Moldova, Chisinau, Stefan cel Mare 28/3, ap44', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 1, 1); 
insert into students values(1017, '1980631111113', 'Sergiu', 'Babin', to_date('05-06-1998', 'dd-MM-yyyy'), '+4079546754', 'babinserg@gmail.com','student','Romania, Conctanta, Piata Vinerea Mare 6, ap9', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1018, '1980531000004', 'Ghenadie', 'Caraman', to_date('31-05-1998', 'dd-MM-yyyy'), '+4079543333', 'ghenacar@gmail.com','student','Rep. Moldova, Chisinau, Barbu Stefanescu 4, ap109', 'male', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1019, '2990312000003', 'Andreea', 'Laurentiu', to_date('12-03-1999', 'dd-MM-yyyy'), '+4079514000', 'andylaur1@gmail.com','student','Romania, Bucuresti, Piata Iancu 109', 'female', to_date('24-07-2018', 'dd-MM-yyyy'), 4, 1); 
insert into students values(1020, '1010801111112', 'Marian', 'Cristescu', to_date('01-08-2001', 'dd-MM-yyyy'), '+40756565656', 'cristescu.marian@gmail.com','student','Romania, Bucuresti, Piata Alba Iulia 3, ap65', 'male', to_date('28-07-2020', 'dd-MM-yyyy'), 2, 1); 

insert into professors values(0, '2840321786609', 'Irina', 'Mocanu', to_date('21-03-1984', 'dd-MM-yyyy'), '+40746338906', 'irina.mocanu@cs.pub.ro', 'professor', 'female', 1);
insert into professors values(1, '1741011000291', 'Alin Dragos Bogdan', 'Moldoveanu', to_date('11-10-1974', 'dd-MM-yyyy'), '+40709283372', 'alin.moldoveanu@cs.pub.ro', 'professor', 'male', 1);
insert into professors values(2, '1720809211541', 'Ciprian Octavian', 'Truica', to_date('09-08-1972', 'dd-MM-yyyy'), '+4076534221', 'ciprian.truica@cs.pub.ro', 'professor', 'male', 1);
insert into professors values(3, '1851001562649', 'Mihai', 'Carabas', to_date('01-10-1985', 'dd-MM-yyyy'), '+40746626182', 'imihai.carabas@cs.pub.ro', 'professor', 'male', 1);
insert into professors values(4, '1841212546836', 'Traian', 'Rebedea', to_date('12-12-1984', 'dd-MM-yyyy'), '+40764736281', 'traian.rebedea@cs.pub.ro', 'professor', 'male', 1);
insert into professors values(5, '1820609448594', 'Matei', 'Popovici', to_date('09-06-1982', 'dd-MM-yyyy'), '+40715415653', 'matei.popovici@cs.pub.ro', 'professor', 'male', 1);
insert into professors values(6, '1610111265478', 'Cornel', 'Popescu', to_date('11-01-1961', 'dd-MM-yyyy'), '+40756264552', 'cornel.pop@cs.pub.ro', 'professor', 'male', 1);
insert into professors values(7, '1750111546878', 'Marios', 'Choudary', to_date('14-11-1975', 'dd-MM-yyyy'), '+40746338322', 'marioschoudary@cs.pub.ro', 'professor', 'male', 1);

insert into courses values(0, 'Sisteme de Operare', 5, 15);
insert into courses values(1, 'Inteligenta Artificiala', 6, 12);
insert into courses values(2, 'Procesarea Semnalelor', 6, 20);
insert into courses values(3, 'Ingineria Programelor', 4, 12);
insert into courses values(4, 'Introducere in Criptologie', 6, 16);
insert into courses values(5, 'Baze de Date', 5, 12);
insert into courses values(6, 'Limbaje Formale si Automate', 5, 14);
insert into courses values(7, 'Proiectarea Algoritmilor', 5, 15);
insert into courses values(8, 'Sisteme cu Microprocesoare', 4, 10);
insert into courses values(9, 'Sisteme de Operare 2', 5, 15);
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
