class Backend {

    constructor() {
        this.chunk_dim = 8;
        this.chunks = {};
    }

    getChunk(coords) {
        var chunk_key = coords[0] + ' ' + coords[1];
        if (chunk_key in this.chunks){
            return this.chunks[chunk_key];
        } else { // create the chunk!
            var tiles = [];
            for (let y=0; y<this.chunk_dim; y++) {
                for (let x=0; x<this.chunk_dim; x++) {
                    tiles[x+y*this.chunk_dim] = {
                        a: [x + coords[0]*this.chunk_dim, y + coords[1]*this.chunk_dim+1],
                        b: [x + coords[0]*this.chunk_dim + 1, y + coords[1]*this.chunk_dim],
                        color: [0, 0, 0, 0]
                    }
                }
            }
            this.chunks[chunk_key] = {tiles: tiles};
        }
        return this.chunks[chunk_key];
    } 


}

module.exports = Backend;