// Tutorial from https://www.yld.io/blog/building-a-tcp-service-using-node-js/
// https://nodejs.org/api/net.html

const net = require('net');
const EventEmitter = require('events');
const server = net.createServer();
const incoming_events = new EventEmitter();
const Backend = require('./backend');
const be = new Backend();

server.on('connection', (socket) => {

    var client = socket.remoteAddress + ':' + socket.remotePort;  
    console.log(`${client} connected`)

    socket.setEncoding('utf8');

    socket.on('data', (data) => {
        try {
            data = JSON.parse(data)
            if (!('event' in data))
                throw new Error();
            // TODO add error if the event type is invalid
            incoming_events.emit(data.event, data, socket);
        } catch(e) {
            if (e instanceof SyntaxError) {
                console.log(`${data} is not parseable into JSON`)
            } else {
                console.log(`${data} doesn't contain an event!`)
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

server.listen(4398, () => {    
    console.log('listening on %j', server.address());  
});

incoming_events.on('testing', (data, socket) => {
    socket.write();  
});

incoming_events.on('get_chunk', (data, socket) => {
    t = be.getChunk(data.coords);
    socket.write(JSON.stringify(t));
});

incoming_events.on('update_player', (data, socket) => {
    if (be.updatePlayer(data.id, data.pos))
        socket.write(JSON.stringify({resp: 'success'}));
    else 
    socket.write(JSON.stringify({resp: 'misseed'}));
});

incoming_events.on('del_player', (data, socket) => {
    if (be.removePlayer(data.id))
        socket.write(JSON.stringify({resp: 'success'}));
    else 
        socket.write(JSON.stringify({resp: 'misseed'}));
});

incoming_events.on('get_players', (data, socket) => {
    // Comment
    socket.write(JSON.stringify(be.getPlayers()));

});