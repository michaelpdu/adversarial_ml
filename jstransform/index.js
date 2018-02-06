var acorn = require('acorn');
var escodegen = require('escodegen')
var estraverse = require('estraverse')
var fs = require('fs');


function toAST(code) {
    var comments = [], tokens = [];
    var ast = acorn.parse(code, {
        // collect ranges for each node
        ranges: true,
        // collect comments in Esprima's format
        onComment: comments,
        // collect token ranges
        onToken: tokens
    });
    return ast;
}

function analyzeInsertPosition(ast) {
    insertPositions = [0];
    estraverse.traverse(ast, {
        enter: function (node, parent) {
            if (node.type == 'FunctionExpression' || node.type == 'FunctionDeclaration') {
                insertPositions.push(node.start)
                // console.log(escodegen.generate(node))
                // return estraverse.VisitorOption.Skip;
            }
            if (node.type == 'ExpressionStatement') {
                // console.log(escodegen.generate(node))
                insertPositions.push(node.start)
            }
        },
        leave: function (node, parent) {

        }
    });
    return insertPositions;
}

function getFunctions(ast) {
    functions = [];
    estraverse.traverse(ast, {
        enter: function (node, parent) {
            if (node.type == 'FunctionExpression' || node.type == 'FunctionDeclaration') {
                insertPositions.push(node.start)
                functions.push(node.id.name);
                // return estraverse.VisitorOption.Skip;
            }
        },
        leave: function (node, parent) {

        }
    });
    return functions;
}


function conflictCheck(src, insertion) {

}

exports.getInsertPositions = function (path) {
    var text = fs.readFileSync(path).toString();
    var positions = analyzeInsertPosition(toAST(text))
    positions.push(text.length)
    return positions;
}
