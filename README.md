# TvSupervision

**TvSupervision** is a software system for checking if Tv works as it's 
normal way when it is opened from closed status.

List below are some standard or third libs which are used for the system.

**Standard Lib**
***
* logging - Handle all log events. Look for [logging](https://docs.python.org/3.6/library/logging.html).
* os - Handling file and dir relatively. Look for [os](https://docs.python.org/3.6/library/os.html).
* sys - Access to some variables provided command line. Look for [sys](https://docs.python.org/3.6/library/sys.html).
* threading - Handle multi-thread so as to control multi cameras 
simultaneously. Look for [threading](https://docs.python.org/3.6/library/threading.html).
* time - Handle data and time relatively. Use these to get current time for
 test result. Look for [time](https://docs.python.org/3.6/library/time.html).
* webbrowser - The webbrowser module provides a high-level interface to allow 
displaying Web-based documents to users. The system uses this to open test 
result directly in your browser. Look for [webbrowser](https://docs.python.org/3.6/library/webbrowser.html).
* xml.dom.minidom - Use this to save all test result into .xml files. Look 
for [xml.dom.minidom](https://docs.python.org/3.6/library/xml.dom.minidom.html).

**Third Lib**
***
* PyQt5 - Handle all software UI. Look for [QT](http://doc.qt.io/).
* cv2 - Image process, comparing standard img and any time's image. Look for 
[Python OpenCv](https://docs.opencv.org/3.4.3/d6/d00/tutorial_py_root.html).
* numpy - Essential lib for opencv-python. Look for [numpy](http://www.numpy.org/).
* pyserial - Provide comport control for infrared plate or power relay. Look 
for [pyserial](https://pythonhosted.org/pyserial/).
