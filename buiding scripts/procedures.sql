create or replace package procedures_pck
as
    procedure addStudent(stud_id in number,
                                       cnp in varchar2,
                                       f_name in varchar2,
                                       l_name in varchar2,
                                       bd in varchar2,
                                       phone in varchar2,
                                       email in varchar2,
                                       pass in varchar2,
                                       addr in varchar2,
                                       gender in varchar2,
                                       enrolment in varchar2,
                                       study_y in number,
                                       dept_id in number
                                       );
                                       
    procedure addProfessor(prof_id in number,
                                         CNP in varchar2,
                                         f_name in varchar2,
                                         l_name in varchar2,
                                         birth_date in varchar2,
                                         phone in char,
                                         email in char,
                                         pass in char,
                                         gender in char,
                                         dept_id in number
                                         );
                                         
    procedure addDepartment(dept_id in number, dept_name in varchar2);
    
    procedure addStudentRec (stud_id in number, course_id in number, 
                             f_grade in number, passed in varchar2);
    
    procedure addCourse(course_id in number,
                                      course_name in varchar2,
                                      credit_pts in number,
                                      units in number
                                      );
    procedure addGivenCourse(course_id in number, professor_id in number);
    procedure loginUser(user_id in number);
    
    procedure logoutUser(user_id in number);
    
    procedure removeGivenCourse(course_id in number, professor_id in number);
    
    procedure removeCourse(c_id in number);
    
    procedure removeDepartment(d_id in number);
    
    procedure removeProfessor(p_id in number);
    
    procedure removeStudent(s_id in number);
    
    procedure removeStudRecord(s_id in number, c_id in number);
        
    procedure showCourses(sys_ref out sys_refcursor);
    procedure showDepts(sys_ref out sys_refcursor);
    procedure getAllInfoStudent(s_id in number, sys_ref out sys_refcursor);
    procedure getAllInfoProf(p_id in number, sys_ref out sys_refcursor);
    procedure showProfessors(sys_ref out sys_refcursor);
    procedure showProfCourses(sys_ref out sys_refcursor);
    procedure getCourseData(c_id in number, sys_out out sys_refcursor);
    procedure showStudents(modet in varchar2, sys_ref out sys_refcursor);
    procedure studyYears(sys_ref out sys_refcursor);
    procedure showStudCourses(stud_id in number, sys_ref out sys_refcursor);
    procedure updateCourseStud(studid in number, courseid in number, grade in number);
    
end procedures_pck;
/

create or replace package body procedures_pck
as
------ add ------
    procedure addStudent(stud_id in number,
                                       cnp in varchar2,
                                       f_name in varchar2,
                                       l_name in varchar2,
                                       bd in varchar2,
                                       phone in varchar2,
                                       email in varchar2,
                                       pass in varchar2,
                                       addr in varchar2,
                                       gender in varchar2,
                                       enrolment in varchar2,
                                       study_y in number,
                                       dept_id in number
                                       )
    is
    begin
        insert into students values(stud_id, cnp, f_name, l_name, to_date(bd,'dd-mm-yyyy'), phone, email, pass, addr, gender, to_date(enrolment,'dd-mm-yyyy'), study_y, dept_id);
    end;

    procedure addProfessor(prof_id in number,
                                         CNP in varchar2,
                                         f_name in varchar2,
                                         l_name in varchar2,
                                         birth_date in varchar2,
                                         phone in char,
                                         email in char,
                                         pass in char,
                                         gender in char,
                                         dept_id in number
                                         )
    is
    begin
        insert into professors values(prof_id,CNP,f_name,l_name,to_date(birth_date, 'dd-MM-yyyy'),phone,email,pass,gender,dept_id);
    end;

    procedure addDepartment(dept_id in number, dept_name in varchar2)
    is
    begin
        insert into departments values(dept_id, dept_name);
    end;

    procedure addStudentRec (stud_id in number, course_id in number, f_grade in number, passed in varchar2)
    is
    begin
        insert into  student_records values(stud_id, course_id, f_grade, passed);
    end;
    
    
    procedure addCourse(course_id in number,
                                          course_name in varchar2,
                                          credit_pts in number,
                                          units in number
                                          )
    is
    begin
        insert into courses values(course_id, course_name, credit_pts, units);
    end;
    
    procedure addGivenCourse(course_id in number, professor_id in number)
    is
    begin
        insert into given_courses values(course_id, professor_id);
    end;
    
    procedure loginUser(user_id in number)
    is
    begin
        insert into logedin values(user_id);
    end;
    
    procedure logoutUser(user_id in number)
    is
    begin
        delete from logedin where user_id=user_id;
    end;
    
    
    ------ remove -----
    
    procedure removeGivenCourse(course_id in number, professor_id in number)
    is 
    begin
        delete from given_courses g
        where g.course_id = course_id and g.prof_id = professor_id;
    end;
    
    procedure removeCourse(c_id in number)
    is
    begin
        delete from courses
        where course_id = c_id;
    end;
    
    procedure removeDepartment(d_id in number)
    is
    begin
        delete from departments
        where dept_id = d_id;
    end;
    
    procedure removeProfessor(p_id in number)
    is
    begin
        delete from professors
        where prof_id = p_id;
    end;
    
    procedure removeStudent(s_id in number)
    is
    begin
        delete from students
        where stud_id = s_id;
    end;
    
    
    procedure removeStudRecord(s_id in number, c_id in number)
    is
    begin
        delete from student_records
        where stud_id = s_id and course_id = c_id;
    end;

    procedure showCourses(sys_ref out sys_refcursor)
    is
    begin
        open sys_ref  for select * from courses;
    end;
    
    procedure showDepts(sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for 
        select * 
        from departments
        order by dept_id;
    end;

    procedure getAllInfoStudent(s_id in number, sys_ref out sys_refcursor)
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
            where stud_id = s_id;  
    end;
    
    procedure getAllInfoProf(p_id in number, sys_ref out sys_refcursor)
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
            where p_id = prof_id;
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
            order by dept_id,prof_id;
    end;
    
    procedure showProfCourses(sys_ref out sys_refcursor)
    is
    begin
        open sys_ref for
            select *
            from  given_courses;
    end;
    
    
    procedure getCourseData(c_id in number, sys_out out sys_refcursor)
    as
    begin
        open sys_out for
            select c.course_id, c.course_name, c.credit_pts, c.units, p.full_name, p.prof_id
            from courses c
            full join (select a.prof_id, a.f_name ||' '|| a.l_name as full_name, b.course_id
                from professors a inner join given_courses b on b.prof_id = a.prof_id) p on c.course_id = p.course_id
            where c.course_id = c_id;
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
    
    procedure showStudCourses(stud_id in number, sys_ref out sys_refcursor)
    as
    begin
        open sys_ref for
            select c.course_id, c.course_name, r.f_grade, r.passed
            from courses c inner join student_records r on c.course_id = r.course_id
            where r.stud_id = stud_id;
       

    end;
    
     
     
    procedure updateCourseStud(studid in number, courseid in number, grade in number)
    as
        do_pass varchar2(5);
    begin
        if grade >= 5 then do_pass := 'yes';
        else do_pass := 'no';
        end if;
        
        update student_records 
        set f_grade = grade,
            passed = do_pass
        where stud_id = studid and course_id = courseid;
    end;
    
end procedures_pck;
/