import fsm
import terminatom as tmt
import time

# global variables
f = fsm.fsm()  # finite state machine
robot = tmt.terminatom()
dt = 0.05


#fonction avancer et tourner
def motor(vL,vD):
    robot.leftMotor(vL)
    robot.rightMotor(VD)



# functions (actions of the fsm)
def doLine(): # go until obstacle
    event="Go"
    motor(50,50)
    dFront = robot.ultrason()
    if dFront < 60:
        event = "Turn_left"
    if dFront < 20:
        event="Stop"
    return event

def doStart(): # do no start if obstacle
    event="Go"
    motor(0,0)
    time.sleep(0.5)
    dFront = robot.ultrason()
    if dFront < 20:
        event="Stop"   
    else : 
        event = "Go"
    return event

def doTurnLeft():
    """
    Turn left while there's still a obstacle at the front.
    """
    motor(0,0)
    time.sleep(0.5)
    event = "Go"
    motor(-50,50)
    time.sleep(1)
    dFront = robot.ultrason()
    if dFront < 20:
        event = "Stop"
    motor(0,0)
    time.sleep(0.5)
    return event

  
def doStopAll():
    """
    Stop the program
    """
    event="Stop"
    motor(0,0)
    return event

if __name__== "__main__":

    # define the states
    f.add_state ("Idle")
    f.add_state ("Move")
    f.add_state ("End")
    f.add_state("TurnLeft")

    # defines the events
    f.add_event ("Go")
    f.add_event ("Stop")
    f.add_event("Turn_left")
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Move","Go",doStart)
    f.add_transition ("Move","Move","Go",doLine)
    f.add_transition("TurnLeft","Move","Go",doLine)
    f.add_transition("Move","TurnLeft","Turn_left",doTurnLeft)

    f.add_transition("Move","End","Stop",doStopAll)
    f.add_transition("TurnLeft","End","Stop",doStopAll)
    
    
    

 
    # current state
    f.set_state ("Idle")
    # first event
    f.set_event ("Go")

 
    # fsm loop
    run = True   
    while (run):
        funct = f.run ()
        if f.curState != "End":
            newEvent = funct()
            #print "New Event : ",newEvent
            f.set_event(newEvent)
        else:
            funct()
            run = False
            
    print ("End of the programm")



