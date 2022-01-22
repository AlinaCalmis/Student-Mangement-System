

create or replace package functions_pck
as

    ----------- Checks whether a student exists or not---------
    function isUserRegistered(p_user_id in number) return boolean;
    ----------- Check credentials -----------------------------
    function checkPasswd(p_user_id in number, p_pass in varchar2) 
                         return boolean;
    ----------- Check user type(user is logged in)-------------
    function userType(p_user_id in number) return varchar2;
    
    function doCountProfInDept(p_dept_id in number, sys_ref out sys_refcursor)
                                return integer;
    function doCountStudentsInDept(p_dept_id in number)return integer;
    
    function checkDept(p_dept_id in number, p_dept_name in varchar2) return boolean;
    
    function doCountFemale(sys_ref out sys_refcursor) return integer;

    function doCountMen(modet in varchar2) return integer;
    
    function addCourseStud(p_stud_id in number, p_course_id in number) 
                           return boolean;
    
    function addGivenCourse(p_course_id in number, p_prof_id in number)
    return boolean;

end functions_pck;
/

create or replace package body functions_pck
as
    
    function isUserRegistered(p_user_id in number) return boolean
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
            if ad.user_id = p_user_id then
                return true;
            end if;
        end loop;
        
        for us in usersC
        loop
            if us.stud_id = p_user_id then
                return true;
            end if;
        end loop;
        
        
        exception 
            when no_data_found then
                return false;
    end;
    
    function checkPasswd(p_user_id in number, p_pass in varchar2) return boolean
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
            if us.stud_id = p_user_id and us.pass = p_pass then
                return true;
            end if;
        end loop;
        
        for ad in adminsC
        loop
            if ad.user_id = p_user_id and ad.pass = p_pass then
                return true;
            end if;
        end loop;
        
        raise nothing_detected;
        
        exception 
            when nothing_detected then
                return false;
                
--        return false;
    end;
    
    function userType(p_user_id in number) return varchar2
    as
    begin
        if p_user_id > 1000 then
            return 'student';
        elsif p_user_id = 0 then
                return 'admin';
        else 
            return 'professor';
        end if;
    end;

    function getStudentData(p_stud_id in number, p_full out varchar2, 
                            p_phone out varchar2, p_email out varchar2, 
                            p_addr out varchar2, p_sex out varchar2, 
                            y out number) return varchar2
    as 
        deptN departments.dept_name%type;
    begin
        select f_name||' '||l_name, phone, email, address, gender, study_year, d.dept_name
        into p_full, p_phone, p_email, p_addr, p_sex, y, deptN
        from students s join departments d on s.dept_id = d.dept_id
        where stud_id = p_stud_id;
        
        return deptN;
        
        exception
        when no_data_found then
            raise_application_error(-20001, 'STUDENT_NOT_FOUND');
    end;
    
    function getProfData(p_prof_id in number, p_full out varchar2, 
                         p_phone out varchar2, p_email out varchar2) 
                         return varchar2
    as 
        deptN departments.dept_name%type;
    begin
        select f_name||' '||l_name, phone, email, d.dept_name
        into p_full, p_phone, p_email, deptN
        from professors p join departments d on p.dept_id = d.dept_id
        where prof_id = p_prof_id;
        
        return deptN;
        
        exception
        when no_data_found then
            raise_application_error(-20002, 'PROFESSOR_NOT_FOUND');
    end;
    
    function doCountStudentsInDept(p_dept_id in number)
    return integer
    as 
        nstud integer default 0;
    begin
        select count(stud_id)
        into nstud
        from students s 
        where s.dept_id = p_dept_id;
            
        return nstud;
    end;
    
    function doCountProfInDept(p_dept_id in number, sys_ref out sys_refcursor)
    return integer
    as 
        nprof integer default 0;
    begin
        select count(prof_id)
        into nprof
        from professors p 
        where p.dept_id = p_dept_id;
        
        open sys_ref for
            select * from departments
            where dept_id = p_dept_id;
        
        return nprof;
    end;
    
    function checkDept(p_dept_id in number, p_dept_name in varchar2) 
                       return boolean
    as
        checked boolean;
        
        cursor dept is select * from departments;
        
        nothing_detected exception;
    begin
        for d in dept
        loop
            if d.dept_id = p_dept_id then
                return true;
            elsif d.dept_name = p_dept_name then
                return true;
            end if;
        end loop;
        
        raise nothing_detected;
        
        exception 
            when nothing_detected then
                return false;
    end;

    function doCountFemale(sys_ref out sys_refcursor) return integer
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
    
    function doCountMen(modet in varchar2) return integer
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
    
    function addCourseStud(p_stud_id in number, p_course_id in number)
    return boolean
     as
        cursor courses_c is
            select r.stud_id, r.course_id
            from student_records r;
        exist boolean := false;
     begin
        for c in courses_c
        loop
            if c.stud_id = p_stud_id and c.course_id = p_course_id then
                exist := true;
                return false;
            end if;
        end loop;
        
        insert into student_records values(p_stud_id, p_course_id, 0, null);
        return true;
        
     end;
     
         
    function addGivenCourse(p_course_id in number, p_prof_id in number)
    return boolean
    is
        cursor courses_c is
            select course_id from given_courses where prof_id = p_prof_id;
        exist boolean;
    begin
        for c in courses_c
        loop
            if c.course_id = p_course_id then
                return False;
            end if;
        end loop;
        
        insert into given_courses values(p_course_id, p_prof_id);
        return True;
    end;
    
 
    
end functions_pck;
/

