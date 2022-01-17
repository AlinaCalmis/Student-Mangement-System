create or replace package functions_pck
as
    ----------- Checks whether a student exists or not---------
    function isUserRegistered(userId in number) return boolean;
    ----------- Check credentials -----------------------------
    function checkPasswd(userId in number, passwd in varchar2) return boolean;
    ----------- Check user type(user is logged in)-------------
    function userType(uid in number) return varchar2;
    ----------- Get Student Personal DATA------------
    function getStudentData(studId in number, fullN out varchar2, phone out varchar2, 
                         email out varchar2, addr out varchar2, sex out varchar2, y out number) return varchar2;
    ----------- Get Proessors Data ------------------
    function getProfData(profid in number, fullN out varchar2, phone out varchar2, 
                         email out varchar2) return varchar2;
end functions_pck;
/

create or replace package body functions_pck
as
    
    function isUserRegistered(userId in number) return boolean
    as 
        cursor usersC is
            select stud_id from students
            union
            select prof_id from professors;
        cursor adminC is
        select user_id from admins;
    begin
    
        for ad in adminC
        loop
            if ad.user_id = userId then
                return true;
            end if;
        end loop;
        
        for us in usersC
        loop
            if us.stud_id = userId then
                return true;
            end if;
        end loop;
        
        
        exception 
            when no_data_found then
                return false;
    end;
    
    function checkPasswd(userId in number, passwd in varchar2) return boolean
    as
        cursor passwords is
        select stud_id, pass from students
        union
        select prof_id, pass from professors;
        
        cursor adminsC is
        select * from admins;
        
        nothing_detected exception;
    begin
        for us in passwords
        loop
            if us.stud_id = userID and us.pass = passwd then
                return true;
            end if;
        end loop;
        
        for ad in adminsC
        loop
            if ad.user_id = userId and ad.pass = passwd then
                return true;
            end if;
        end loop;
        
        raise nothing_detected;
        
        exception 
            when nothing_detected then
                return false;
                
--        return false;
    end;
    
    function userType(uid in number) return varchar2
    as
    begin
        if uid > 1000 then
            return 'student';
        elsif uid = 0 then
                return 'admin';
        else 
            return 'professor';
        end if;
    end;

    function getStudentData(studId in number, fullN out varchar2, phone out varchar2, 
                         email out varchar2, addr out varchar2, sex out varchar2, y out number) return varchar2
    as 
        deptN departments.dept_name%type;
    begin
        select f_name||' '||l_name, phone, email, address, gender, study_year, d.dept_name
        into fullN, phone, email, addr, sex, y, deptN
        from students s join departments d on s.dept_id = d.dept_id
        where studId = stud_id;
        
        return deptN;
        
        exception
        when no_data_found then
            raise_application_error(-20001, 'STUDENT_NOT_FOUND');
    end;
    
    function getProfData(profid in number, fullN out varchar2, phone out varchar2, 
                         email out varchar2) return varchar2
    as 
        deptN departments.dept_name%type;
    begin
        select f_name||' '||l_name, phone, email, d.dept_name
        into fullN, phone, email, deptN
        from professors p join departments d on p.dept_id = d.dept_id
        where profid = prof_id;
        
        return deptN;
        
        exception
        when no_data_found then
            raise_application_error(-20002, 'PROFESSOR_NOT_FOUND');
    end;
    
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