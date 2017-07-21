#!/usr/bin/nodejs


var lineReader = require('readline').createInterface({
    input: require('fs').createReadStream('input.json')
});

var cat = {
    "baby & child": 0,
    "beauty": 1,
    "diet & nutrition": 2,
    "health & medicine": 3,
    "home health care": 4,
    "household & grocery": 5,
    "personal care": 6,
    "sexual health": 7,
    "vitamins": 8
};

lineReader.on('line', function (line) {
    var value = JSON.parse(line);
    if (value["_type"] === "search") {
        var search = value["_source"].search;
        if (search.totalRecordCount > 0 && search.origin.search) {
            var query = search.query;
            var tokens = query.split(" ");
            if (query && tokens.length == 1) {
                var availableNavigation = search.availableNavigation;
                var nav1 = availableNavigation[0];
                if (nav1.name === "categories.1") {
                    var category = [];
                    for (var i = 0; i < nav1.refinements.length; i++) {

                        var refinement = nav1.refinements[i];
                        category.push({
                            "value": refinement,
                            "percentage": refinement.count / search.totalRecordCount
                        });
                    }
                }
                var output = {"query": tokens[0], "category": category};
                console.log(JSON.stringify(output));
            }
        }
    }
});

