// Tutorial from https://www.yld.io/blog/building-a-tcp-service-using-node-js/
// https://nodejs.org/api/net.html

const net = require('net');
const EventEmitter = require('events');
const server = net.createServer();
const incoming_events = new EventEmitter();
const Backend = require('./backend');
const be = new Backend();
const events = require('./events.json');

server.on('connection', (socket) => {

    var client = socket.remoteAddress + ':' + socket.remotePort;  
    console.log(`${client} connected`)

    socket.setEncoding('utf8');

    socket.on('data', (data) => {
        try {
            data = JSON.parse(data)
            if (!('event' in data)) throw new Error(); // when no event tag in the req
            if (!(data.event in events)) throw new Error() // when it is not an event we handle
            incoming_events.emit(data.event, data, socket);
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
    console.log('listening on %j', server.address());  
});

incoming_events.on('login', (data, socket) => {
    socket.write(JSON.stringify({
        err: "unimplemented"
    }));
});

incoming_events.on('logout', (data, socket) => {
    socket.write(JSON.stringify({
        err: "unimplemented"
    }));
});

incoming_events.on('get_chunk', (data, socket) => {
    t = be.getChunk(data.coords);
    socket.write(JSON.stringify(t));
});

incoming_events.on('get_players', (data, socket) => {
    socket.write(JSON.stringify(be.getPlayers()));
});

incoming_events.on('update_player', (data, socket) => {
    if (be.updatePlayer(data.id, data.pos))
        socket.write(JSON.stringify({resp: 'success'}));
    else 
    socket.write(JSON.stringify({resp: 'misseed'}));
});

incoming_events.on('get_events', (data, socket) => {
    socket.write(JSON.stringify(be.getEvents()));
});