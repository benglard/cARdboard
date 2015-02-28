//
//  ViewController.swift
//  cARdboard
//
//  Created by Benjamin Englard on 2/27/15.
//  Copyright (c) 2015 Benjamin Englard. All rights reserved.
//

import UIKit
import Starscream

class ViewController: UIViewController, WebSocketDelegate {
    
    var socket = WebSocket(url: NSURL(scheme: "ws", host: "ec2-52-11-8-41.us-west-2.compute.amazonaws.com:8081", path: "/ws/test/app")!)
    var coordinates: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.multipleTouchEnabled = true
        socket.delegate = self
        socket.connect()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    func websocketDidConnect(ws: WebSocket) {
        println("Connection!")
    }
    
    override func touchesBegan(touches: NSSet, withEvent event: UIEvent) {
        // One touch: move
        // Multitouch: click
        
        let eventType = touches.count == 1 ? "move" : "click"
        var sumX = 0.0
        var sumY = 0.0
        for touch in touches {
            let point = touch.locationInView(self.view)
            sumX += Double(point.x)
            sumY += Double(point.y)
        }
        sumX /= Double(touches.count)
        sumY /= Double(touches.count)
        coordinates = String(format: "%d,%d,", Int(sumX), Int(sumY)) + eventType
        println(coordinates)
        socket.writeString(coordinates)
    }
    
    func websocketDidDisconnect(ws: WebSocket, error: NSError?) {
        if let e = error {
            println("Connection ended: \(e.localizedDescription)")
        } else {
            println("Connection ended")
        }
    }
    
    func websocketDidReceiveMessage(ws: WebSocket, text: String) {
        println("Received text: \(text)")
    }
    
    func websocketDidReceiveData(ws: WebSocket, data: NSData) {
        println("Received data: \(data.length)")
    }

}

