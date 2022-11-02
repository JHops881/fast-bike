// Tutorial from https://www.yld.io/blog/building-a-tcp-service-using-node-js/
// https://nodejs.org/api/net.html

const net = require('net');
const server = net.createServer();

const be = require('./backend');
const events = require('./events.json');

server.on('connection', (socket) => {

    var client = socket.remoteAddress + ':' + socket.remotePort;  
    console.log(`${client} connected`)

    socket.setEncoding('utf8');

    socket.on('data', (data) => {
        try {
            req = JSON.parse(data)
            if (!('event' in req)) throw new Error(); // when no event tag in the req
            if (!(req.event in events)) throw new Error() // when it is not an event we handle
            be.emit(req.event, req, socket);
        } catch(e) {
            if (e instanceof SyntaxError) {
                socket.write(JSON.stringify({
                    "err": "request is not parseable into JSON"
                }));
            } else {
                socket.write(JSON.stringify({
                    "err": "request does not contain a valid event"
                }));
            }
        }
    });  

    socket.once('close', () => {  
        console.log(`${client} closed`);  
    });  

    socket.on('error', (error) => {  
        console.log(`${client} error ${error.message}`);  
    });

});

server.listen(4399, () => {    
    console.log('listening on port 4399');  
});
