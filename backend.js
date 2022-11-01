const events = require('./events.json');

class Backend {

    constructor() {
        this.chunk_dim = 8;
        this.chunks = {};
        this.players = {}
    }

    getChunk(coords) {
        var chunk_key = coords[0] + ' ' + coords[1];
        if (chunk_key in this.chunks){
            return this.chunks[chunk_key];
        } else { // create the chunk!
            var tiles = [];
            for (let y=0; y<this.chunk_dim; y++) {
                for (let x=0; x<this.chunk_dim; x++) {
                    var c = [100, 100, 100]
                    if (x == 0 || x+1== this.chunk_dim || y == 0 || y+1== this.chunk_dim){
                        c = [255, 0, 0]
                    }
                    tiles[x+y*this.chunk_dim] = {
                        a: [x + coords[0]*this.chunk_dim, y + coords[1]*this.chunk_dim+1],
                        b: [x + coords[0]*this.chunk_dim + 1, y + coords[1]*this.chunk_dim],
                        color: c
                    }
                }
            }
            this.chunks[chunk_key] = {tiles: tiles};
        }
        return this.chunks[chunk_key];
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

module.exports = Backend;