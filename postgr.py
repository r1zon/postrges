import psycopg2 as pg

def get_student(student_id, cur):
    cur.execute("""select s.name, c.course_name from student_course sc 
                join student s on s.id = sc.student_id 
                join course c on c.id=sc.course_id 
                where s.id = (%s)""", (student_id, ))
    print(cur.fetchall())

def get_students(course_id, cur):
    cur.execute("""select s.name, c.course_name from student_course sc 
                join student s on s.id = sc.student_id 
                join course c on c.id=sc.course_id 
                where c.id = (%s)""", (course_id, ))
    print(cur.fetchall())

def add_student():
    name = input('Введите имя студента: \n')
    gpa = input('Введите средний бал студента: \n')
    birth = input('Введите дату рождения студента: \n')
    student_dict = {'name': name,
                    'gpa': gpa,
                    'birth': birth
                    }
    return student_dict

def add_students(course,cur):
    students_list = []
    cur.execute("insert into course (course_name) values (%s)", (course,))
    cur.execute("""select * from course""")
    len_course = cur.fetchall()
    while True:
        add = input('Добавить студента? Нажмите y/n')
        if add == 'y':
            students_list.append(add_student())
        if add == 'n':
            break
    for i in students_list:
        cur.execute("insert into student (name, gpa, birth) values (%s,%s,%s)", (i['name'], i['gpa'],i['birth']))
        cur.execute("""select * from student""")
        len_student = cur.fetchall()
        cur.execute("insert into student_course (student_id, course_id) values (%s,%s)", (len_student[len(len_student)-1][0], len_course[len(len_course)-1][0]))

def create_db(cur):
    cur.execute("""
            CREATE TABLE if not exists student(
                id serial PRIMARY KEY,
                name varchar(100) not NULL,
                gpa numeric(10, 2),
                birth timestamp with time zone
            );
            """)

    cur.execute("""
            CREATE TABLE if not exists course(
                id serial PRIMARY KEY,
                course_name varchar(100) not NULL
            );
            """)

    cur.execute("""
            CREATE TABLE if not exists student_course(
                id serial PRIMARY KEY,
                student_id integer references student(id),
                course_id integer references course(id)
            );
            """)

def main():
    dbname = input('Введите название базы данных: ')
    user = input('Введите логин: ')
    password = input('Введите пароль: ')
    with pg.connect(dbname=dbname,
                    user=user,
                    password=password
                    ) as conn:

        cur = conn.cursor()
        while True:
            next = input('Нажмите:\n'
                         'q - для выхода\n'
                         'c - создать таблицы\n'
                         's - добавить студентов на курс\n'
                         'gs -  получить студента по его id\n'
                         'gsc - получить всех студентов курса\n')
            if next == 'c':
                create_db(cur)
                conn.commit()
            if next == 's':
                course = input('Введите номер курса, на который будут отправлены студенты:\n')
                add_students(course,cur)
                conn.commit()
            if next == 'gs':
                student_id = input('Введите id студента:\n')
                get_student(student_id,cur)
            if next == 'gsc':
                course_id = input('Введите id курса:\n')
                get_students(course_id,cur)
            if next == 'q':
                break
main()


