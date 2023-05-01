from turtle import *
fillcolor('pink')
pencolor('black')
pensize()
# to increase the speed
speed(0)

for i in range(6):
    fd(100)
    for i in range(6):
        fd(50)
        begin_fill()
        for i in range(6):
            fd(25)
            circle(10)
            dot(5)
            rt(60)
        end_fill()
        lt(60)
    rt(60)

hideturtle()
mainloop()