const http = require('http');

const requestListener = function(req, res) {
  let body = '';
  req.on('data', function(chunk) {
    body += chunk;
  });
  req.on('end', function() {
    console.log(JSON.parse(body));
    var answer = {
      'granted' : false  // Forbid access
    };
    res.writeHead(200);
    res.end(JSON.stringify(answer));
  });
}

http.createServer(requestListener).listen(8000);
