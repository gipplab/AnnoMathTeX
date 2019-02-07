//those words that are highlighted are added to this dictionary
var highlighted = {};
//all wikidata items are added to this dictionary
//for those items, whose ids are selected, the item will be returned to django
var wikidataReference = {};
//the words that are annotated with a certain wikidata qid are added to this dictionary
//which is returned to Django
var annotatedWQID = {};
//the words that are annotated with a certain NE from surrounding text are added to this dictionary
//which is returned to Django
var annotatedNE = {}



function populateTable(wikidataResult) {
    console.log('in populate table');
    console.log(wikidataResult);
    //todo: change
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
        wikidataReference[qid] = item;

        //must be enclosed like this, because qid is a string value
        myTable+="<tr><td style='width: 100px;' onclick='selectQid(\"" + qid + "\")'>" + qid + "</td>";
        myTable+="<td style='width: 100px; text-align: right;'>" + itemLabel + "</td></tr>";

      }
      document.getElementById('tableholder').innerHTML = myTable;
    }

    var modal = document.getElementById("popupModal");
    modal.style.display = "block";

    var span = document.getElementById("span");
    span.onclick = function () {
      modal.style.display = "none";
    };

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };
    return;
}



function populateTableWordWindow(wordWindow) {
    console.log('in populate table word window');
    var recommendations = JSON.parse(wordWindow)['word_window'];
    if (recommendations != "None") {


      var myTable= "<table><tr><td style='width: 100px; color: red;'>Named Entity</td></tr>";
      //myTable+= "<td style='width: 100px; color: red; text-align: right;'>Name</td>";

      for (var i in recommendations){
        console.log('looping');
        //var attrName = item;
        var item = recommendations[i];
        var content = item['content'];
        var unique_id = item['unique_id'];
        console.log(content);

        //add the wikidata items to wikidataReference
        //wikidataReference[qid] = item;

        //must be enclosed like this, because qid is a string value
        //myTable+="<tr><td style='width: 100px;' onclick='selectQid(\"" + qid + "\")'>" + qid + "</td>";
        //myTable+="<td style='width: 100px; text-align: right;'>" + itemLabel + "</td></tr>";
        myTable+="<tr><td style='width: 100px;' onclick='selectQid(\"" + content + "\")'>" + content + "</td></tr>";

      }
      document.getElementById('tableholder').innerHTML = myTable;
    }



    var modal = document.getElementById("popupModal");
    modal.style.display = "block";

    var span = document.getElementById("span");
    span.onclick = function () {
      modal.style.display = "none";
    };

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };
    return;
}





/*
FUNCTIONALITY USED TO SEND THE INFORMATION ABOUT ANNOTATIONS AND HIGHLIGHTING BACK TO DJANGO
 */

function selectWordWindowNE(unique_id) {
    console.log(tokenContent + ' assigned ' + unique_id)
}


function selectQid(wikidataQid){
    annotatedWQID[wikidataQid] = {
      'token': tokenContent,
      'uniqueID': uniqueID,
      'wikidataInf': wikidataReference[wikidataQid]
    };
    console.log(tokenContent + ' assigned ' + wikidataQid);
}

//select named entity from surrounding text
function selectNE(content){
    annotatedNE[content] = {
        'content': content
    };
    console.log(tokenContent + ' assigned ' + content );
}

function highlightToken() {
    document.getElementById(uniqueID).style.color = 'blue';
    highlighted[uniqueID] = tokenContent;
    console.log('highlighted ' + tokenContent);
    return;
}

function unHighlightToken() {
    delete highlighted[uniqueID];
    document.getElementById(uniqueID).style.color = 'black';
    return;
}





function radioButtonClicked(option) {
    switch (String(option)) {
        case 'Wikidata':
            populateTable(wikidataResults);
            console.log('OPTION: WIKDIATA');
            break;
        case 'WordWindow':
            populateTableWordWindow(wordWindowJson);
            console.log('OPTION: WORD WINDOW');
            break;
        case 'Presaved':
            console.log('Presaved');
            console.log('OPTION: PRESAVED');
            break;
    }
}



/*
AJAX FUNCTIONS USED TO POST THE REQUEST BACK TO DJANGO, WHERE THE WIKIDATA SPARQL QUERY IS EXECUTED
 */

function wordClicked(tokenContent, tokenUniqueId, tokenType, wordWindow) {
  //take the tokenContent of the word that was clicked
  //make a post request to django with this information
  //django does a sparql query search and returns the results
  //populate <tableholder> with the information
  console.log('in wikidataQuery');
  console.log(tokenContent);
  console.log(tokenType);
  //console.log(wordWindow);

  var wordWindowJson = wordWindow;//['word_window'];
  console.log(wordWindowJson);
  //alert(wordWindowJson);



  //Display the highlighted text
  document.getElementById("highlightedText").innerHTML = tokenContent;

  //Not the best way of doing this
  //https://stackoverflow.com/questions/5786851/define-global-variable-in-a-javascript-function
  window.uniqueID = tokenUniqueId;
  window.tokenContent = tokenContent;
  window.wordWindowJson = wordWindowJson

  let data_dict = { the_post : $("#" + tokenUniqueId).val(),
                  'csrfmiddlewaretoken': getCookie("csrftoken"),
                  //'csrfmiddlewaretoken': getCookie("csrftoken"),
                  'queryDict': tokenContent,
                  'tokenType': tokenType,
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
          populateTable(json['wikidataResults']);
          window.wikidataResults = json['wikidataResults'];
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
}


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
                        'annotatedQID': $.param(annotatedWQID),
                        'annotatedNE': $.param(annotatedNE)
                        };


      $.ajax({
          url : "file_upload/", // the endpoint
          type : "POST", // http method
          data : data_dict, // data sent with the post request

          // handle a successful response
          success : function(json) {
              $('#post-text').val(''); // remove the value from the input
              console.log(json['testkey']); // log the returned json to the console
              console.log("success"); // another sanity check
          },

          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    }

});
