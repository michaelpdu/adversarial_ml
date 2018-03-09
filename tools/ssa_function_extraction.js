/**
 * SSA for function analysis
 * Created by michael_du on 12/16/2017.
 */
esprima = require("esprima");
estraverse = require("estraverse");
escodegen = require("escodegen");
var fs = require('fs');
var path = require("path");
var md5 = require('md5');

function_map = {};

function save_function_snippet(dest_dir) {
    if (!fs.existsSync(dest_dir)){
        fs.mkdirSync(dest_dir);
    }
    for (var key in function_map) {
        if (function_map.hasOwnProperty(key)) {
            // console.log(key + " -> " + function_map[key]);
            dest_file = path.join(dest_dir, key);
            fs.writeFile(dest_file, function_map[key], function(err) {
                if(err) {
                    return console.log(err);
                }
                console.log("Save function: "+dest_file);
            });
        }
    }
}

function process_script(script_content, dest_dir) {
    var md5_hash = md5(script_content)
    var ast = esprima.parse(script_content);
    estraverse.traverse(ast, {
        enter: function (node, parent) {
        },
        leave: function (node, parent) {
            try {
                switch (node.type) {
                    case esprima.Syntax.AssignmentExpression: {
                        break;
                    }
                    case esprima.Syntax.ArrayExpression: {
                        break;
                    }
                    case esprima.Syntax.BinaryExpression: {
                        break;
                    }
                    case esprima.Syntax.CallExpression: {
                        break;
                    }
                    case esprima.Syntax.FunctionDeclaration: {

                        var function_code = escodegen.generate(node);
                        key_name = 'aaa';
                        if (node.id.type == 'Identifier') {
                            key_name = node.id.name;
                        }
                        function_map[md5_hash+'_'+key_name] = function_code;
                        break;
                    }
                    case esprima.Syntax.Identifier: {
                        break;
                    }
                    case esprima.Syntax.LogicalExpression: {
                        break;
                    }
                    case esprima.Syntax.MemberExpression: {
                        break;
                    }
                    case esprima.Syntax.NewExpression: {
                        break;
                    }
                    case esprima.Syntax.VariableDeclarator : {
                        break;
                    }
                }
            } catch (err) {
                console.error(err);
            }
        }
    });

    // save all of function codes
    save_function_snippet(dest_dir)
}

function main(filename, dest_dir) {
    var fs = require('fs');
    fs.readFile(filename, 'utf8', function (err, data) {
        if (err) {
            throw err;
        }
        process_script(data, dest_dir);
    });
}

if (module === require.main) {
    main(process.argv[2], process.argv[3]);
}

