from turtle import *
fillcolor('pink')
pencolor('blue')

for i in range(6):
    fd(100)
    begin_fill()
    for i in range(6):
        fd(50)
        lt(60)
    end_fill()
    rt(60)

hideturtle()
mainloop()