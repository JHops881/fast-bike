

// Tutorial from https://www.yld.io/blog/building-a-tcp-service-using-node-js/

const net = require('net');
var server = net.createServer();
server.on('connection', handleConnection);

server.listen(8080, function() {    
    console.log('LISTENING ON: %j', server.address());  
});

function handleConnection(conn) {    

    var remoteAddress = conn.remoteAddress + ':' + conn.remotePort;  
    console.log('NEW CONNECTION:\n\tADDR :%s', remoteAddress);

    conn.setEncoding('utf8');

    conn.on('data', onConnData);  
    conn.once('close', onConnClose);  
    conn.on('error', onConnError);

    function onConnData (d) {  
        console.log('DATA:\n\tADDR: %s\n\tDATA: %j', remoteAddress, d); 
        data = JSON.parse(d)
        // work with data
        

        // send the response
        resp = {
            data: data,
            time: Date.now(),
            status: true
        }
        conn.write(JSON.stringify(resp));  
    }

    function onConnClose() {  
        console.log('CLOSED:\n\tADDR: %s', remoteAddress);  
    }

    function onConnError(err) {  
        console.log('ERROR:\n\tADDR: %s\n\t MSG: %s', remoteAddress, err.message);  
    }  
}