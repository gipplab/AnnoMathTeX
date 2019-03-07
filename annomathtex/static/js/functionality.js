//those words that are highlighted are added to this dictionary
var highlighted = {};
//those tokens, that were highlighted, but user rejected the highlighting
var rejectedHighlight = {};
//all wikidata items are added to this dictionary
//for those items, whose ids are selected, the item will be returned to django
var wikidataReference = {};
//the words that are annotated with a certain wikidata qid are added to this dictionary
//which is returned to Django
var annotatedWQID = {};
//the words that are annotated with a certain NE from surrounding text (word window) are added to this dictionary
//which is returned to Django
var annotatedWW = {};
//the words that are annotated with a certain item from the arXiv evaluation list are added to this dictionary
//which is returned to Django
var annotatedArXiv = {};
//the words that are annotated with a certain item from the wikipedia evaluation list are added to this dictionary
//which is returned to Django
var annotatedWikipedia = {};


var linkedWords;
var linkedMathSymbols;


function populateTable(wikidataResult) {
    console.log('Function: populateTable');
    //todo: change
    if (wikidataResult != "None") {

      var myTable= "<table><tr><td style='width: 100px; color: red;'>Wikidata QID</td>";
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
}



function populateTableWordWindow(wordWindow) {
    console.log('Function: populateTableWordWindow');
    //var recommendations = wordWindow;
    var myTable= "<table><tr><td style='width: 100px; color: red;'>Named Entity</td></tr>";
    if (wordWindow != "None") {

      var recommendations = JSON.parse(wordWindow)['word_window'];

      for (var i in recommendations){
        var item = recommendations[i];
        var content = item['content'];
        var unique_id = item['unique_id'];

        myTable+="<tr><td style='width: 100px;' onclick='selectWW(\"" + content + "\")'>" + content + "</td></tr>";

      }
    }

    document.getElementById('tableholder').innerHTML = myTable;

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
}



function populateTableArXiv(arXivEvaluationItems) {
    console.log('Function: populateTableArXiv');
    var myTable= "<table><tr><td style='width: 100px; color: red;'>Item</td>";
    myTable+= "<td style='width: 100px; color: red; text-align: right;'>Value</td></tr>";
    //var evaluationItems = arXivEvaluationItems;
    if (arXivEvaluationItems != "None") {

      var evaluationItems = JSON.parse(arXivEvaluationItems)['arXiv_evaluation_items'];




      for (var i in evaluationItems){
        var item = evaluationItems[i];
        var name = item['name'];
        var value = item['value'];

        myTable+="<tr><td style='width: 100px;' onclick='selectArXiv(\"" + name + "\")'>" + name + "</td>";
        myTable+="<td style='width: 100px; text-align: right;'>" + value + "</td></tr>";

      }
    }

    document.getElementById('tableholder').innerHTML = myTable;

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
}




function populateTableWikipedia(wikipediaEvaluationItems) {
    console.log('Function: populateTableWikipedia');

    var myTable= "<table><tr><td style='width: 100px; color: red;'>Item</td>";
    myTable+= "<td style='width: 100px; color: red; text-align: right;'>Value</td></tr>";

    //var evaluationItems = wikipediaEvaluationItems;
    if (wikipediaEvaluationItems != "None") {

      var evaluationItems = JSON.parse(wikipediaEvaluationItems)['wikipedia_evaluation_items'];

      for (var i in evaluationItems){
        var item = evaluationItems[i];
        var value = item['value'];
        var identifier = item['identifier'];
        var description = item['description'];
        var wikimiediaLink = item['wikimedia_link'];

        myTable+="<tr><td style='width: 100px;' onclick='selectWikipedia(\"" + i + "\")'>" + identifier + "</td>";
        myTable+="<td style='width: 100px; text-align: right;'>" + description + "</td></tr>";
      }
    }

    document.getElementById('tableholder').innerHTML = myTable;


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
}





/*
FUNCTIONALITY USED TO SEND THE INFORMATION ABOUT ANNOTATIONS AND HIGHLIGHTING BACK TO DJANGO
 */


function selectQid(wikidataQid){
    annotatedWQID[wikidataQid] = {
      'token': tokenContent,
      'uniqueID': uniqueID,
      'wikidataInf': wikidataReference[wikidataQid]
    };
    console.log(tokenContent + ' assigned ' + wikidataQid);
}

//select named entity from surrounding text
function selectWW(content){
    annotatedWW[content] = {
        'content': content
    };
    console.log(tokenContent + ' assigned ' + content );
}

function selectArXiv(name){
    annotatedArXiv[name] = {
        'name': name
    };
    console.log(tokenContent + ' assigned ' + name );
}

function selectWikipedia(name){
    annotatedWikipedia[name] = {
        'name': name
    };
    console.log(tokenContent + ' assigned ' + name );
}





function highlightToken() {
    document.getElementById(uniqueID).style.color = 'blue';
    highlighted[uniqueID] = tokenContent;
    console.log('highlighted ' + tokenContent);
}

function unHighlightToken() {
    delete highlighted[uniqueID];
    document.getElementById(uniqueID).style.color = 'black';
    console.log('un highlighted ' + tokenContent);
}

function rejectHighlight() {
    document.getElementById(uniqueID).style.color = 'grey';
    rejectedHighlight[uniqueID] = tokenContent;
    console.log('rejected ' + tokenContent);
}





function radioButtonClicked(option) {
    switch (String(option)) {
        case 'Wikidata':
            //if ()
            populateTable(wikidataResults);
            console.log('OPTION: WIKDIATA');
            break;
        case 'WordWindow':
            populateTableWordWindow(wordWindow);
            console.log('OPTION: WORD WINDOW');
            break;
        case 'arXiv':
            populateTableArXiv(arXivEvaluationItems);
            console.log('OPTION: arXiv');
            break;
        case 'Wikipedia':
            populateTableWikipedia(wikipediaEvaluationItems);
            console.log('OPTION: Wikipedia');
            break;
    }
}


//store the linked tokens in a variable, to enable only having to
//annotate a symbol, word, formula once for entire doc
function linkTokens(linked_words, linked_math_symbols) {
    //JSON.parse(wordWindow)['word_window'];
    //console.log(linkedWords);
    //console.log(linkedMathSymbols);
    linkedWords = JSON.parse(linked_words)['linked_words'];
    linkedMathSymbols = JSON.parse(linked_math_symbols)['linked_math_symbols'];

    //console.log(linkedWords['Sun']);

    var sun = linkedWords['Sun'];

    console.log(sun[0]);

    //console.log(i);

    //document.getElementById(sun[0]).style.color = 'blue';
    //document.getElementById(sun[1]).style.color = 'blue';

    /*for (var i in sun) {
        //document.getElementById(sun[i]).style.color = "blue";
        console.log(typeof(sun[i]));
    }*/


}


/*
AJAX FUNCTIONS USED TO POST THE REQUEST BACK TO DJANGO, WHERE THE WIKIDATA SPARQL QUERY IS EXECUTED
 */

function clickToken(tokenContent, tokenUniqueId, tokenType, wordWindow, arXivEvaluationItems, wikipediaEvaluationItems, mathEnv, tokenHighlight) {

    /*console.log(typeof(linkedWords));
    console.log(typeof(linkedMathSymbols));
    console.log(testVal)
    console.log(wikipediaEvaluationItems);*/

    //Display the highlighted text
    if (mathEnv == 'None') {
        var fillText = tokenContent;
    }
    else {
        var fillText = mathEnv;
    }

    //make reject button hidden if the token is not highlighted
    if (tokenHighlight == "black") {
        document.getElementById("rejectHighlightBtn").hidden = true;
    }
    else {
        document.getElementById("rejectHighlightBtn").hidden = false;
    }

    document.getElementById("highlightedText").innerHTML = fillText;

    //check wikidata option (default)
    document.getElementById("wikidataButton").checked = true;

    //Not the best way of doing this
    //https://stackoverflow.com/questions/5786851/define-global-variable-in-a-javascript-function
    window.uniqueID = tokenUniqueId;
    window.tokenContent = tokenContent;
    window.arXivEvaluationItems = arXivEvaluationItems;
    window.wikipediaEvaluationItems = wikipediaEvaluationItems;
    window.tokenType = tokenType;


    let data_dict = { the_post : $("#" + tokenUniqueId).val(),
                  'csrfmiddlewaretoken': getCookie("csrftoken"),
                  //'csrfmiddlewaretoken': getCookie("csrftoken"),
                  'queryDict': tokenContent,
                  'tokenType': tokenType,
                  'mathEnv': mathEnv,
                  };

    $.ajax({
      url : "file_upload/", // the endpoint
      type : "POST", // http method
      data : data_dict, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#" + tokenUniqueId).val(''); // remove the value from the input


          switch (tokenType) {
              case 'Identifier':
                  console.log('Identifier');
                  document.getElementById("wordWindowButton").hidden = false;
                  populateTable(json['wikidataResults']);
                  window.wordWindow = wordWindow;
                  break;
              case 'Word':
                  console.log('Word');
                  document.getElementById("wordWindowButton").hidden = true;
                  populateTable(json['wikidataResults']);
                  window.wordWindow = [];
                  break;
              case 'Formula':
                  console.log('Formula');
                  document.getElementById("wordWindowButton").hidden = false;
                  populateTable(json['wikidataResults']);
                  window.wordWindow = wordWindow;
                  break;
          }
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
        create_post();
  });

    // AJAX for posting
    function create_post() {
      let data_dict = { the_post : $('#post-text').val(),
                        //'csrfmiddlewaretoken': '{{ csrf_token }}',
                        'csrfmiddlewaretoken': getCookie("csrftoken"),
                        'highlighted': $.param(highlighted),
                        'annotatedQID': $.param(annotatedWQID),
                        'annotatedWW': $.param(annotatedWW),
                        'annotatedArXiv': $.param(annotatedArXiv),
                        'annotatedWikipedia': $.param(annotatedWikipedia),
                        'rejectedHighlight': $.param(rejectedHighlight)
                        };


      $.ajax({
          url : "file_upload/", // the endpoint
          type : "POST", // http method
          data : data_dict, // data sent with the post request

          // handle a successful response
          success : function(json) {
              $('#post-text').val(''); // remove the value from the input
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
