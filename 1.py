# import numpy as np
# import streamlit as st
# from tensorflow.keras.models import load_model
# import cv2
# from collections import deque
# import os
# import subprocess



# # loading the saved model
# loaded_model = load_model("Elevator_LRCN_model_0.8454545736312866.h5")


# # Specify the height and width to which each video frame will be resized in our dataset.
# IMAGE_HEIGHT , IMAGE_WIDTH = 64, 64

# # Specify the list containing the names of the classes used for training. Feel free to choose any set of classes.
# CLASSES_LIST = ['Anomaly', 'Bad Footage', 'Empty', 'Full', 'Normal']

# # Specify the number of frames of a video that will be fed to the model as one sequence.
# SEQUENCE_LENGTH = 50


# # creating a function for Prediction
# def predict_on_video(video_file_path, output_file_path, SEQUENCE_LENGTH):
#     '''
#     This function will perform action recognition on a video using the LRCN model.
#     Args:
#     video_file_path:  The path of the video stored in the disk on which the action recognition is to be performed.
#     output_file_path: The path where the ouput video with the predicted action being performed overlayed will be stored.
#     SEQUENCE_LENGTH:  The fixed number of frames of a video that can be passed to the model as one sequence.
#     '''

#     # Initialize the VideoCapture object to read from the video file.
#     video_reader = cv2.VideoCapture("rtsp://192.168.137.189:8080/h264_opus.sdp")

#     # Get the width and height of the video.
#     original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
#     original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Initialize the VideoWriter Object to store the output video in the disk.
#     video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 
#                                 video_reader.get(cv2.CAP_PROP_FPS), (original_video_width, original_video_height))

#     # Declare a queue to store video frames.
#     frames_queue = deque(maxlen = SEQUENCE_LENGTH)

#     # Initialize a variable to store the predicted action being performed in the video.
#     predicted_class_name = ''

#     # Iterate until the video is accessed successfully.
#     while video_reader.isOpened():

#         # Read the frame.
#         ok, frame = video_reader.read() 
        
#         # Check if frame is not read properly then break the loop.
#         if not ok:
#             break

#         # Resize the Frame to fixed Dimensions.
#         resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        
#         # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1.
#         normalized_frame = resized_frame / 255

#         # Appending the pre-processed frame into the frames list.
#         frames_queue.append(normalized_frame)

#         # Check if the number of frames in the queue are equal to the fixed sequence length.
#         if len(frames_queue) == SEQUENCE_LENGTH:

#             # Pass the normalized frames to the model and get the predicted probabilities.
#             predicted_labels_probabilities = loaded_model.predict(np.expand_dims(frames_queue, axis = 0))[0]

#             # Get the index of class with highest probability.
#             predicted_label = np.argmax(predicted_labels_probabilities)

#             # Get the class name using the retrieved index.
#             predicted_class_name = CLASSES_LIST[predicted_label]

#         # Write predicted class name on top of the frame.
#         cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         # Write The frame into the disk using the VideoWriter Object.
#         video_writer.write(frame)
        
#     # Release the VideoCapture and VideoWriter objects.
#     video_reader.release()
#     video_writer.release()

# def main():  
#     # giving a title
#     st.title('Video Classification Web App')
#     #Upload video file
#     uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mpeg"])
#     if uploaded_file is not None:
#         #store the uploaded video locally
#         with open(os.path.join("D:/CODE/JUPYTER NOTEBOOK/ELEVATOR SURVEILLANCE SYSTEM/ELEVATOR VIDEO CLASSIFICATION/temp/",uploaded_file.name.split("/")[-1]),"wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.success("File Uploaded Successfully")

#         if st.button('Classify The Video'):
#             # Construct the output video path. 
#             output_video_file_path = "D:/CODE/JUPYTER NOTEBOOK/ELEVATOR SURVEILLANCE SYSTEM/ELEVATOR VIDEO CLASSIFICATION/output/"+uploaded_file.name.split("/")[-1].split(".")[0]+"_output1.mp4"
#             with st.spinner('Wait for it...'):
#                 # Perform Action Recognition on the Test Video.
#                 predict_on_video("D:/CODE/JUPYTER NOTEBOOK/ELEVATOR SURVEILLANCE SYSTEM/ELEVATOR VIDEO CLASSIFICATION/temp/"+uploaded_file.name.split("/")[-1], output_video_file_path, SEQUENCE_LENGTH)
#                 #OpenCV’s mp4v codec is not supported by HTML5 Video Player at the moment, one just need to use another encoding option which is x264 in this case 
#                 os.chdir('D:/CODE/JUPYTER NOTEBOOK/ELEVATOR SURVEILLANCE SYSTEM/ELEVATOR VIDEO CLASSIFICATION/output/')
#                 subprocess.call(['ffmpeg','-y', '-i', uploaded_file.name.split("/")[-1].split(".")[0]+"_output.mp4",'-vcodec','libx264','-f','mp4','output4.mp4'],shell=True)
#                 st.success('Done!')
            
#             #displaying a local video file
#             video_file = open("D:/CODE/JUPYTER NOTEBOOK/ELEVATOR SURVEILLANCE SYSTEM/ELEVATOR VIDEO CLASSIFICATION/output" + 'output4.mp4', 'rb') #enter the filename with filepath
#             video_bytes = video_file.read() #reading the file
#             st.video(video_bytes) #displaying the video
    
#     else:
#         st.text("Please upload a video file")
  
    
#     while True:
#         cam = cv2.VideoCapture(0)#YHN PAR WO PHONE KA IP LIKHNE KA USING RTSP WO BROWSER PAR JAB RUN KROGE TOH MIL JYEGA IP ADDRESS
#         cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#         FRAME_WINDOW = st.image([])
#         ret, frame = cam.read()
#         if not ret:
#             st.error("Failed to capture frame from camera")
#             st.info("Please turn off the other app that is using the camera and restart app")
#             st.stop()

    
    
# if __name__ == '__main__':
#     main()
    
    
import numpy as np
import streamlit as st
from tensorflow.keras.models import load_model
import cv2
from collections import deque
import os


# loading the saved model
loaded_model = load_model("Elevator_LRCN_model_0.8454545736312866.h5")

# Specify the height and width to which each video frame will be resized in our dataset.
IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64

# Specify the list containing the names of the classes used for training. Feel free to choose any set of classes.
CLASSES_LIST = ['Anomaly', 'Bad Footage', 'Empty', 'Full', 'Normal']

# Specify the number of frames of a video that will be fed to the model as one sequence.
SEQUENCE_LENGTH = 50

# Queue to store frames
frames_queue = deque(maxlen=SEQUENCE_LENGTH)


# creating a function for Prediction
def predict_on_frames(frames_queue):
    '''
    This function will perform action recognition on a sequence of frames using the LRCN model.
    Args:
    frames_queue:  Queue containing frames from webcam.
    '''

    # Check if the number of frames in the queue are equal to the fixed sequence length.
    if len(frames_queue) == SEQUENCE_LENGTH:
        # Convert frames queue to numpy array
        frames_array = np.array(frames_queue)
        
        # Normalize the frames
        normalized_frames = frames_array / 255

        # Pass the normalized frames to the model and get the predicted probabilities.
        predicted_labels_probabilities = loaded_model.predict(np.expand_dims(normalized_frames, axis=0))[0]

        # Get the index of class with highest probability.
        predicted_label = np.argmax(predicted_labels_probabilities)

        # Get the class name using the retrieved index.
        predicted_class_name = CLASSES_LIST[predicted_label]

        return predicted_class_name
    else:
        return ''


def main():
    # giving a title
    st.title('Video Classification Web App')

    # Initialize webcam
    cam = cv2.VideoCapture(0)  # YHN PAR WO PHONE KA IP LIKHNE KA USING RTSP WO BROWSER PAR JAB RUN KROGE TOH MIL JYEGA IP ADDRESS
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    FRAME_WINDOW = st.image([])

    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to capture frame from camera")
            st.info("Please turn off the other app that is using the camera and restart app")
            st.stop()

        # Resize the Frame to fixed Dimensions.
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))

        # Append the resized frame to frames queue
        frames_queue.append(resized_frame)

        # Perform prediction on frames queue
        predicted_class_name = predict_on_frames(frames_queue)

        # Write predicted class name on top of the frame.
        cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        FRAME_WINDOW.image(frame)


if __name__ == '__main__':
    main()
