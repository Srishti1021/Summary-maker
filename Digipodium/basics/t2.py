from turtle import *
def polygon(side,dis):
    for i in range(side):
        fd(dis)
        lt(60)
polygon(3,100)
hideturtle()
mainloop()