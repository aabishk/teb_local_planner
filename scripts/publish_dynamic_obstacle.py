#!/usr/bin/env python

# Author: franz.albers@tu-dortmund.de

import rospy, math, tf
from teb_local_planner.msg import ObstacleMsg
from geometry_msgs.msg import PolygonStamped, Point32, QuaternionStamped, Quaternion, TwistWithCovariance
from tf.transformations import quaternion_from_euler


def publish_obstacle_msg():
  pub = rospy.Publisher('/test_optim_node/obstacles', ObstacleMsg, queue_size=1)
  #pub = rospy.Publisher('/p3dx/move_base/TebLocalPlannerROS/obstacles', ObstacleMsg, queue_size=1)
  rospy.init_node("test_obstacle_msg")

  y_0 = -3.0
  vel_x = 0.0
  vel_y = 0.3
  range_y = 6.0

  obstacle_msg = ObstacleMsg() 
  obstacle_msg.header.stamp = rospy.Time.now()
  obstacle_msg.header.frame_id = "odom" # CHANGE HERE: odom/map
  
  # Add point obstacle
  obstacle_msg.obstacles.append(PolygonStamped())
  obstacle_msg.obstacles[0].polygon.points = [Point32()]
  obstacle_msg.obstacles[0].polygon.points[0].x = -1.5
  obstacle_msg.obstacles[0].polygon.points[0].y = 0
  obstacle_msg.obstacles[0].polygon.points[0].z = 0

  yaw = math.atan2(vel_y, vel_x)
  q = tf.transformations.quaternion_from_euler(0,0,yaw)
  quat = Quaternion(*q)
  obstacle_msg.orientations.append(QuaternionStamped())
  obstacle_msg.orientations[0].quaternion = quat

  obstacle_msg.velocities.append(TwistWithCovariance())
  obstacle_msg.velocities[0].twist.linear.x = math.sqrt(vel_x*vel_x + vel_y*vel_y)
  obstacle_msg.velocities[0].twist.linear.y = 0
  obstacle_msg.velocities[0].twist.linear.z = 0
  obstacle_msg.velocities[0].twist.angular.x = 0
  obstacle_msg.velocities[0].twist.angular.y = 0
  obstacle_msg.velocities[0].twist.angular.z = 0

  # Add line obstacle
  #obstacle_msg.obstacles.append(PolygonStamped())
  #line_start = Point32()
  #line_start.x = -2.5
  #line_start.y = 0.5
  #line_start.y = -3
  #line_end = Point32()
  #line_end.x = -2.5
  #line_end.y = 2
  #line_end.y = -4
  #obstacle_msg.obstacles[1].polygon.points = [line_start, line_end]
  
  # Add polygon obstacle
  #obstacle_msg.obstacles.append(PolygonStamped())
  #v1 = Point32()
  #v1.x = -1
  #v1.y = -1
  #v2 = Point32()
  #v2.x = -0.5
  #v2.y = -1.5
  #v3 = Point32()
  #v3.x = 0
  #v3.y = -1
  #obstacle_msg.obstacles[2].polygon.points = [v1, v2, v3]

  r = rospy.Rate(10) # 10hz
  t = 0.0
  while not rospy.is_shutdown():
    
    # Vary y component of the point obstacle
    if (vel_y >= 0):
      obstacle_msg.obstacles[0].polygon.points[0].y = y_0 + (vel_y*t)%range_y
    else:
      obstacle_msg.obstacles[0].polygon.points[0].y = y_0 + (vel_y*t)%range_y - range_y

    t = t + 0.1
    
    pub.publish(obstacle_msg)
    
    r.sleep()



if __name__ == '__main__': 
  try:
    publish_obstacle_msg()
  except rospy.ROSInterruptException:
    pass

