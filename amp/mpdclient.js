var fs = require('fs');
var exec = require('child_process').exec;
var mpdlib = require('mpd'),
    cmd = mpdlib.cmd;

var cmd_play = "python /opt/amp/unmute.py";
var cmd_stop = "python /opt/amp/mute.py";
var errorMonitorInterval = 600000;

var refreshMPD = function() {
    client.sendCommand(cmd("status", []), function(err, msg) {
        if (err) console.log(err);
        if (msg) {
            var data = mpdlib.parseKeyValueMessage(msg);
            console.log(data.state);
            if (data.state == "play") {
                execute(cmd_play, console.log);
            } else if (data.state == "stop" || data.state == "pause") {
                execute(cmd_stop, console.log);
            };
        }
    });
};

var firstErrDate, lastErrMessage = "",
    errCount = 0;
// keep alive
setInterval(function() {
    if (errCount > 1) {
        var date = new Date();
        d = date.toLocaleString();
        console.log('[' + d + ']:\t' + 'Last error happend ' + errCount + ' times in the last ' + 
        	Math.round((date - firstErrDate) / 60000) + ' minutes.');
    }
}, errorMonitorInterval);

var logError = function(err, when) {
    var date = new Date();
    d = date.toLocaleString();

    var message = err.message || err;
    if (!firstErrDate || lastErrMessage != message) {
        if (errCount > 1) {
            console.log('[' + d + ']:\t' + message + ' happend ' + errCount + ' times so far.');
        }
        firstErrDate = date;
        lastErrMessage = message;
        errCount = 1;
        console.log('[' + d + ']:\t' + message + ' when ' + when);
    } else {
        errCount++;
    }
}

var execute = function(command, callback) {
    try {
        exec(command, function(error, stdout, stderr) {
            if (error) {
                logError(error, 'executing \'' + command + '\'');
                callback(error.name);
            } else {
                callback(stdout);
            }
        });
    } catch (err) {
        logError(err, 'executing \'' + command + '\'');
        callback(err.name);
    }
};

var getDate = function() {
    var d = new Date();
    return d.getMonth() + 1 + '/' + d.getDate() + '/' + d.getFullYear() + ' ' + 
    d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
};

//===================================
var client = mpdlib.connect({
    port: 6600,
    host: 'localhost',
});

client.on('system-player', refreshMPD);
client.on('system', function(name) {
    if (name == "mixer") refreshMPD();
});
client.on('ready', refreshMPD);