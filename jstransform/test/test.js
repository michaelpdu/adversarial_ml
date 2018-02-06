var fs = require('fs');
var jstransform = require(__dirname + '/../index.js');
var filePath = __dirname + '/../test/good-js.txt';
var code = fs.readFileSync(filePath).toString();

function insertCodeAt(src, position, insertion) {
    return src.slice(0, position) + insertion + src.slice(position);
}

var positions = jstransform.getInsertPositions(filePath);

function saveTextToFile(filePath, text) {
    fs.writeFileSync(filePath, text);
}

for (var i = 0; i < positions.length; i++) {
    saveTextToFile(i.toString() + '.js', insertCodeAt(code, positions[i], 'var x = 1;\n'));
    console.log('======================================');
}