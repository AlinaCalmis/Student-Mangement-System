create or replace package procedures_pck
as
    procedure addStudent(p_stud_id in number,
                                       p_cnp in varchar2,
                                       p_f_name in varchar2,
                                       p_l_name in varchar2,
                                       p_bd in varchar2,
                                       p_phone in varchar2,
                                       p_email in varchar2,
                                       p_pass in varchar2,
                                       p_addr in varchar2,
                                       p_gender in varchar2,
                                       p_enrolment in varchar2,
                                       p_study_y in number,
                                       p_dept_id in number
                                       );
                                       
    procedure addProfessor(p_prof_id in number,
                                         p_CNP in varchar2,
                                         p_f_name in varchar2,
                                         p_l_name in varchar2,
                                         p_birth_date in varchar2,
                                         p_phone in char,
                                         p_email in char,
                                         p_pass in char,
                                         p_gender in char,
                                         p_dept_id in number
                                         );
                                         
    procedure addDepartment(p_dept_id in number, p_dept_name in varchar2);
    
    procedure addCourse(p_course_id in number,
                                          p_course_name in varchar2,
                                          p_credit_pts in number,
                                          p_units in number
                                          );
                                      
    procedure loginUser(p_user_id in number, p_user_type in varchar2, 
                        sys_ref out sys_refcursor);
    
    procedure logoutUser(p_user_id in number);
    
    procedure removeGivenCourse(p_course_id in number, 
                                p_prof_id in number);
    
    procedure removeCourse(p_course_id in number);
    
    procedure removeDepartment(p_dept_id in number);
    
    procedure removeProfessor(p_prof_id in number);
    
    procedure removeStudent(p_stud_id in number);
    
    procedure removeStudRecord(p_stud_id in number, p_course_id in number);
        
    procedure showCourses(sys_ref out sys_refcursor);
    
    procedure showDepts(sys_ref out sys_refcursor);
    
    procedure getAllInfoStudent(p_stud_id in number, sys_ref out sys_refcursor);
    
    procedure getAllInfoProf(p_prof_id in number, sys_ref out sys_refcursor);
    
    procedure showProfessors(sys_ref out sys_refcursor);
   
    procedure showProfCourses(p_prof_id in number,sys_ref out sys_refcursor);
    
    procedure getCourseData(p_course_id in number, sys_out out sys_refcursor);
    
    procedure showStudents(modet in varchar2, sys_ref out sys_refcursor);
    
    procedure studyYears(sys_ref out sys_refcursor);
    
    procedure showStudCourses(p_stud_id in number, sys_ref out sys_refcursor);
    
    procedure updateCourseStud(p_stud_id in number, p_course_id in number, 
                               p_grade in number);
    
end procedures_pck;
/

create or replace package body procedures_pck
as
------ add ------
    procedure addStudent(p_stud_id in number,
                                       p_cnp in varchar2,
                                       p_f_name in varchar2,
                                       p_l_name in varchar2,
                                       p_bd in varchar2,
                                       p_phone in varchar2,
                                       p_email in varchar2,
                                       p_pass in varchar2,
                                       p_addr in varchar2,
                                       p_gender in varchar2,
                                       p_enrolment in varchar2,
                                       p_study_y in number,
                                       p_dept_id in number
                                       )
    is
    begin
        insert into students values(p_stud_id, p_cnp, p_f_name, p_l_name, 
                                    to_date(p_bd,'dd-mm-yyyy'), p_phone, 
                                    p_email, p_pass, p_addr, p_gender, 
                                    to_date(p_enrolment,'dd-mm-yyyy'), 
                                    p_study_y, p_dept_id);
    end;

    procedure addProfessor(p_prof_id in number,
                                         p_CNP in varchar2,
                                         p_f_name in varchar2,
                                         p_l_name in varchar2,
                                         p_birth_date in varchar2,
                                         p_phone in char,
                                         p_email in char,
                                         p_pass in char,
                                         p_gender in char,
                                         p_dept_id in number
                                         )
    is
    begin
        insert into professors values(p_prof_id, p_CNP, p_f_name, p_l_name,
                                      to_date(p_birth_date, 'dd-MM-yyyy'),
                                      p_phone, p_email, p_pass, p_gender, 
                                      p_dept_id);
    end;

    procedure addDepartment(p_dept_id in number, p_dept_name in varchar2)
    is
    begin
        insert into departments values(p_dept_id, p_dept_name);
    end;

    procedure addStudentRec (p_stud_id in number, p_course_id in number, 
                             p_f_grade in number, p_passed in varchar2)
    is
    begin
        insert into student_records values(p_stud_id, p_course_id, p_f_grade, 
                                           p_passed);
    end;
    
    
    procedure addCourse(p_course_id in number,
                                          p_course_name in varchar2,
                                          p_credit_pts in number,
                                          p_units in number
                                          )
    is
    begin
        insert into courses values(p_course_id, p_course_name, p_credit_pts, 
                                   p_units);
    end;

    procedure loginUser(p_user_id in number, p_user_type in varchar2, 
                        sys_ref out sys_refcursor)
    is
    begin
        insert into loggedin values(p_user_id);
        
        if p_user_type = 'professor' then
            open sys_ref for
                select * from professors
                where prof_id = p_user_id;
        elsif p_user_type = 'student' then
            open sys_ref for
                select * from students
                where stud_id = p_user_id;
        else 
            open sys_ref for 
            select * from admins s
            where s.user_id = p_user_id;
        end if;
    end;
    
    procedure logoutUser(p_user_id in number)
    is
    begin
        delete from loggedin where user_id = p_user_id;
    end;
    
    
    ------ remove -----
    
    procedure removeGivenCourse(p_course_id in number, p_prof_id in number)
    is 
    begin
        delete from given_courses
        where course_id = p_course_id and prof_id = p_prof_id;
    end;
    
    procedure removeCourse(p_course_id in number)
    is
    begin
        delete from courses
        where course_id = p_course_id;
    end;
    
    procedure removeDepartment(p_dept_id in number)
    is
    begin
        delete from departments
        where dept_id = p_dept_id;
    end;
    
    procedure removeProfessor(p_prof_id in number)
    is
    begin
        delete from given_courses
        where prof_id = p_prof_id;
        
        delete from professors
        where prof_id = p_prof_id;
    end;
    
    procedure removeStudent(p_stud_id in number)
    is
    begin
        delete from student_records
        where stud_id = p_stud_id;
        
        delete from students
        where stud_id = p_stud_id;
    end;
    
    
    procedure removeStudRecord(p_stud_id in number, p_course_id in number)
    is
    begin
        delete from student_records
        where stud_id = p_stud_id and course_id = p_course_id;
    end;

    procedure showCourses(sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for select * from courses;
    end;
    
    procedure showDepts(sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for 
        select * 
        from departments
        order by dept_id;
    end;

    procedure getAllInfoStudent(p_stud_id in number, sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for
             select S.STUD_ID ,
                    S.CNP ,
                    S.F_NAME ||' ' ||
                    S.L_NAME ,
                    to_char(S.BIRTH_DATE) ,
                    S.PHONE ,
                    S.EMAIL ,
                    S.PASS ,
                    S.ADDRESS ,
                    S.GENDER ,
                    to_char(S.ENROLMENT),
                    S.STUDY_YEAR ,
                    D.DEPT_NAME  
            from students s join departments d on s.dept_id = d.dept_id
            where stud_id = p_stud_id;  
    end;
    
    procedure getAllInfoProf(p_prof_id in number, sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for
            select  PROF_ID ,
                    CNP ,
                    F_NAME || ' ' ||
                    L_NAME ,
                    to_char(BIRTH_DATE) ,
                    PHONE ,
                    EMAIL ,
                    PASS ,
                    GENDER ,
                    DEPT_ID  
            from professors
            where prof_id = p_prof_id;
    end;
    
    procedure showProfessors(sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for
            select  PROF_ID ,
                    CNP ,
                    F_NAME || ' ' ||
                    L_NAME ,
                    EMAIL ,
                    DEPT_ID  
            from professors 
            order by dept_id, prof_id;
    end;
    
    procedure showProfCourses(p_prof_id in number, sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for
            select g.course_id, c.course_name
            from  given_courses g 
            inner join courses c 
            on g.course_id=c.course_id
            where g.prof_id = p_prof_id;
    end;
    
    
    procedure getCourseData(p_course_id in number, sys_out out sys_refcursor)
    as
    begin
        open sys_out for
            select c.course_id, 
                   c.course_name, 
                   c.credit_pts, 
                   c.units, 
                   p.full_name, 
                   p.prof_id
            from courses c
            full join (
                        select a.prof_id, a.f_name||' '||a.l_name as full_name, 
                               b.course_id
                        from professors a 
                        inner join given_courses b 
                        on b.prof_id = a.prof_id
                        ) p on c.course_id = p.course_id
            where c.course_id = p_course_id;
    end;
    
    procedure showStudents(modet in varchar2, sys_ref out sys_refcursor)
    as
        orderby integer := 1;
    begin
    
        if modet='dept' then orderby:= 11;
            elsif modet='year' then orderby:= 10;
            elsif modet='gender' then orderby:= 8;
        end if;
    
        open sys_ref for
                select  S.STUD_ID ,
                        S.CNP ,
                        S.F_NAME ||' ' ||S.L_NAME ,
                        to_char(S.BIRTH_DATE) ,
                        S.PHONE ,
                        S.EMAIL ,
                        S.PASS ,
                        S.ADDRESS ,
                        S.GENDER ,
                        to_char(S.ENROLMENT) ,
                        S.STUDY_YEAR ,
                        S.DEPT_ID ,
                        D.DEPT_NAME
                from students s join departments d on d.dept_id = s.dept_id
                order by orderby;

    end;
    
    procedure studyYears(sys_ref out sys_refcursor)
    as
    begin
        open sys_ref for
            select distinct(study_year) from students
            order by 1;
    end;
    
    procedure showStudCourses(p_stud_id in number, sys_ref out sys_refcursor)
    as
    begin
        open sys_ref for
            select c.course_id, c.course_name, r.f_grade, r.passed, r.stud_id
            from courses c 
            inner join student_records r 
            on c.course_id = r.course_id
            where r.stud_id = p_stud_id;
       

    end;
    
     
     
    procedure updateCourseStud(p_stud_id in number, p_course_id in number, 
                               p_grade in number)
    as
        do_pass varchar2(5);
    begin
        if p_grade >= 5 then do_pass := 'yes';
        else do_pass := 'no';
        end if;
        
        update student_records 
        set f_grade = p_grade,
            passed = do_pass
        where stud_id = p_stud_id and course_id = p_course_id;
    end;
    
end procedures_pck;
/