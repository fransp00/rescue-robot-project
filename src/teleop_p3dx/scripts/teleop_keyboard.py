#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import sys
import select
import termios
import tty
import math


# =========================
# Variável global
# =========================
front_blocked = False


# =========================
# Callback do laser
# =========================
def laser_callback(msg):

    global front_blocked

    valid_ranges = []

    # região frontal do laser
    # pega aproximadamente ±15 graus

    total = len(msg.ranges)

    center = total // 2

    window = 30

    front_ranges = msg.ranges[center - window:center + window]

    for r in front_ranges:

        if not math.isinf(r) and not math.isnan(r):
            valid_ranges.append(r)

    if len(valid_ranges) == 0:
        front_blocked = False
        return

    min_distance = min(valid_ranges)

    # distância mínima de segurança
    if min_distance < 1:
        front_blocked = True
    else:
        front_blocked = False


# =========================
# Leitura do teclado
# =========================
def get_key():

    tty.setraw(sys.stdin.fileno())

    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)

    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    return key


# =========================
# Main
# =========================
if __name__ == '__main__':

    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('teleop_keyboard_safe')

    pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=10)

    rospy.Subscriber('/scan', LaserScan, laser_callback)

    vel_msg = Twist()

    linear_speed = 1
    angular_speed = 1.0

    rate = rospy.Rate(20)

    print("Teleop com anti-colisão")
    print("---------------------------")
    print("w -> frente")
    print("s -> ré")
    print("a -> esquerda")
    print("d -> direita")
    print("q -> sair")

    try:

        while not rospy.is_shutdown():

            key = get_key()

            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0

            # =====================
            # Frente
            # =====================
            if key == 'w':

                if front_blocked:
                    print("OBSTÁCULO À FRENTE!")
                    vel_msg.linear.x = 0.0
                else:
                    vel_msg.linear.x = linear_speed

            # =====================
            # Ré
            # =====================
            elif key == 's':
                vel_msg.linear.x = -linear_speed

            # =====================
            # Giro esquerda
            # =====================
            elif key == 'a':
                vel_msg.angular.z = angular_speed

            # =====================
            # Giro direita
            # =====================
            elif key == 'd':
                vel_msg.angular.z = -angular_speed

            elif key == 'q':
                break

            pub.publish(vel_msg)

            rate.sleep()

    except Exception as e:
        print(e)

    finally:

        vel_msg.linear.x = 0.0
        vel_msg.angular.z = 0.0

        pub.publish(vel_msg)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)