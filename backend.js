const events = require('./events.json');
const EventEmitter = require('events');

class Backend extends EventEmitter {

    constructor() {
        super();
        this.chunk_dim = 8;
        this.chunks = {};
        this.players = {};

        
    }

    getChunk(coords) {
        
    }

    login(user, pass) {

    }

    removePlayer(id) {
        delete this.players[id];
        return true;
    }

    updatePlayer(id, pos) {
        this.players[id] = pos;
        return true;
    }

    getPlayers() {
        return this.players;
    }

    getEvents() {
        return events;
    }


}

be = new Backend();

be.on('login', (req, socket) => {
    socket.write(JSON.stringify({
        err: "unimplemented"
    }));
});

be.on('logout', (req, socket) => {
    socket.write(JSON.stringify({
        err: "unimplemented"
    }));
});

be.on('get_chunk', (req, socket) => {
    coords = req.coords;
    var chunk_key = coords[0] + ' ' + coords[1];
    if (chunk_key in be.chunks){
        return be.chunks[chunk_key];
    } else { // create the chunk!
        var tiles = [];
        for (let y=0; y<be.chunk_dim; y++) {
            for (let x=0; x<be.chunk_dim; x++) {
                var c = [100, 100, 100]
                if (x == 0 || x+1== be.chunk_dim || y == 0 || y+1== be.chunk_dim){
                    c = [255, 0, 0]
                }
                tiles[x+y*be.chunk_dim] = {
                    a: [x + coords[0]*be.chunk_dim, y + coords[1]*be.chunk_dim+1],
                    b: [x + coords[0]*be.chunk_dim + 1, y + coords[1]*be.chunk_dim],
                    color: c
                }
            }
        }
        be.chunks[chunk_key] = {data: tiles};
    }
    socket.write(JSON.stringify(this.chunks[chunk_key]));
});

be.on('get_players', (data, socket) => {
    socket.write(JSON.stringify(be.getPlayers()));
});

be.on('update_player', (data, socket) => {
    if (be.updatePlayer(data.id, data.pos))
        socket.write(JSON.stringify({resp: 'success'}));
    else 
    socket.write(JSON.stringify({resp: 'misseed'}));
});

be.on('get_events', (data, socket) => {
    socket.write(JSON.stringify(be.getEvents()));
});

module.exports = be;