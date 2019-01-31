
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



function populateTable(wikidataResult) {
    console.log('in populate table');
    //console.log(wikidataResult);
    if (wikidataResult != "None") {

      var myTable= "<table><tr><td style='width: 100px; color: red;'>Wikidata Qid</td>";
      myTable+= "<td style='width: 100px; color: red; text-align: right;'>Name</td>";

      for (var i in wikidataResult){
        //var attrName = item;
        var item = wikidataResult[i];
        var qid = item['qid'];
        var link = item['link'];
        var foundString = item['found_string'];
        var itemLabel = item['item_label'];
        var itemDescription = item['item_description'];

        //add the wikidata items to wikidataReference
        //wikidataReference[qid] = item

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
    };

    //Display the highlighted text
    //document.getElementById("highlightedText").innerHTML = tokenContent;

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };
    return;
}



/*
AJAX FUNCTIONS USED TO POST
 */


function wikidataQuery(tokenContent, tokenUniqueId) {
  //take the tokenContent of the word that was clicked
  //make a post request to django with this information
  //django does a sparql query search and returns the results
  //populate <tableholder> with the information
  console.log('in wikidataQuery');
  console.log(tokenContent);

  let data_dict = { the_post : $("#" + tokenUniqueId).val(),
                  'csrfmiddlewaretoken': getCookie("csrftoken"),
                  //'csrfmiddlewaretoken': getCookie("csrftoken"),
                  'queryDict': tokenContent
                  };

  console.log('data_dict formed');
  console.log(data_dict);


  $.ajax({
      url : "file_upload/", // the endpoint
      type : "POST", // http method
      data : data_dict, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#" + tokenUniqueId).val(''); // remove the value from the input
          console.log(json['wikidataResults'][0]); // log the returned json to the console
          console.log("success"); // another sanity check
          populateTable(json['wikidataResults']);
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });


};

