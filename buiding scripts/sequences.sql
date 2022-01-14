create sequence sidInsert
increment by 1
minvalue 1001
nocache;

create or replace trigger studInsert
before insert on students for each row
begin
    :new.stud_id:=sidInsert.nextval;
end;
/

create or replace trigger studPass
before insert on students for each row
begin
    if :new.pass = 'student' then
        :new.pass:= concat('student' , substr(:new.CNP, -3));
    end if;
end;
/


create sequence pidInsert
increment by 1
minvalue 1
maxvalue 1000
nocache;

create or replace trigger profInsert
before insert on professors for each row
begin
    :new.prof_id:=pidInsert.nextval;
end;
/


create sequence depIdInsert
increment by 1
minvalue 1
maxvalue 99999
nocache;

create or replace trigger depInsert
before insert on departments for each row
begin
    :new.dept_id:=depIdInsert.nextval;
end;
/


create sequence courseIdInsert
increment by 1
minvalue 1
maxvalue 99999
nocache;

create or replace trigger courseInsert
before insert on courses for each row
begin
    :new.course_id:=courseIdInsert.nextval;
end;
/