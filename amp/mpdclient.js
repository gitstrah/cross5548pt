// TODO: recover MPD connection if MPD has restarted
// TODO: get external commands as cmd-line arguments

var fs = require('fs');
var exec = require('child_process').exec;
var mpdlib = require('mpd'),
    cmd = mpdlib.cmd;

var cmd_unmute = "python /opt/amp/unmute.py";
var cmd_mute = "python /opt/amp/mute.py";
var errorMonitorInterval = 600000;
var muteTimeout = 5000; // wait for 5s before muting
var muteTimer = null;

var refreshMPD = function() {
    client.sendCommand(cmd("status", []), function(err, msg) {
        if (err) console.log(err);
        if (msg) {
            var data = mpdlib.parseKeyValueMessage(msg);
            console.log(data.state);
            if (data.state == "play") {
				executePlay();
            } else if (data.state == "stop" || data.state == "pause") {
				executeStop();
            };
        }
    });
};

var executePlay = function() {
	abortMute();
	execute(cmd_unmute, console.log);
}

var executeStop = function() {
	abortMute();
	muteTimer = setTimeout(function() {
		execute(cmd_mute, console.log);
	}, muteTimeout);
}

var abortMute = function() {
	if(muteTimer) {
		clearTimeout(muteTimer);
		muteTimer = null;
	}
}

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