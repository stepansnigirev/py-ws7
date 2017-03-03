function Wavemeter(options){
    var _wlm = {};
    _wlm.options = options;
    _wlm.wavelengths = [0,0,0,0,0,0,0,0];
    _wlm.callback = null;
    _wlm.parseData = function(d){
        _wlm.wavelengths = d;
        for (var i = 0; i < options.channels.length; i++) {
            var channel = options.channels[i];
            document.getElementById(channel.element).innerHTML = _wlm.wavelengths[channel.channel].toFixed(_wlm.options.precision);
        }
    };

    var addr = _wlm.options.url.replace("http://","").replace("https://","").replace(/\/$/, "");

    _wlm.start = function(){
        _wlm.ws = new WebSocket("ws://"+addr+"/ws/");
        _wlm.ws.onmessage = function(e) {
            var d = JSON.parse(e.data);
            _wlm.parseData(d);
            if(_wlm.callback != null){
                _wlm.callback(d);
            }
        };
    }

    _wlm.onupdate = function(callback){
        _wlm.callback = callback;
    }
    return _wlm;
}