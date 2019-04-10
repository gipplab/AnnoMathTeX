/*
This file contains the functionality for the frontend of the project.
It is called in annotation_template.html.
 */


//those words that are marked as NE are added to this dictionary
var marked = {};
//those tokens, that were marked by the system, but user rejected the suggestion
var unmarked = {};
//all wikidata items are added to this dictionary
//for those items, whose ids are selected, the item will be returned to django
var wikidataReference = {};
//The tokens (identifier, formula, word) that are annotated with an item from wikidata, the arXiv evaluation list, the
//wikipedia evaluation list or the word window are stored in this dictionary. Upon saving, the dictionary is sent to the
//backend for further processing (saving, writing to database).
var annotated = {};



function populateTable(results, source) {
    /*
    Possible sources: concatenated, wikidata, wordWindow, arXiv, wikipedia.
    This function renders the table with the results that were retrieved by the backend of the project for a token that
    the user mouse cliked. The table is rendered in the popup modal.

    Each row in the table is stored as a string in an array. after the entire table has been created, an html element
    that serves as a placeholder for the table is filled with its content.
     */

    console.log('populateTable, source: ', source);
    var myTable= "<table><tr><td style='width: 100px; color: red;'>Name</td></tr>";
    if (results != "None"){
        for (var i in results){
            var item = results[i];
            var name = item['name'];
            //var qid = item['qid'];
            var qid = null;
            myTable+="<tr><td style='width: 100px;' onclick='selected(\"" + name + "," + qid + "," + source + "\")'>" + name + "</td></tr>";
            //myTable+="<tr><td style='width: 100px;' onclick=\"" + selectedFunction + name + "\")'>" + name + "</td></tr>";

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


function selected(name, qid, source){
    /*
    This function is called when the user annotates a token with an element from the created table (e.g. from the
    retrieved wikidata results).
     */
    function ww(id) {
        if (name in annotated) {
            annotated[name]['uniqueIDs'].push(id);
        }
        else {
            annotated[name] = {
            'token': tokenContent,
            'content': name,
            //'wikidataInf': wikidataReference[qid],
            'uniqueIDs': [id]
            };
        }
    }
    ww(uniqueID);
    handleLinkedTokens(ww);
    console.log(tokenContent + ' assigned ' + name );
}


function handleLinkedTokens(func) {
    /*
    This function is used to annotate, mark the identical tokens in the document.
    i.e. if a word, identifier, formula is marked by the user, then all other
    occurences of the same token are marked accross the entire document.
    This function takes a function f as argument, since a lot of differnen functions need this
    functionality.
     */

    console.log('linkedWords: ', linkedWords);
    console.log('linkedMathSymbols: ', linkedMathSymbols);

    if (tokenType == 'Word') {
        dicToCheck = linkedWords;
    }
    else {
        dicToCheck = linkedMathSymbols;
    }

    if (tokenContent in dicToCheck) {
        var word = dicToCheck[tokenContent];
        for (i in word) {
            var id = word[i];
            func(id)
        }
    }
}



/*
FUNCTIONALITY USED TO SEND THE INFORMATION ABOUT ANNOTATIONS AND HIGHLIGHTING BACK TO DJANGO
 */


function markAsNE() {
    /*
    This function is called when the user selects a word in the document that wasn't found by the named entity tagger
    and determines that it is a named entity after all.
     */

    function mark(id) {
        document.getElementById(id).style.color = 'blue';
        marked[id] = tokenContent;
    }

    mark(uniqueID);
    handleLinkedTokens(mark);
    console.log('marked ' + tokenContent);

}

function unMarkAsNE() {
    /*
    This function is called when the user selects a named entity in the document that wasn found by the named entity
    tagger but determines that it isn't a named entity after all.
     */

    function unmark(id) {
        document.getElementById(id).style.color = 'grey';
        unmarked[id] = tokenContent;
    }

    unmark(uniqueID);
    handleLinkedTokens(unmark);
    console.log('unmarked ' + tokenContent);
}



function radioButtonClicked(option) {
    /*
    This function is called when the user selects a different column of results to be displayed in the table inside the
    popup modal.
     */
    switch (String(option)) {
        case 'Concatenated':
            populateTable(concatenatedResults, 'concatenated');
            console.log('OPTION: CONCATENATED');
            break;
        case 'Wikidata':
            populateTable(wikidataResults, 'wikidata');
            console.log('OPTION: WIKDIATA');
            break;
        case 'WordWindow':
            populateTable(wordWindow, 'wordWindow');
            console.log('OPTION: WORD WINDOW');
            break;
        case 'arXiv':
            populateTable(arXivEvaluationItems, 'arXiv');
            console.log('OPTION: arXiv');
            break;
        case 'Wikipedia':
            populateTable(wikipediaEvaluationItems, 'wikipedia');
            console.log('OPTION: Wikipedia');
            break;
    }
}



function linkTokens(linked_words, linked_math_symbols) {
    /*
    Linked tokens are stored in a variable, to enable only having to annotate an identifier, word, formula once for
    entire document.
     */
    window.linkedWords = JSON.parse(linked_words)['linkedWords'];
    window.linkedMathSymbols = JSON.parse(linked_math_symbols)['linkedMathSymbols'];
}


/*
AJAX FUNCTIONS USED TO POST THE REQUEST BACK TO DJANGO, WHERE THE WIKIDATA SPARQL QUERY IS EXECUTED
 */

function clickToken(tokenContent, tokenUniqueId, tokenType, mathEnv, tokenHighlight) {


    //Display the selected tokens
    if (mathEnv == 'None') {
        var fillText = tokenContent;
    }
    else {
        var fillText = mathEnv;
    }

    //hide both buttons for math environments
    if (tokenType == 'Identifier' || tokenType == 'Formula') {
        document.getElementById("unmarkBtn").hidden = true;
        document.getElementById("markBtn").hidden = true;
    }
    else if (tokenHighlight == "black") {
        document.getElementById("unmarkBtn").hidden = true;
        document.getElementById("markBtn").hidden = false;
    }
    else {
        document.getElementById("markBtn").hidden = true;
        document.getElementById("unmarkBtn").hidden = false;
    }

    document.getElementById("highlightedText").innerHTML = fillText;

    //check wikidata option (default)
    if (tokenType == 'Word'){
        document.getElementById("wikidataBtn").checked = true;
    }
    else {
        document.getElementById("concatenatedLabel").checked = true;
    }


    //Not the best way of doing this
    //https://stackoverflow.com/questions/5786851/define-global-variable-in-a-javascript-function
    window.uniqueID = tokenUniqueId;
    window.tokenContent = tokenContent;
    //window.arXivEvaluationItems = arXivEvaluationItems;
    //window.wikipediaEvaluationItems = wikipediaEvaluationItems;
    window.tokenType = tokenType;


    let data_dict = { the_post : $("#" + tokenUniqueId).val(),
                  'csrfmiddlewaretoken': getCookie("csrftoken"),
                  //'csrfmiddlewaretoken': getCookie("csrftoken"),
                  'queryDict': tokenContent,
                  'tokenType': tokenType,
                  'mathEnv': mathEnv,
                  'uniqueId': tokenUniqueId
                  };


    $.ajax({
      url : "file_upload/", // the endpoint
      type : "POST", // http method
      data : data_dict, // data sent with the post request

      // handle a successful response
      success : function(json) {
          $("#" + tokenUniqueId).val(''); // remove the value from the input


          window.concatenatedResults = json['concatenatedResults'];
          window.wikidataResults = json['wikidataResults'];
          window.arXivEvaluationItems = json['arXivEvaluationItems'];
          window.wikipediaEvaluationItems = json['wikipediaEvaluationItems'];
          window.wordWindow = json['wordWindow'];


          switch (tokenType) {
              //todo: clean up
              case 'Identifier':
                  console.log('Identifier');
                  document.getElementById("concatenatedLabel").hidden = false;
                  document.getElementById("wordWindowLabel").hidden = false;
                  document.getElementById("arXivLabel").hidden = false;
                  document.getElementById("wikipediaLabel").hidden = false;
                  document.getElementById("concatenatedBtn").checked = true;
                  populateTable(concatenatedResults, 'concatenated');
                  break;
              case 'Word':
                  console.log('Word');
                  document.getElementById("concatenatedLabel").hidden = true;
                  document.getElementById("wordWindowLabel").hidden = true;
                  document.getElementById("arXivLabel").hidden = true;
                  document.getElementById("wikipediaLabel").hidden = true;
                  document.getElementById("wikidataBtn").checked = true;
                  populateTable(wikidataResults, 'wikidata');
                  break;
              case 'Formula':
                  console.log('Formula');
                  document.getElementById("concatenatedLabel").hidden = false;
                  document.getElementById("wordWindowLabel").hidden = false;
                  document.getElementById("arXivLabel").hidden = true;
                  document.getElementById("wikipediaLabel").hidden = true;
                  document.getElementById("concatenatedBtn").checked = true;
                  populateTable(concatenatedResults, 'concatenated');
                  break;
          }

          //console.log('WORD WINDOW   ', json['wordWindow']);
          //console.log('wikidata: ', json['wikidataResults']);
          //console.log('arXiv: ', json['arXivEvaluationItems']);
          //console.log('wikipedia: ', json['wikipediaEvaluationItems']);
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
                        'marked': $.param(marked),
                        'annotated': $.param(annotated),
                        'unmarked': $.param(unmarked)
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
