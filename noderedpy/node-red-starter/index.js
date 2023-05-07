// import modules
const { ArgumentParser } = require("argparse"),
    express = require("express"),
    http = require("http"),
    RED = require("node-red"),
    fs = require("fs"), path = require("path");

// parser
const parser = new ArgumentParser();
parser.add_argument("--user-dir", { type: "str" });
parser.add_argument("--admin-root", { type: "str" });
parser.add_argument("--port", { type: "int" });
parser.add_argument("--user-category", { type: "str", default: "" });
parser.add_argument("--show-default-category", { type: "str" });
const args = parser.parse_args();

// parse user-category
if (args["user_category"] == "") {
    args["user_category"] = [];
}
else {
    const raw_categories = args["user_category"].split(",");
    args["user_category"] = [];
    for (var raw_category of raw_categories) {
        args["user_category"].push(raw_category.trim());
    }
}


// create express and node-red server
const exapp = express();
const RED_server = http.createServer(exapp);

// set configs
var editorTheme = JSON.parse(fs.readFileSync(path.join(__dirname, "editorTheme.json")))
editorTheme["projects"] = { enabled: false };

let opts = {
    editorTheme: editorTheme,
    httpAdminRoot: args["admin_root"].startsWith("/") ? args["admin_root"] : `/${args["admin_root"]}`,
    httpNodeRoot: "/",
    flowFile: "noderedpy.json",
    userDir: args["user_dir"],
    paletteCategories: args["show_default_category"] == "true" ? args["user_category"].concat([ "subflows", "common", "function", "network", "sequence", "parser", "storage" ]) : args["user_category"]
};
// if (![ "None", "null", "" ].includes(args["admin_auth"])) {
//     opts.adminAuth = {
//         type: "credentials",
//         users: [
//             {
//                 username: "nodered-py",
//                 password: args["admin_auth"],
//                 permissions: "*"
//             }
//         ]
//     };
//     opts.httpNodeAuth = {
//         user: "nodered-py", pass: args["admin_auth"]
//     };

//     fs.writeFileSync(path.join(args["user_dir"], "settings.js"), `
// module.exports = ${JSON.stringify(opts, space = 4)};
// `);
// }

RED.init(RED_server, opts);

// node-red default routes
exapp.use("/", express.static("web"));
exapp.use(RED.settings.httpAdminRoot, RED.httpAdmin);
exapp.use(RED.settings.httpNodeRoot, RED.httpNode);

// start node-red
RED.start().then(() => {
    RED_server.listen(args.port, "0.0.0.0", () => {
        fs.writeFileSync(path.join(__dirname, "started"), "");
    });
});
