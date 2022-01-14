create sequence sidInsert
increment by 1
start with 1001
minvalue 1001
nocache;

create or replace trigger studInsert
before insert on students for each row
begin
    :new.stud_id:=sidInsert.nextval;
end;