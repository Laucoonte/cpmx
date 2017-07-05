import os
import cv2
import time
import argparse
import numpy as np
import tensorflow as tf
import socket

from paths import marker, pathfinder,giveme_the_ponits
from utils import FPS, WebcamVideoStream
from multiprocessing import Process, Queue, Pool
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# ____________________________________________________
# Configuracion del socket
s = socket.socket()
adress = ("172.16.51.48",9999)
s.connect(adress)
# ____________________________________________________

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


## Init program

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

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    #print(np.squeeze(boxes).shape)
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=4)

    a=giveme_the_ponits(
        np.squeeze(boxes),
        np.squeeze(scores),
        width=480,
        height=360,
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

if __name__ == '__main__':
    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')


    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-src', '--source', dest='video_source', type=int,
                        default=3, help='Device index of the camera.')
    parser.add_argument('-wd', '--width', dest='width', type=int,
                        default=480, help='Width of the frames in the video stream.')
    parser.add_argument('-ht', '--height', dest='height', type=int,
                        default=360, help='Height of the frames in the video stream.')
    parser.add_argument('-num-w', '--num-workers', dest='num_workers', type=int,
                        default=2, help='Number of workers.')
    parser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
                        default=5, help='Size of the queue.')
    args = parser.parse_args()

    #
    input_q = Queue(maxsize=args.queue_size)
    output_q = Queue(maxsize=args.queue_size)

    process = Process(target=worker, args=((input_q, output_q)))
    process.daemon = True
    pool = Pool(args.num_workers, worker, (input_q, output_q))
    video_capture = WebcamVideoStream(src=args.video_source,
                                      width=args.width,
                                      height=args.height).start()
    fps = FPS().start()

    while True:  # fps._numFrames < 120
        frame = video_capture.read() #Get a frame
        input_q.put(frame) #Save in input
        t = time.time()

        cv2.imshow('Video', output_q.get()) #show image in "video" -- output_q.get() is an image in np.array()
        fps.update()

        # print('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

        if cv2.waitKey(1) & 0xFF ==  27 : # Press Esc for quit
            break

    fps.stop()
    # print('[INFO] elapsed time (total): {:.2f}'.format(fps.elapsed()))
    # print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))
    video_capture.stop()
    cv2.destroyAllWindows()
