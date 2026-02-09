/**
 * HIVE Chronos (v1.0) - Node.js Edition
 * Purpose: Provide reliable Unix timestamps without relying on buggy PowerShell formatting.
 */

function getUnixTimestamp() {
    return Math.floor(Date.now() / 1000);
}

function getISOTime() {
    return new Date().toISOString();
}

if (require.main === module) {
    console.log(getUnixTimestamp());
}

module.exports = { getUnixTimestamp, getISOTime };
