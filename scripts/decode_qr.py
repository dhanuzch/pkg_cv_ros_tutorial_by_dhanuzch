#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from pyzbar.pyzbar import decode

class Camera1:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera_1/image_raw", Image,self.callback)
  
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      rospy.logerr(e)

    (rows,cols,channels) = cv_image.shape
    
    image = cv_image

    # Resize a 720x1280 image to 360x640 to fit it on the screen
    resized_image = cv2.resize(image, (360, 640)) 

    cv2.imshow("Camera output", resized_image)

    # convert the resized image to b&w
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    thresh = 40
    img_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

    # decode the obtained qrcode
    qr_result = decode(img_bw)

    rospy.loginfo(qr_result)
    
    cv2.waitKey(5)


def main():
  
  rospy.init_node('decode_qr', anonymous=True)

  ic = Camera1()
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    rospy.loginfo("Shutting down")
  
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
