#frontend
#!/usr/bin/python
import openpyxl

from tkinter import *
import backend

w=Tk(className= 'Student Database')
#w.geometry("600x500")
w.grid_rowconfigure(0,weight=1)
w.grid_rowconfigure(1,weight=1)
w.grid_rowconfigure(2,weight=1)
w.grid_rowconfigure(3,weight=1)
w.grid_rowconfigure(4,weight=1)
w.grid_rowconfigure(5,weight=1)
w.grid_rowconfigure(6,weight=1)
w.grid_rowconfigure(7,weight=1)

w.grid_columnconfigure(0,weight=1)
w.grid_columnconfigure(1,weight=1)
w.grid_columnconfigure(2,weight=1)
w.grid_columnconfigure(3,weight=1)
#w.grid_columnconfigure(4,weight=0)
w.grid_columnconfigure(5,weight=1)

def view_all():
    t.configure(text='')
    list.delete(0,END)
    for row in backend.view():
        list.insert(END,row)
    t.configure(text='All Entries Loaded!',fg='red')
def search():
    t.configure(text='')
    list.delete(0,END)
    rows=backend.search(n.get(),rn.get(),m.get(),at.get())
    for row in rows:
        list.insert(END,row)

test=0
def insert():
    t.configure(text='')
    k=backend.insert(n.get(),rn.get(),m.get(),at.get())
    global test
    if(k==0):
        test=(test+1)%2
        #print(test,type(test))
        #test=t.after(1000,t.grid(row=test))
        t.configure(text='DUPLICATE PRIMARY KEY (ROLL-NO)',fg='red')
        t.grid(column=test,row=8)
    else:
       t.configure(text='Inserted Successfully!',fg='red')
       view_all()


def selected_row(event):
    try:
        t.configure(text='')
        global id,selected_tuple
        key=list.curselection()
        selected_tuple=list.get(key)
        id=selected_tuple[1]

        n.delete(0,END)
        rn.delete(0,END)
        m.delete(0,END)
        at.delete(0,END)
        n.insert(END,selected_tuple[0])
        rn.insert(END,selected_tuple[1])
        m.insert(END,selected_tuple[2])
        at.insert(END,selected_tuple[3])
    except:
        pass

def delete():
    t.configure(text='')
    backend.delete(id)
    view_all()
    t.configure(text="Deleted Successfully!")

def update():
    t.configure(text='')
    try:
        count=backend.update(n.get(),rn.get(),m.get(),at.get())
        view_all()
        if(count>0):
            t.configure(text='Updated Successfully!')
        else:
            raise Exception
    except:
        t.configure(text='Please Provide Registered Roll-No',fg='red')

def defaulter_list():
    t.configure(text='')
    list.delete(0,END)
    rows=backend.defaulter_list()
    for row in rows:
        list.insert(END,row)
    t.configure(text="Defaulters Loaded Successfully!")

name_e=StringVar()
n=Entry(w,textvariable=name_e)
n.grid(row=0,column=1,padx=3,sticky=EW)

rollno_e=StringVar()
rn=Entry(w,textvariable=rollno_e)
rn.grid(row=0,column=5,padx=3,sticky=EW)

marks_e=StringVar()
m=Entry(w,textvariable=marks_e)
m.grid(row=1,column=1,padx=3,sticky=EW)

attendance_e=StringVar()
at=Entry(w,textvariable=attendance_e)
at.grid(row=1,column=5,padx=3,sticky=EW)

name=Label(w,text="Name:")
name.grid(row=0,column=0,pady=2,padx=3)

rollno=Label(w,text="* Roll-No: ")
rollno.grid(row=0,column=3,pady=2,padx=3,columnspan=2)

marks=Label(w,text="Marks:")
marks.grid(row=1,column=0,padx=3)

attendance=Label(w,text="Attendance:")
attendance.grid(row=1,column=3,padx=3,columnspan=2)

list=Listbox(w)
list.grid(row=2,column=0,rowspan=6,columnspan=4,padx=4,pady=3,sticky=NSEW)
list.bind("<<ListboxSelect>>", selected_row)

search=Button(w,text="Search",command=search)
search.grid(row=2,column=5,padx=3,sticky=NSEW)

update=Button(w,text="* Update",command=update)
update.grid(row=3,column=5,padx=3,sticky=NSEW)

insert=Button(w,text="Insert",command=insert)
insert.grid(row=4,column=5,padx=3,sticky=NSEW)

defaulters=Button(w,text="Defaulters",command=defaulter_list)
defaulters.grid(row=5,column=5,padx=3,sticky=NSEW)

view=Button(w,text='View-All',command=view_all)
view.grid(row=6,column=5,padx=3,sticky=NSEW)

delete=Button(w,text="Delete Selected",command=delete)
delete.grid(row=7,column=5,padx=3,sticky=NSEW)

scbr=Scrollbar(w)
scbr.grid(row=2,column=4,rowspan=6,pady=5,sticky=NS)

list.configure(yscrollcommand=scbr.set)
scbr.configure(command=list.yview)

t=Label()
t.grid(row=8,columnspan=7,column=0)

w.mainloop()

#backend
import sqlite3

def connect():
    conn=sqlite3.connect('student.db')
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS student \
    (name TEXT,rollno INTEGER PRIMARY KEY,marks INTEGER,attendance INTEGER)")
    conn.commit()
    conn.close()

def insert(name,rollno,marks,att):
    conn=sqlite3.connect('student.db')
    cur=conn.cursor()
    try:
        cur.execute("INSERT INTO student VALUES (?,?,?,?)"\
                ,(name,rollno,marks,att))
    except:
        return 0
        #print("*****Duplicate Primary Key Roll-No*****")
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect('student.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM student")
    rows=cur.fetchall()
    conn.close()
    return rows

def search(n='',r='',m='',a=''):
    conn=sqlite3.connect('student.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM student WHERE name=? OR rollno=? OR marks=? OR \
    attendance=?",(n,r,m,a))
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn=sqlite3.connect('student.db')
    cur=conn.cursor()
    cur.execute("DELETE FROM student WHERE rollno=?",(id,))
    conn.commit()
    conn.close()

def update(n,r,m,a):
    conn=sqlite3.connect('student.db')
    cur=conn.cursor()
    cur.execute("UPDATE student SET name=?, marks=?,\
     attendance=? WHERE rollno=?",(n,m,a,r))
    conn.commit()
    return cur.rowcount
    conn.close()

def defaulter_list():
    conn=sqlite3.connect('student.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM student WHERE marks < 75 AND attendance < 75")
    rows=cur.fetchall()
    return rows
    conn.close()

print(view())
