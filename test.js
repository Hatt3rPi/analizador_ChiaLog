const io = require('socket.io-client');

const client = io('https://api.foxypool.io/web-ui');

const poolIdentifier = 'bhd';
client.emit('stats/init', poolIdentifier, ([poolConfig, poolStats, roundStats, liveStats]) => {
  // Do stuff here
});