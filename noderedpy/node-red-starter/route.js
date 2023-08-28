
const express = require("express"),
    path = require("path"),
    fs = require("fs");

module.exports = {
    setupRoutes(exapp, cacheDir, userRoutes) {
        exapp.use(express.json());
        exapp.use(express.urlencoded({ extended: true }));

        const inputFile = path.join(cacheDir, "route_input.json");
        const outputFile = path.join(cacheDir, "route_output.json");
        for (var info of userRoutes) {
            if (info.method == "get") {
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
                            var content = fs.readFileSync(outputFile, { encoding: "utf-8" });
                            fs.unlinkSync(outputFile);
                            break;
                        }
                    }

                    try {
                        res.json(JSON.parse(content));
                    }
                    catch {
                        res.send(content);
                    }
                });
            }
            else if (info.method == "post") {
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
                            var content = fs.readFileSync(outputFile);
                            fs.unlinkSync(outputFile);
                            break;
                        }
                    }

                    try {
                        res.json(JSON.parse(content));
                    }
                    catch {
                        res.send(content);
                    }
                });
            }
            else if (info.method == "static") {
                exapp.use(info.url, express.static(info.path));
            }
        }
    }
};
