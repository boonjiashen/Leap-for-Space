# Leap motion controller for space invaders
# Differs from the listener in that we only poll the controller when we want.

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import math

class SpaceController(Leap.Controller):

    def poll(self):

        frame = self.frame()

        left, right, fire = False, False, False

        # Get left/right command with first hand
        HALF_ANGLE = 10
        MIN_VELOCITY = 500
        hands = frame.hands
        if hands:
            # Get arm bone
            # Arm at 9 o'clock = -90 deg yaw
            # Arm at 3 o'clock = 90 deg yaw
            #tool = hands[0].arm  # Use arm as pointing tool
            tool = hands[0]  # Use hand itself as pointing tool
            yaw = math.atan2(-tool.direction.z, tool.direction.x) *  \
                    Leap.RAD_TO_DEG - 90

            left = yaw > HALF_ANGLE
            right = yaw < -HALF_ANGLE

        # Get fire command from first index finger of first hand
        index_fingers = [finger
                for hand in frame.hands
                for finger in hand.fingers
                if finger.type() == 1]
        if index_fingers:
            finger = index_fingers[0]
            up_velocity = finger.tip_velocity.y
            fire = up_velocity > MIN_VELOCITY

        return left, right, fire

def main():

    # Create a sample listener and controller
    controller = SpaceController()

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    while True:
        left, right, fire = controller.poll()
        print ('Go left? %i, Go right? %i, Fire? %i' % (left, right, fire))
        time.sleep(.01)

    #keyboard.tap_key('a')
    #keyboard.tap_key('d')
    #try:
        #sys.stdin.readline()
    #except KeyboardInterrupt:
        #pass
    #finally:
        #controller.remove_listener(listener)  # Remove the sample listener when done 

if __name__ == "__main__":
    main()
