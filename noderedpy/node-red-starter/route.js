
const express = require("express"),
    path = require("path"),
    fs = require("fs");

function mapGet(exapp, info, inputFile, outputFile) {
    exapp.get(info.url, ( req, res ) => {
        fs.writeFileSync(
            inputFile,
            JSON.stringify({
                url: info.url,
                data: req.params
            })
        );

        while (true) {
            if (fs.existsSync(outputFile)) {
                var content = JSON.parse(fs.readFileSync(outputFile, { encoding: "utf-8" }));
                fs.unlinkSync(outputFile);
                break;
            }
        }

        if (content.state == "success") {
            if (typeof(content.data) == "string" || content.data instanceof String) {
                res.send(content.data);
            }
            else {
                res.json(content.data);
            }
        }
        else {
            res.json(content);
        }

        // try {
        //     res.json(JSON.parse(content));
        // }
        // catch {
        //     res.send(content);
        // }
    });
}

function mapPost(exapp, info, inputFile, outputFile) {
    exapp.post(info.url, ( req, res ) => {
        fs.writeFileSync(
            inputFile,
            JSON.stringify({
                url: info.url,
                data: req.body
            })
        );

        while (true) {
            if (fs.existsSync(outputFile)) {
                var content = JSON.parse(fs.readFileSync(outputFile));
                fs.unlinkSync(outputFile);
                break;
            }
        }

        if (content.state == "success") {
            if (typeof(content.data) == "string" || content.data instanceof String) {
                res.send(content.data);
            }
            else {
                res.json(content.data);
            }
        }
        else {
            res.json(content);
        }

        // try {
        //     res.json(JSON.parse(content));
        // }
        // catch {
        //     res.send(content);
        // }
    });
}

function mapStatic(exapp, info) {
    exapp.use(info.url, express.static(info.path));
}

module.exports = {
    setupRoutes(exapp, cacheDir, userRoutes) {
        exapp.use(express.json());
        exapp.use(express.urlencoded({ extended: true }));

        const inputFile = path.join(cacheDir, "route_input.json");
        const outputFile = path.join(cacheDir, "route_output.json");
        for (var info of userRoutes) {
            if (info.method == "get") {
                mapGet(exapp, info, inputFile, outputFile);
            }
            else if (info.method == "post") {
                mapPost(exapp, info, inputFile, outputFile);
            }
            else if (info.method == "static") {
                mapStatic(exapp, info);
            }
        }
    }
};
