/*recherche sur la table periodique*/
$(document).ready(function(){

  $(function() {
    $("#periodique-titre").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "periodique-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});


/*recherche sur la table livre*/
$(document).ready(function(){

  $(function() {
    $("#titre_livre").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "livre-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});
