# Author: Arsenii Kostenko
###################### Library ###########################################################
import numpy as np
import cv2
import cnn
import virtual_machine_library  # Import the library for interacting with virtual machines
#################### End ##################################################################

#################### Variables ############################################################
# define colors
red_color = (255, 0, 0)
yellow_color = (255, 255, 0)
green_color = (0, 255, 0)
orange_color = (255, 165, 0)
red_color_name = "red"
yellow_color_name = "yellow"
green_color_name = "green"
orange_color_name="orange"
##################### End #################################################################

while(True):
    print('')
    print('Choose an option:',color='yellow')
    print('a) Train Model'color='yellow')
    print('b) Test Model'color='yellow')
    print('c) Test Model with Virtual Machine'color='yellow')
    print('d) Run test you're virtual machine'color='yellow')
    print('e) Exit'color='yellow')
    print('')
    option = input()
    print('')

    if option.lower() == 'c':
        print('###############################################')
        print('Capturing and predicting with Virtual Machine',color='orange')
        print('###############################################')

        # Code to capture the image from the virtual machine using the dedicated library
        captured_image = virtual_machine_library.capture_image()

        # Process the captured image and predict using the CNN model
        npImg, npLabel = cnn.process_data(captured_image, 'A')  # Replace 'A' with appropriate label
        test_data = [[npImg, 'Test']]
        model = cnn.create_model()
        print(cnn.predict_data(test_data[0], model))

    elif option.lower() == 'a':
        model = cnn.create_model()

    elif option.lower() == 'b':
        test_data = cnn.process_test_data()
        cnn.run_test_data(test_data, model)
    elif option.lower() == 'd':
      

    elif option.lower() == 'e':
        break

    else:
        print('Please select a valid option',color='red')
