create or replace package functions_pck
as
    ----------- Get Student Personal DATA------------
    type pers_stud_data_rec is record(
            f_name varchar2(50),
            l_name varchar2(50),
            study_year number(1),
            birth_date DATE,
            phone varchar2(12),
            email varchar2(50),
            dept_name varchar2(50));

    type pers_stud_data is varray(1) of pers_stud_data_rec;
--/
    function getStudentPersonalData(st_id in number) return pers_stud_data;
    
    type prof_data_rec is record(
        f_name varchar2(50),
        l_name varchar2(50),
        birth_date DATE,
        phone varchar2(12),
        email varchar2(50),
        dept_name varchar2(50));
        
    type prof_data is varray(1) of prof_data_rec;
    
    function getProfessorData(p_id in number) return prof_data;
end functions_pck;
/

create or replace package body functions_pck
as
    function getStudentPersonalData(st_id in number) return pers_stud_data
    as 
        stud pers_stud_data:= pers_stud_data();
        
        f varchar2(50);
        l varchar2(50);
        sy number(1);
        bd DATE;
        ph varchar2(12);
        e varchar2(50);
        dn varchar2(50);
    begin
        
        select f_name,l_name,study_year, birth_date, phone, email, d.dept_name
        into f,l,sy,bd,ph,e,dn
        from students s join departments d on d.dept_id = s.dept_id
        where stud_id = st_id;
        
        stud.extend;
        stud(1) :=  pers_stud_data_rec(null,null,null,null,null,null,null);
        stud(1).f_name :=f;
        stud(1).l_name :=l;
        stud(1).study_year := sy;
        stud(1).birth_date :=bd;
        stud(1).phone :=ph;
        stud(1).email :=e;
        stud(1).dept_name :=dn;
        
        return stud;
        
    exception
        when no_data_found then
            raise_application_error(-20001, 'STUDENT_NOT_FOUND');
        
    end getStudentPersonalData;
    
    
    ------------- GET PROF PERSONAL DATA -------------------
    --drop TYPE prof_data;
    
--    create or replace type prof_data_rec as object(
--        f_name varchar2(50),
--        l_name varchar2(50),
--        birth_date DATE,
--        phone varchar2(12),
--        email varchar2(50),
--        dept_name varchar2(50));
--    /
--    create or replace type prof_data as varray(1) of prof_data_rec;
--    /
    
    function getProfessorData(p_id in number) return prof_data
    as 
        prof prof_data:= prof_data();
        
        f varchar2(50);
        l varchar2(50);
        bd DATE;
        ph varchar2(12);
        e varchar2(50);
        dn varchar2(50);
    begin
        
        select f_name,l_name, birth_date, phone, email, d.dept_name
        into f,l,bd,ph,e,dn
        from professors p join departments d on d.dept_id = p.dept_id
        where prof_id = p_id;
        
        prof.extend;
        prof(1) :=  prof_data_rec(null,null,null,null,null,null);
        prof(1).f_name :=f;
        prof(1).l_name :=l;
        prof(1).birth_date :=bd;
        prof(1).phone :=ph;
        prof(1).email :=e;
        prof(1).dept_name :=dn;
        
        return prof;
        
    exception
        when no_data_found then
            raise_application_error(-20002, 'PROFESSOR_NOT_FOUND');
        
    end getProfessorData;
    
end functions_pck;
/


--SET SERVEROUTPUT ON;
--declare
--    S pers_stud_data:= functions_pck.pers_stud_data();
----    P prof_data:= prof_data();
--begin
--    
--    S.extend;
--    S(1) :=  functions_pck.pers_stud_data_rec(null,null,null,null,null,null,null);
--    dbms_output.put_line(S.count);
--    S:= functions_pck.getStudentPersonalData(1001);
----    
----    p.extend;
----    p(1) :=  prof_data_rec(null,null,null,null,null,null);
----    dbms_output.put_line(p.count);
----    p:= getProfessorData(1);
----    DBMS_OUTPUT.PUT_LINE(x(1));
--end;
--/