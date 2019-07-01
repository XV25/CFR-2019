import RPi.GPIO as gp



gp.setmode(gp.BOARD)
gp.setup(40, gp.IN,pull_up_down=gp.PUD_DOWN)
gp.setup(38,gp.IN)
while True:
    print(gp.input(40))
