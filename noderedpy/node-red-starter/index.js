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
RED.init(RED_server, {
    editorTheme: { projects: { enabled: false } },
    httpAdminRoot: args["admin_root"].startsWith("/") ? args["admin_root"] : `/${args["admin_root"]}`,
    httpNodeRoot: "/",
    flowFile: "noderedpy.json",
    userDir: args["user_dir"],
    paletteCategories: args["user_category"].concat([ "subflows", "flow", "input", "output", "function", "parser", "social", "mobile", "storage", "analysis", "advanced" ])
});

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
