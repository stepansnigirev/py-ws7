function Wavemeter(options){
    var _wlm = {};
    _wlm.options = options;
    _wlm.wavelengths = [0,0,0,0,0,0,0,0];
    _wlm.updateCallback = null;
    _wlm.closeCallback = null;
    _wlm.parseData = function(d){
        _wlm.wavelengths = d;
        for (var i = 0; i < options.channels.length; i++) {
            var channel = options.channels[i];
            document.getElementById(channel.element).innerHTML = _wlm.wavelengths[channel.channel].toFixed(_wlm.options.precision);
        }
    };

    // building an address for websocket
    var link = document.createElement("a");
    link.href = _wlm.options.url;
    var addr = link.protocol.replace("http","ws")+"//"+link.host+link.pathname

    _wlm.start = function(){
        _wlm.ws = new WebSocket(addr+"ws/");
        _wlm.ws.onmessage = function(e){
            var d = JSON.parse(e.data);
            _wlm.parseData(d);
            if(_wlm.updateCallback != null){
                _wlm.updateCallback(d);
            }
        };
        _wlm.ws.onclose = function(e){
            setTimeout(_wlm.start, 1000);
            if(_wlm.closeCallback != null){
                _wlm.closeCallback();
            }
        }
    }

    _wlm.onupdate = function(callback){
        _wlm.updateCallback = callback;
    }

    _wlm.onclose = function(callback){
        _wlm.closeCallback = callback;
    }
    return _wlm;
}
