/*
This file contains all the necessary js functions that are used to render the file
 */



/*
HELPER FUNCTIONS
 */

//function to format strings
//https://coderwall.com/p/flonoa/simple-string-format-in-javascript
String.prototype.format = function() {
    a = this;
    for (k in arguments) {
      a = a.replace("{" + k + "}", arguments[k])
    }
    return a
}

//better way to get the type of object
var toType = function(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
};

//https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 };


/*
FUNCTIONALITY
 */


var highlighted = {};
//all wikidata items are added to this dictionary
//for those items, whose ids are selected, the item will be returned to django
var wikidataReference = {};
var annotated = {};


function alertthis(uniqueId, tokenContent, wikidataResult) {
    //Not the best way of doing this
    //https://stackoverflow.com/questions/5786851/define-global-variable-in-a-javascript-function
    window.uniqueID = uniqueId;
    window.tokenContent = tokenContent;

    if (wikidataResult != "None") {
      var json = JSON.parse(wikidataResult);
      var w = json['w'];
      //console.log(toType(w));

      var myTable= "<table><tr><td style='width: 100px; color: red;'>Wikidata Qid</td>";
      myTable+= "<td style='width: 100px; color: red; text-align: right;'>Name</td>";
      var $dtable = $("<table><tr><td style='width: 100px; color: red;'>Wikidata Qid</td>");
      $dtable.append($("<td style='width: 100px; color: red; text-align: right;'>Name</td>"));


      for (var i in w){
        //var attrName = item;
        var item = w[i];
        var qid = item['qid'];
        var link = item['link'];
        var foundString = item['found_string'];
        var itemLabel = item['item_label'];
        var itemDescription = item['item_description'];

        //add the wikidata items to wikidataReference
        wikidataReference[qid] = item

        let inf = {'qid': qid};


        //must be enclosed like this, because qid is a string value
        myTable+="<tr><td style='width: 100px;' onclick='selectQid(\"" + qid + "\")'>" + qid + "</td>";
        myTable+="<td style='width: 100px; text-align: right;'>" + itemLabel + "</td></tr>";

      }
      document.getElementById('tableholder').innerHTML = myTable;
    }

    var modal = document.getElementById("foo");
    modal.style.display = "block";

    var span = document.getElementById("span");
    span.onclick = function () {
      modal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
    return;
};

function selectQid(wikidataQid){
    annotated[wikidataQid] = {
      'token': tokenContent,
      'uniqueID': uniqueID,
      'wikidataInf': wikidataReference[wikidataQid]
    };
    console.log(tokenContent + ' assigned ' + wikidataQid);
};

function highlightToken() {
    document.getElementById(uniqueID).style.color = 'blue';
    highlighted[uniqueID] = tokenContent;
    console.log('highlighted ' + tokenContent);
    return;
};

function unHighlightToken() {
    delete highlighted[uniqueID];
    document.getElementById(uniqueID).style.color = 'black';
    return
};


/*
AJAX FUNCTIONS USED TO POST
 */

$(document).ready(function () {
    $('#post-form').on('submit', function(event){
        event.preventDefault();
        console.log('form submitted');
        create_post();
  });

    // AJAX for posting
    function create_post() {
      console.log("create post is working!") // sanity check
      let data_dict = { the_post : $('#post-text').val(),
                        //'csrfmiddlewaretoken': '{{ csrf_token }}',
                        'csrfmiddlewaretoken': getCookie("csrftoken"),
                        'highlighted': $.param(highlighted),
                        'annotated': $.param(annotated)
                        };


      $.ajax({
          url : "file_upload/", // the endpoint
          type : "POST", // http method
          data : data_dict, // data sent with the post request

          // handle a successful response
          success : function(json) {
              $('#post-text').val(''); // remove the value from the input
              //console.log(json); // log the returned json to the console
              console.log("success"); // another sanity check
          },

          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    };

});
