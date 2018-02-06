**JSTransform is used to find a proper position to insert code for automatic JavaScript code generate**

## Installation dependencies

```bash
npm install
```

## Usage

First analyze your code, find all potential insert positions as follows

```javascript
var jstransform = require('jstransform');

// get all possible insert positions by
var positions = jstransform.getInsertPositions(filePath);

```

change you code

```javascript
function saveTextToFile(filePath, text) {
    fs.writeFileSync(filePath, text)
}

for (var i = 0; i < positions.length; i++) {
    saveTextToFile(i.toString() + '.js', insertCodeAt(code, positions[i], 'var x = 1;\n'));
}
```

you can reference ./test/test.js for more details

## TODO

* conflict check for insert and original code
* more positions, current only support insert code before statement and function