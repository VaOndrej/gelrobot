import math
import time

import click
import cv2
import matplotlib
import matplotlib.pyplot
import tkinter
from tkinter import filedialog


def find_hair(image, p_list, r, g, b) -> int:
    global count
    angle_deg = 0
    for c in p_list:
        angle_deg = angle_deg + 1
        blue = image[int(c[0]), int(c[1]), 0]
        green = image[int(c[0]), int(c[1]), 1]
        red = image[int(c[0]), int(c[1]), 2]
        
        # these values are in HSV code, it would be best to modifie them before starting with the video
        if r*0.97 < red < 1.03*r and b*0.97 < blue < 1.03*b and g*0.97 < green < 1.03*g:
            return int(angle_deg)


def calculate_angular_velocity(current_angle, old_angle, frequency, frames_skipped) -> float:
    # subtract cur and old angle to get difference = degrees, then divide by time passed
    # result is in degree/s
    # here i know that i have passed one rotation
    if old_angle is None:
        old_angle = current_angle
    if current_angle < old_angle:
        angle_dif = 360 - old_angle + current_angle
    elif current_angle > old_angle:
        angle_dif = current_angle - old_angle
    else:
        angle_dif = 0
    # print(f"Angle dif {angle_dif}")
    # print(angle_dif)
    if angle_dif > 350:
        angle_dif = 360 - angle_dif
    angular_velocity = angle_dif / (frequency * frames_skipped)
    return angular_velocity


@click.command()
@click.option('--frame_rate', default = 60 ,help='Frame rate of video')
@click.option('--skipped', default = 1, help='How many frames should be skipped (for ideal results 1 is best)')
@click.option('--x', help='X axis for the middle of gelrobot')
@click.option('--y', help='Y axis for the middle of gelrobot')
@click.option('--diameter', help='Chosen diameter for gelrobot')
@click.option('--red', help='R value of hair')
@click.option('--green', help='G value of hair')
@click.option('--blue', help='B value of hair')
def main(frame_rate, skipped, x, y, diameter, red, green, blue):
    root = tkinter.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    vs = cv2.VideoCapture(str(file_path))
    length = int(vs.get(cv2. CAP_PROP_FRAME_COUNT))
    success, frame = vs.read()
    start = time.time()
    count = 0
    # two dimensional array with coordinates for pixels where to detect hair
    pixels_list = []
    FREQUENCY = int(frame_rate)
    FRAMES_SKIPPED = int(skipped)
    graph_data_list_x = []
    graph_data_list_y = []
    while success:
        success, frame = vs.read()
        if success is False:
            break
        if count == 2000:
            PI = 3.1415926535
            # create circle outline where hair detection will happen
            i = 0
            previous_angle = 0
            while i < 360:
                angle = i
                x1 = float(diameter) * math.cos(angle * PI / 180)
                y1 = float(diameter) * math.sin(angle * PI / 180)
                pixels_list.append([int(y)+ y1, int(x) + x1])
                i = i + 1
            click.echo('created circular detection area')
            previous_angle = find_hair(frame, pixels_list, float(red), float(green), float(blue)) 

        if count > 2001 and count % FRAMES_SKIPPED == 0:
            # check if hair is at this position
            hair_angle = find_hair(frame, pixels_list, float(red), float(green), float(blue))
            
            if hair_angle is not None:
                if hair_angle != previous_angle:
                    # here i know that some rotation was done
                    velocity = calculate_angular_velocity(hair_angle, previous_angle, FREQUENCY, FRAMES_SKIPPED)
                    if velocity > 0 :
                        previous_angle = hair_angle
                        graph_data_list_x.append(count)
                        graph_data_list_y.append(velocity)
                        #print(f"Calculated angular velocity in degree/s {velocity}")
                    # else:
                    #     previous_angle = hair_angle
                    #     #print(f"Calculated angular velocity in degree/s {velocity}")
                        continue
        if count % 1000 == 0 and count != 0:
            print(f'-------------{length-count}--------------')

        count = count + 1

    # GRAPH creation
    print(f'-------------{count}--------------')
    print(f'\n\033[1mFinished working.... Time elapsed: {time.time() - start} \033[0m')
    matplotlib.pyplot.plot(graph_data_list_x, graph_data_list_y)
    matplotlib.pyplot.ylabel('Angular velocity [degrees/s]')
    matplotlib.pyplot.xlabel('Frames elapsed')
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
