# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import torch
from imutils.video import WebcamVideoStream,FPS
import threading, queue
import signal
import readchar
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
#Utilizing GPU for the network
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and
# frame dimensions
if args['input'] == 'camera':
	print('Accessing Camera')
	cap = WebcamVideoStream(src = 0).start()
	q = queue.Queue()
	width = 1280
	height = 720
	W = width
	H = height
	def frame_render(queue_from_cam):
            frame = cap.read() # If you capture stream using opencv (cv2.VideoCapture()) the use the following line
            # ret, frame = self.cap.read()
            frame = cv2.resize(frame,(1280, 720))
			#
            queue_from_cam.put(frame)
writer = None
def handler(signum,frame):
	print('Ctrl-C is pressed: stopping the code')
	print("[INFO] cleaning up...")
	writer.release()
	exit(1)
signal.signal(signal.SIGINT,handler)




# try to determine the total number of frames in the video file
#try:
#	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
#		else cv2.CAP_PROP_FRAME_COUNT
#	total = int(vs.get(prop))
#	print("[INFO] {} total frames in video".format(total))

# an error occurred while trying to determine the total
# number of frames in the video file
#except:
#	print("[INFO] could not determine # of frames in video")
#	print("[INFO] no approx. completion time can be provided")
#	total = -1

# loop over frames from the video file stream
while True:
	# read the next frame from the file
	cam = threading.Thread(target=frame_render, args=(q,))
	cam.start()
	cam.join()
	frame = q.get()
	q.task_done()
	fps = FPS().start()
	
	

	# if the frame dimensions are empty, grab them
	#if W is None or H is None:
	#	(H, W) = frame.shape[:2]

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []
	angles_left = []
	angles_right = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")
			angle_left = (W/2 - (centerX - (width / 2))) * 0.02532
			angle_right = (W/2 - (centerX + (width/2))) * 0.02532
			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > args["confidence"]:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# confidences, and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)
				angles_left.append(round(angle_left,2))
				angles_right.append(round(angle_right,2))
	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
		args["threshold"])

	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the frame
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}, angle-l:{}, angle-r:{}".format(LABELS[classIDs[i]],
				confidences[i], angles_left[i], angles_right[i])
			cv2.putText(frame, text, (x, y - 5),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
	#cv2.imshow('inital',frame)
	# check if the video writer is None
	if writer is None:
		print('intial write')
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
		(frame.shape[1], frame.shape[0]), True)

		# some information on processing single frame
		#if total > 0:
			#elap = (end - start)
			#print("[INFO] single frame took {:.4f} seconds".format(elap))
			#print("[INFO] estimated total time to finish: {:.4f}".format(
			#	elap * total))
	writer.write(frame)
	cv2.imshow('realtime',frame)
	cv2.waitKey(1)
	# write the output frame to disk
	

# release the file pointers
	
	fps.update()
	fps.stop()