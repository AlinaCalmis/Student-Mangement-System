

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
                         
    function doCountProfInDept(d_id in number, sys_ref out sys_refcursor)
                                return integer;
    function doCountStudentsInDept(d_id in number)return integer;
    
    function checkDept(d_id in number, d_name in varchar2) return boolean;
    
    function studGender(sys_ref out sys_refcursor) return integer;

    function countMen(modet in varchar2) return integer;
    
    function addCourseStud(stud_id in number, course_id in number) return boolean;
    

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
    
    function doCountStudentsInDept(d_id in number)
    return integer
    as 
        nstud integer default 0;
    begin
        select count(stud_id)
        into nstud
        from students s 
        where s.dept_id = d_id;
            
        return nstud;
    end;
    
    function doCountProfInDept(d_id in number, sys_ref out sys_refcursor)
    return integer
    as 
        nprof integer default 0;
    begin
        select count(prof_id)
        into nprof
        from professors p 
        where p.dept_id = d_id;
        
        open sys_ref for
            select * from departments
            where dept_id = d_id;
        
        return nprof;
    end;
    
    function checkDept(d_id in number, d_name in varchar2) return boolean
    as
        checked boolean;
        
        cursor dept is select * from departments;
        
        nothing_detected exception;
    begin
        for d in dept
        loop
            if d.dept_id = d_id then
                return true;
            elsif d.dept_name = d_name then
                return true;
            end if;
        end loop;
        
        raise nothing_detected;
        
        exception 
            when nothing_detected then
                return false;
    end;

    function studGender(sys_ref out sys_refcursor) return integer
    as 
        female integer;
    begin
        
        select count(stud_id)
        into female
        from students
        where gender = 'female';
    
        open sys_ref for 
            select distinct(gender)
            from students;
            
        return female;
    end;
    
    function countMen(modet in varchar2) return integer
    as
    men integer:=0;
    begin
        if modet = 'stud' then
            select count(stud_id)
            into men
            from students
            where gender='male';
        elsif modet = 'prof' then
            select count(prof_id)
            into men
            from professors
            where gender='male';
        end if;
        return men;
    end;
    
    function addCourseStud(stud_id in number, course_id in number)
    return boolean
     as
        cursor courses_c is
            select r.stud_id, r.course_id
            from student_records r;
        exist boolean := false;
     begin
        for c in courses_c
        loop
            if c.stud_id = stud_id and c.course_id = course_id then
                exist := true;
                return false;
            end if;
        end loop;
        
        insert into student_records values(stud_id, course_id, 0, null);
        return true;
        
     end;
 
    
end functions_pck;
/

