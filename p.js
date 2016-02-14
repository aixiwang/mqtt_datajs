//=======================================
// MQTT-DATAJS Sample Code v0.1
//
// Copyright(c) Aixi Wang (aixi.wang@hotmail.com)
//=======================================
//-------------------------------
// event_handler
//-------------------------------
function event_handler(msg){
    // puts(msg);
    log_dump(msg['topic'] + '->' + msg['payload']);
    return 0;
}

//-------------------------------
//          main
//-------------------------------

// sub topic
mqtt_subscribe('home/#',2);
puts('start processing loop ...');
log_dump('start processing loop ...');

// processing loop
while(1){
    // get new data
    s = queue_in_get(0.1);
    if (s !== ''){
        puts('data 1!');    
        try {
            // msg = JSON.stringify(s);
            msg = JSON.parse(s);
        }        
        catch(e) {
            puts('exception ' + e.message + e.name)
            continue;
            
        }
        puts('data 2!');        
        // puts(msg['topic']);
        // puts(msg['payload']);
        // puts(msg['ts']);
        ret_s = event_handler(msg);
        puts(ret_s);       

    } 
    sleep(0.1);    
}

