function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? null : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function checkParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "(\s|$|&|#|=)"),
        results = regex.exec(location.search);
    return results !== null
}

function RegisterOperations(map) {
    for (var name in map) {
        if (checkParameterByName(name)) {
            var url = map[name];
            window.location.href = url;
        }
    }
}
