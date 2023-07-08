#! /usr/bin/env python3
import rospy 
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class CameraTurtle():

    def __init__(self):
        
        # subscribers (camera_info topic)
        self.camera = rospy.Subscriber("camera_info", String, self.camera_callback)
        self.camera_feed = String()

        # publishers
        self.cmd_control = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)

        # nodes
        rospy.init_node("control_node", anonymous=False)

        # actions
        rospy.on_shutdown(self.shutdown)

        # rate
        self.rate = rospy.Rate(10)
        rospy.loginfo("Set rate to 10Hz")
    

    def camera_callback(self, feed):
        """
        Camera feed callback
        """
        self.camera_feed = feed.data 


    def shutdown(self):
        """
        Shutdown callback
        """
        # publish empty twist msg
        rospy.loginfo("Stopping Turtlesim") 
        self.cmd_control.publish(Twist()) 
        # Give time to stop
        rospy.sleep(1)
    

    def move(self):
        """
        Moves according to camera feed (subscribed to node).
        4 types of input:
        - left - 0
        - right - 1
        - forward - 2
        - backward - 3
        """
        
        # init Twist obj
        move_cmd = Twist()
        
        while not rospy.is_shutdown():
            print(str(self.camera_feed))
            # check camera feed 
            if self.camera_feed == "left":
                move_cmd.angular.z = 0.5
                print("turning left...")
            elif self.camera_feed == "right":
                move_cmd.angular.z = -0.5
                print("turning right...")
            elif self.camera_feed == "forward":
                move_cmd.linear.x = 0.5
                print("moving forward...")
            elif self.camera_feed == "backward":
                move_cmd.linear.x = -0.5
                print("moving backward...")
            
            # publish message
            self.cmd_control.publish(move_cmd)
            self.rate.sleep()


if __name__ == "__main__":

    try:
        CameraTurtle().move()
    except:
        pass