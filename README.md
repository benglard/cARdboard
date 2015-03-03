# cARdboard
cARdboard is an augmented reality device that allows me to see and control my remote laptop. It achieves this by controlling several systems:

Laptop to Tablet: My laptop is screen-casting over websockets to a Nexus 7 inside of a typical shipping box. The Nexus 7 screen is projected through a magnifying glass onto a picture frame.

Phone to Laptop: Attached to the outside of the box is my iPhone, which is taking a picture every second and transmitting the image and screen taps back to my laptop over websockets. My laptop has a blob detection algorithm running which detects the location of my hand. The position of my hand in the image is transformed into the position of my mouse cursor, so my hand can control my laptop's mouse. Tapping the iPhone screen clicks my mouse.

I can thus see and control my laptop.

Note: this is hackathon level code.
