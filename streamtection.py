
import sys
import cv2
import os #For Getting directory paths
import time # To know FPS processed
import argparse # To pass args in terminal`
import numpy as np # Sci Library for python
import tensorflow as tf # Tensorflow
import socket # To pass value of movement to Rasp

from gi.repository import Gst
from paths import marker, pathfinder,giveme_the_ponits # Paths Library to find free way
from utils import FPS, WebcamVideoStream  # Utils for stream video
from multiprocessing import Process, Queue, Pool #Multiprocessing
from object_detection.utils import label_map_util # Object detectionlibrary
from object_detection.utils import visualization_utils as vis_util #Object detection library

###################################
#Configuration
# Socket Configuration
IP_RASP ="192.168.43.188"
SPORT_RASP=9000 #Raspberry Socket Port
#GStreamer Port
GPORT_RASP=5000 # Gstreamer Raspberry Port
#Image Detection size configuration in pixels
WIDTH= 480
HEIGHT= 360
###################################

# ____________________________________________________
#Socket initialization
s = socket.socket()
adress = (IP_RASP, SPORT_RASP)
s.connect(adress)
# ____________________________________________________

#Get pwd
CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)
Gst.init(None)
image_arr = None


## Init program

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-src', '--source', dest='video_source', type=int,
                    default=0, help='Device index of the camera.')
parser.add_argument('-wd', '--width', dest='width', type=int,
                    default=WIDTH, help='Width of the frames in the video stream.')
parser.add_argument('-ht', '--height', dest='height', type=int,
                    default=HEIGHT, help='Height of the frames in the video stream.')
parser.add_argument('-num-w', '--num-workers', dest='num_workers', type=int,
                    default=2, help='Number of workers.')
parser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
                    default=5, help='Size of the queue.')
args = parser.parse_args()


def detect_objects(image_np, sess, detection_graph):
    """ image_np image in np array
        sess  tf.Session()
    """
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Detection happens Here
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=4)
    # Prints the output in string format and gives the coordinate of movement
    a=giveme_the_ponits(
        np.squeeze(boxes),
        np.squeeze(scores),
        width=WIDTH,
        height=HEIGHT,
        ycloseness=360,
        xwidthness=80
        )
    return a,image_np

def worker(input_q, output_q):
    sess = tf.Session(graph=detection_graph)
    fps = FPS().start()
    while True:
        fps.update()
        frame = input_q.get()
        a,img = detect_objects(frame, sess, detection_graph)
        output_q.put(img)
        a = str(a)
        print a
        s.send(a)
        s.recv(1024)
    fps.stop()
    sess.close()

# Converts a Buffer of GStreamer in to np.array readable in OpenCV
def gst_to_opencv(sample):
    buf = sample.get_buffer()
    caps = sample.get_caps()
    arr = np.ndarray(
        (caps.get_structure(0).get_value('height'),
         caps.get_structure(0).get_value('width'),
         3),
        buffer=buf.extract_dup(0, buf.get_size()),
        dtype=np.uint8)
    return arr
def new_buffer(sink, data):
    global image_arr
    sample = sink.emit("pull-sample")
    arr = gst_to_opencv(sample)
    image_arr = arr
    #print image_arr.shape
    return Gst.FlowReturn.OK

# PIPELINE PARAMATERS

"""
Basically this pipeline makes with python this
    gst-launch-1.0 -v tcpclientsrc host=IP_RASP port=GIP_RASP \
                       ! gdpdepay !  rtph264depay ! avdec_h264 \
                       ! videoconvert ! appsink sync=false emit-signals=True

"""
source = Gst.ElementFactory.make('tcpclientsrc', 'source')
source.set_property("host", IP_RASP)
source.set_property("port", GPORT_RASP)
gdpdepay = Gst.ElementFactory.make('gdpdepay', 'gdpdepay')
rtph264depay= Gst.ElementFactory.make('rtph264depay', 'rtph264depay')
avdec_h264 = Gst.ElementFactory.make('avdec_h264', 'avdec_h264')
convert = Gst.ElementFactory.make('videoconvert', 'videoconverter')
sink = Gst.ElementFactory.make('appsink', 'sink')
sink.set_property('sync', False)
sink.set_property("emit-signals", True)

# Create the empty pipeline
pipeline = Gst.Pipeline.new("test-pipeline")

if not source or not sink or not pipeline:
    print("Not all elements could be created.")
    exit(-1)

caps = Gst.caps_from_string("video/x-raw, format=(string){BGR, GRAY8}; video/x-bayer,format=(string){rggb,bggr,grbg,gbrg}")

sink.set_property("caps", caps)
sink.connect("new-sample", new_buffer, sink)

# Build the pipeline
pipeline.add(source, gdpdepay, rtph264depay, avdec_h264, convert, sink)

source.link(gdpdepay)
gdpdepay.link(rtph264depay)
rtph264depay.link(avdec_h264)
avdec_h264.link(convert)
convert.link(sink)

# Start playing
ret = pipeline.set_state(Gst.State.PLAYING)
if ret == Gst.StateChangeReturn.FAILURE:
    print("Unable to set the pipeline to the playing state.")
    exit(-1)

# Wait until error or EOS
bus = pipeline.get_bus()
# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


#########################
input_q = Queue(maxsize=args.queue_size)
output_q = Queue(maxsize=args.queue_size)

process = Process(target=worker, args=((input_q, output_q)))
process.daemon = True
pool = Pool(args.num_workers, worker, (input_q, output_q))
#video_capture = WebcamVideoStream(image_arr,
#                                  width=args.width,
#                                  height=args.height).start()
fps = FPS().start()

# Parse message
while True:
    message = bus.timed_pop_filtered(10000, Gst.MessageType.ANY)
    # print "image_arr: ", image_arr
    if image_arr is not None:
        frame = image_arr #Get a frame
        input_q.put(frame) #Save in input
        t = time.time()
        cv2.imshow('Video', output_q.get()) #show image in "video" -- output_q.get() is an image in np.array()
        fps.update()

        print('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

        if cv2.waitKey(1) & 0xFF ==  27 : # Press Esc to Quit
            break

        #cv2.imshow("appsink image arr", image_arr)
        #cv2.waitKey(1)
    if message:
        if message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error received from element %s: %s" % (
                message.src.get_name(), err))
            print("Debugging information: %s" % debug)
            break
        elif message.type == Gst.MessageType.EOS:
            print("End-Of-Stream reached.")
            break
        elif message.type == Gst.MessageType.STATE_CHANGED:
            if isinstance(message.src, Gst.Pipeline):
                old_state, new_state, pending_state = message.parse_state_changed()
                print("Pipeline state changed from %s to %s." %
                       (old_state.value_nick, new_state.value_nick))
        else:
            print("Unexpected message received.")

# Free resources
pipeline.set_state(Gst.State.NULL)
