const http = require('http');

const url = process.argv[2] || 'http://127.0.0.1:8317/v1/models';

http.get(url, (res) => {
    let body = '';
    res.on('data', (chunk) => body += chunk);
    res.on('end', () => {
        console.log(body);
    });
}).on('error', (e) => {
    console.error(`Fetch error: ${e.message}`);
    process.exit(1);
});
