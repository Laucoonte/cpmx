""" Basically this program makes with python this
    gst-launch-1.0 -v tcpclientsrc host=192.168.1.70 port=5000 \
                       ! gdpdepay !  rtph264depay ! avdec_h264 \
                       ! videoconvert ! autovideosink sync=false

"""

import gi
gi.require_version('Gst','1.0')
gi.require_version('Gtk','3.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import Gst, GLib, GObject, Gtk
from gi.repository import GdkX11, GstVideo

GObject.threads_init()
Gst.init(None)

###################################
#Configuration
#GStreamer Port
IP_RASP ="172.6.52.40"
GPORT_RASP=5000 # Gstreamer Raspberry Port
#Image Detection size configuration in pixels
WIDTH= 480
HEIGHT= 360
###################################


class Player():
    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(800, 450)

        self.drawingarea = Gtk.DrawingArea()
        self.window.add(self.drawingarea)

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        ## Video Streaming Pipeline
        self.source = Gst.ElementFactory.make('tcpclientsrc', 'source')
        self.source.set_property("host", '172.16.52.40')
        self.source.set_property("port", 5000)
        self.gdpdepay = Gst.ElementFactory.make('gdpdepay', 'gdpdepay')
        self.rtph264depay= Gst.ElementFactory.make('rtph264depay', 'rtph264depay')
        self.avdec_h264 = Gst.ElementFactory.make('avdec_h264', 'avdec_h264')
        self.videoconvert = Gst.ElementFactory.make('videoconvert', 'videoconverter')
        self.autovideosink = Gst.ElementFactory.make('autovideosink', 'autovideosink')
        self.autovideosink.set_property('sync', False)

        # Adding Pipeline
        self.pipeline.add(self.source, self.gdpdepay, self.rtph264depay, self.avdec_h264, self.videoconvert, self.autovideosink)
        ## Piping
        self.source.link(self.gdpdepay)
        self.gdpdepay.link(self.rtph264depay)
        self.rtph264depay.link(self.avdec_h264)
        self.avdec_h264.link(self.videoconvert)
        self.videoconvert.link(self.autovideosink)

    def run(self):
        self.window.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.xid = self.drawingarea.get_property('window').get_xid()
        self.pipeline.set_state(Gst.State.PLAYING)
        Gtk.main()
    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()
    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )
    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
p=Player()
p.source.set_property("host",IP_RASP )
p.run()
