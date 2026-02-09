# SKILL: HIVE Core Utilities (Node.js)

Provides stable, cross-environment replacements for buggy shell commands like `dir`, `ls`, and `curl`.

## 🛠️ File System: Stable List (ls)

Replaces `dir /B`. Usage: `node -e "require('fs').readdirSync('.').forEach(f => console.log(f))"`

```javascript
const fs = require('fs');
const path = require('path');

function listFiles(dir, pattern = '') {
    return fs.readdirSync(dir).filter(f => f.includes(pattern));
}
```

## 🌐 Network: Stable Request (curl)

Replaces `curl` / `Invoke-WebRequest`. Usage: `node scripts/hive/net_fetch.js <url>`

```javascript
const http = require('http');

function quickFetch(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}
```

## 📜 Directives

1. **NO CURL**: Do not use `curl` or `iwr`. Use `web_fetch` or `node scripts/hive/net_fetch.js`.
2. **NO DIR**: Do not use `dir` or `ls`. Use `node -e "fs.readdirSync..."` or specialized Node.js scripts.
3. **Encoding**: Always assume UTF-8 for all file operations.
