------ add ------
create or replace procedure addStudent(stud_id in number,
                                       cnp in varchar2,
                                       f_name in varchar2,
                                       l_name in varchar2,
                                       bd in DATE,
                                       phone in varchar2,
                                       email in varchar2,
                                       pass in varchar2,
                                       addr in varchar2,
                                       gender in varchar2,
                                       enrolment in date,
                                       study_y in number,
                                       dept_id in number
                                       )
is
begin
    insert into students values(stud_id, cnp, f_name, l_name, bd, phone, email, pass, addr, gender, enrolment, study_y, dept_id);
end;

create or replace procedure addProfessor(prof_id in number,
                                         CNP in varchar2,
                                         f_name in varchar2,
                                         l_name in varchar2,
                                         birth_date in DATE,
                                         phone in char,
                                         email in char,
                                         pass in char,
                                         gender in char,
                                         dept_id in number
                                         )
is
begin
    insert into professors values(prof_id,CNP,f_name,l_name,birth_date,phone,email,pass,gender,dept_id);
end;

create or replace procedure addDepartment(dept_id in number, dept_name in varchar2)
is
begin
    insert into departments values(dept_id, dept_name);
end;

create or replace procedure addStudentRec (stud_id in number, course_id in number, f_grade in number, passed in varchar2)
is
begin
    insert into  student_records values(stud_id, course_id, f_grade, passed);
end;



create or replace procedure addCourse(course_id in number,
                                      course_name in varchar2,
                                      credit_pts in number,
                                      units in number
                                      )
is
begin
    insert into courses  values(course_id, course_name, credit_pts, units);
end;


------ remove -----
create or replace procedure removeCourse(c_id in number)
is
begin
    delete from courses
    where course_id = c_id;
end;

create or replace procedure removeDepartment(d_id in number)
is
begin
    delete from departments
    where dept_id = d_id;
end;

create or replace procedure removeProfessor(p_id in number)
is
begin
    delete from professors
    where prof_id = p_id;
end;

create or replace procedure removeStudent(s_id in number)
is
begin
    delete from students
    where stud_id = s_id;
end;


create or replace procedure removeStudRecord(s_id in number, c_id in number)
is
begin
    delete from student_records
    where stud_id = s_id and course_id = c_id;
end;

