//
//  ViewController.swift
//  cARdboard
//
//  Created by Benjamin Englard on 2/27/15.
//  Copyright (c) 2015 Benjamin Englard. All rights reserved.
//

// Thanks to https://github.com/sallaben/Radius/blob/master/Radius/ViewController.swift
// and http://stackoverflow.com/questions/11251340/convert-image-to-base64-string-in-ios-swift
// for inspiration

import UIKit
import Foundation
import Starscream
import AVFoundation

class ViewController: UIViewController, WebSocketDelegate {
    
    var socket = WebSocket(url: NSURL(scheme: "ws", host: "ec2-52-11-8-41.us-west-2.compute.amazonaws.com:8081", path: "/ws/test/app")!)
    var connected = false
    var laptopJoined = false
    //var coordinates: String!
    
    let captureSession = AVCaptureSession()
    var captureDevice: AVCaptureDevice?
    var stillImageOutput = AVCaptureStillImageOutput()
    var imageData: NSData!
    var shotImage: UIImage!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.multipleTouchEnabled = true
        socket.delegate = self
        socket.connect()
        
        captureSession.sessionPreset = AVCaptureSessionPresetMedium
        let devices = AVCaptureDevice.devices()
        for device in devices {
            if (device.hasMediaType(AVMediaTypeVideo)) {
                if device.position == AVCaptureDevicePosition.Back {
                    captureDevice = device as? AVCaptureDevice
                    if captureDevice != nil {
                        println("Capture device found")
                        beginSession()
                    }
                }
            }
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    func websocketDidConnect(ws: WebSocket) {
        connected = true
        println("Connection!")
    }
    
    override func touchesBegan(touches: NSSet, withEvent event: UIEvent) {
        // One touch: move
        // Multitouch: click
        
        /*let eventType = touches.count == 1 ? "move" : "click"
        var sumX = 0.0
        var sumY = 0.0
        for touch in touches {
            let point = touch.locationInView(self.view)
            sumX += Double(point.x)
            sumY += Double(point.y)
        }
        sumX /= Double(touches.count)
        sumY /= Double(touches.count)
        sumX *= (1280.0 / 375)
        sumY *= (800.0 / 667)
        coordinates = String(format: "%d,%d,", Int(sumX), Int(sumY)) + eventType
        println(coordinates)
        socket.writeString(coordinates)*/
        
        //let touch: AnyObject = touches.anyObject()!
        let eventType = touches.count == 1 ? "tap" : "dtap"
        let rv = "tap," + eventType
        socket.writeString(rv)
    }
    
    func websocketDidDisconnect(ws: WebSocket, error: NSError?) {
        connected = false
        if let e = error {
            println("Connection ended: \(e.localizedDescription)")
        } else {
            println("Connection ended")
        }
    }
    
    func websocketDidReceiveMessage(ws: WebSocket, text: String) {
        if text == "lj" {
            laptopJoined = true
            println("Laptop joined")
        }
    }
    
    func websocketDidReceiveData(ws: WebSocket, data: NSData) {
        println("Received data: \(data.length)")
    }
    
    func beginSession() {
        var err : NSError? = nil
        captureSession.addInput(AVCaptureDeviceInput(device: captureDevice, error: &err))
        if err != nil {
            println("error: \(err?.localizedDescription)")
            return
        }
        captureSession.startRunning()
        NSTimer.scheduledTimerWithTimeInterval(1.0, target: self, selector: "takePicture", userInfo: nil, repeats: true)
    }
    
    func takePicture() {
        if !connected && laptopJoined {
            return
        }
        
        stillImageOutput.outputSettings = [AVVideoCodecKey: AVVideoCodecJPEG]
        if captureSession.canAddOutput(stillImageOutput) {
            captureSession.addOutput(stillImageOutput)
        }
        
        if let videoConnection = stillImageOutput.connectionWithMediaType(AVMediaTypeVideo) {
            stillImageOutput.captureStillImageAsynchronouslyFromConnection(
                videoConnection,
                { (imageDataSampleBuffer, error) -> Void in
                    if imageDataSampleBuffer != nil {
                        self.imageData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(imageDataSampleBuffer)
                        self.shotImage = UIImage(data: self.imageData)
                        
                        let b64 = self.imageData.base64EncodedStringWithOptions(.allZeros)
                        let rv = "pic," + b64
                        self.socket.writeString(rv)
                    }
                })
        }
    }

}

