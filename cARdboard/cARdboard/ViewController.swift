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
    
    var socket = WebSocket(url: NSURL(scheme: "ws", host: "localhost:8081", path: "/ws/test/app")!)
    var coordinates: String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
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
        let touch: AnyObject? = touches.anyObject()
        let point = touch?.locationInView(self.view)
        let x = Int((point?.x)!)
        let y = Int((point?.y)!)
        coordinates = String(format: "%d,%d", x, y)
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

