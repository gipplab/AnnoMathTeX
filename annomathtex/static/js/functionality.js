//those words that are marked as NE are added to this dictionary
var marked = {};
//those tokens, that were marked by the system, but user rejected the suggestion
var unmarked = {};
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

var annotated = {};

var linkedWords;
var linkedMathSymbols;



function populateTable(results, source) {
    /*
    possible sources: concatenated, wikidata, wordWindow, arXiv, wikipedia
     */

    console.log('populateTable, source: ', source)


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
    function ww(id) {
        if (name in annotated) {
            annotated[name]['uniqueIDs'].push(id);
        }
        else {
            annotatedWW[name] = {
            'token': tokenContent,
            'content': name,
            //'wikidataInf': wikidataReference[qid],
            'uniqueIDs': [id]
            };
        }
    }
    ww(uniqueID);
    handleLinkedTokens(ww);
    console.log(tokenContent + ' assigned ' + content );
}


function handleLinkedTokens(f) {
    /*
    This function is used to annotate, mark the identical tokens in the document.
    i.e. if a word, identifier, formula is marked by the user, then all other
    occurences of the same token are marked accross the entire document.
    This function takes a function f as argument, since a lot of differnen functions need this
    functionality.
     */

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
            f(id)
            //document.getElementById(id).style.color = 'blue';
        }
    }
}



/*
FUNCTIONALITY USED TO SEND THE INFORMATION ABOUT ANNOTATIONS AND HIGHLIGHTING BACK TO DJANGO
 */


function markAsNE() {

    function mark(id) {
        document.getElementById(id).style.color = 'blue';
        marked[id] = tokenContent;
    }

    mark(uniqueID);
    handleLinkedTokens(mark);
    console.log('marked ' + tokenContent);

}

function unMarkAsNE() {

    function unmark(id) {
        document.getElementById(id).style.color = 'grey';
        unmarked[id] = tokenContent;
    }

    unmark(uniqueID);
    handleLinkedTokens(unmark);
    console.log('unmarked ' + tokenContent);
}



function radioButtonClicked(option) {
    switch (String(option)) {
        case 'Concatenated':
            populateTable(concatenatedResults, 'concatenated');
            console.log('OPTION: CONCATENATED')
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


//store the linked tokens in a variable, to enable only having to
//annotate a symbol, word, formula once for entire doc
function linkTokens(linked_words, linked_math_symbols) {
    //JSON.parse(wordWindow)['word_window'];
    //console.log(linkedWords);
    //console.log(linkedMathSymbols);
    linkedWords = JSON.parse(linked_words)['linked_words'];
    linkedMathSymbols = JSON.parse(linked_math_symbols)['linked_math_symbols'];

    //console.log(linkedWords['Sun']);
    //var sun = linkedWords['Sun'][0];
    //console.log(linked_words);
    //document.getElementById("SUNID").style.color = 'blue';
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

function clickToken(tokenContent, tokenUniqueId, tokenType, mathEnv, tokenHighlight) {

    /*console.log(typeof(linkedWords));
    console.log(typeof(linkedMathSymbols));
    console.log(testVal)
    console.log(wikipediaEvaluationItems);*/

    //console.log(tokenUniqueId);

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
    document.getElementById("wikidataBtn").checked = true;

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


          switch (tokenType) {
              //todo: clean up
              case 'Identifier':
                  console.log('Identifier');
                  document.getElementById("wordWindowBtn").hidden = false;
                  document.getElementById("arXivBtn").hidden = false;
                  document.getElementById("wikipediaBtn").hidden = false;
                  break;
              case 'Word':
                  console.log('Word');
                  document.getElementById("wordWindowBtn").hidden = true;
                  document.getElementById("arXivBtn").hidden = true;
                  document.getElementById("wikipediaBtn").hidden = true;
                  break;
              case 'Formula':
                  console.log('Formula');
                  document.getElementById("wordWindowBtn").hidden = false;
                  document.getElementById("arXivBtn").hidden = true;
                  document.getElementById("wikipediaBtn").hidden = true;
                  break;
          }
          window.concatenatedResults = json['concatenatedResults'];
          window.wikidataResults = json['wikidataResults'];
          window.arXivEvaluationItems = json['arXivEvaluationItems'];
          window.wikipediaEvaluationItems = json['wikipediaEvaluationItems'];
          window.wordWindow = json['wordWindow'];

          populateTable(json['concatenatedResults'], 'concatenated');

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
                        'annotatedQID': $.param(annotatedWQID),
                        'annotatedWW': $.param(annotatedWW),
                        'annotatedArXiv': $.param(annotatedArXiv),
                        'annotatedWikipedia': $.param(annotatedWikipedia),
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
