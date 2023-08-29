// import modules
const express = require("express"),
    http = require("http"),
    RED = require("node-red"),
    fs = require("fs"), path = require("path");

// read config file
const configs = JSON.parse(fs.readFileSync(path.join(__dirname, "config.json")));
fs.unlinkSync(path.join(__dirname, "config.json"));


// create express and node-red server
const exapp = express();
const RED_server = http.createServer(exapp);

// set start options
let opts = {
    editorTheme: configs.editorTheme,
    httpAdminRoot: configs.adminRoot,
    httpNodeRoot: configs.nodeRoot,
    flowFile: configs.defaultFlow,
    userDir: configs.userDir,
    paletteCategories: configs.showDefaultCategory ? configs.userCategory.concat([ "subflows", "common", "function", "network", "sequence", "parser", "storage" ]) : configs.userCategory
};
// set auth
if (Array.isArray(configs.adminAuth) && configs.adminAuth.length > 0) {
    var realAuth = [];
    for (var auth of configs.adminAuth) {
        realAuth.push({
            username: auth.username,
            password: require("bcryptjs").hashSync(auth.password, 8),
            permissions: auth.permissions
        });
    }

    opts.adminAuth = {
        type: "credentials",
        users: realAuth
    }
}

// console.log(configs.editorTheme);
RED.init(RED_server, opts);

// node-red default routes
exapp.use("/", express.static("web"));
exapp.use(RED.settings.httpAdminRoot, RED.httpAdmin);
exapp.use(RED.settings.httpNodeRoot, RED.httpNode);

// map routes
require("./route").setupRoutes(exapp, configs.cacheDir, configs.routes);
// set favicon if exists
const faviconFile = path.join(__dirname, "favicon.ico");
if (fs.existsSync(faviconFile)) {
    exapp.use("/favicon.ico", express.static(faviconFile));
}

// start node-red
RED.start().then(() => {
    RED_server.listen(configs.port, configs.enableRemoteAccess ? "0.0.0.0" : "127.0.0.1", () => {
        fs.writeFileSync(path.join(__dirname, "started"), "");
    });
});
