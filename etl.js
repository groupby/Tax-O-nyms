#!/usr/bin/nodejs


var lineReader = require('readline').createInterface({
    input: require('fs').createReadStream('input')
});

lineReader.on('line', function (line) {
    var value = JSON.parse(line);
    if (value["_type"] === "search") {
        var search = value["_source"].search;
        if (search.totalRecordCount > 0 && search.origin.search) {
            var query = search.query;
            // var tokens = query.split(" ");
            if (query) {
                var availableNavigation = search.availableNavigation;
                var nav1 = availableNavigation[0];
                if (nav1.name === "categories.1") {
                    var category = [];
                    var totalCount = 0;
                    for (var i = 0; i < nav1.refinements.length; i++) {
                        var refinement = nav1.refinements[i];
                        totalCount += refinement.count;
                    }

                    for (var i = 0; i < nav1.refinements.length; i++) {
                        var refinement = nav1.refinements[i];
                        category.push({
                            "value": refinement.value,
                            "percentage": refinement.count / totalCount
                        });
                    }
                }
                var output = {"query": query, "category": category};
                console.log(JSON.stringify(output));
            }
        }
    }
});

