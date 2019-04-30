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
//The tokens (identifier, formula, word) that are annotatedGLobal with an item from wikidata, the arXiv evaluation list, the
//wikipedia evaluation list or the word window are stored in this dictionary. Upon saving, the dictionary is sent to the
//backend for further processing (saving, writing to database).
var annotated = {'local': {}, 'global':{}};

var tokenAssignedItemGlobal = new Set([]);
var tokenAssignedItemLocal = new Set([]);

var cellColorBasic = '#dddddd';
var cellColorSelectedGlobal = 'pink';
var cellColorSelectedLocal = 'blue';

var identifierColorBasic = '#c94f0c';
var formulaColorBasic = '#ffa500';
var annotatedColor = '#04B404';

//var identifierColorAnnotated = '#F88000';



var cellCounter = 0;


function populateTable2() {

    arXivEvaluationItems = jsonResults['arXivEvaluationItems'];
    wikipediaEvaluationItems = jsonResults['wikipediaEvaluationItems'];
    wikidataResults = jsonResults['wikidataResults'];
    wordWindow = jsonResults['wordWindow'];

    console.log(jsonResults);


    function createCell(item, source, rowNum) {
        var name = item['name'];
        var backgroundColor = cellColorBasic;

        var containsHighlightedName = false;


        if (tokenAssignedItemGlobal.has(name)){
            backgroundColor = cellColorSelectedGlobal;
            containsHighlightedName = true;
        } else if (tokenAssignedItemLocal.has(name) && annotated['local'][tokenContent]['mathEnv'] == mathEnv) {
            backgroundColor = cellColorSelectedLocal;
        }

        var qid = '';

        var cellID = "cell" + source + rowNum;

        //console.log(cellID);

        var args = [
            name,
            qid,
            source,
            backgroundColor,
            cellID,
            containsHighlightedName
        ];
        var argsString = args.join('---');

        var td = "<td id="+ cellID +" style='background-color:" +  backgroundColor + "'" + "onclick='selected(\"" + argsString + "\")'>" + name + "</td>";
        return td;

    }

    var table= "<table><tr><td>arXiv</td><td>Wikipedia</td><td>Wikidata</td><td>WordWindow</td></tr>";


    for (i = 0; i<10; i++) {
        if (arXivEvaluationItems.length >= i && arXivEvaluationItems.length > 0){
            var tdArXiv = createCell(arXivEvaluationItems[i], 'ArXiv', i);
        }
        if (wikipediaEvaluationItems.length >= i && wikipediaEvaluationItems.length > 0) {
            var tdWikipedia = createCell(wikipediaEvaluationItems[i], 'Wikipedia', i);
        }
        if (wikidataResults.length >= i && wikidataResults.length > 0) {
            var tdWikidata = createCell(wikidataResults[i], 'Wikidata', i);
        }
        if (wordWindow.length >= i && wordWindow.length > 0) {
            var tdWordWindow = createCell(wordWindow[i], 'WordWindow', i);
        }
        var tr = '<tr>' + tdArXiv + tdWikipedia + tdWikidata + tdWordWindow + '</tr>';

        table += tr;

    }

    document.getElementById('tableholder').innerHTML = table;
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


function populateTable(results, source) {
    /*
    Possible sources: concatenated, wikidata, wordWindow, arXiv, wikipedia.
    This function renders the table with the results that were retrieved by the backend of the project for a token that
    the user mouse cliked. The table is rendered in the popup modal.

    Each row in the table is stored as a string in an array. after the entire table has been created, an html element
    that serves as a placeholder for the table is filled with its content.
     */

    console.log('populate table tokenAssignedItemGlobal: ', tokenAssignedItemGlobal);
    console.log('populate table tokenAssignedItemLocal: ', tokenAssignedItemLocal);

    var qidHeader = source=='Concatenated' ? 'QID' : '';

    //console.log('BBAAARR: ', annotated['local'][tokenContent]);


    //for local v global annotation
    //if a highlighted name is already in table, second annotation will get different color
    var containsHighlightedName = false;

    if (source=='Concatenated') {
        var myTable= "<table><tr><td style='width: 100px;'>Name</td><td>" + qidHeader + "</td></tr>";
    } else {
        var myTable= "<table><tr><td style='width: 100px;'>Name</td></tr>";
    }


    if (results != "None"){
        for (var i in results){

            cellCounter += 1;

            var item = results[i];
            var name = item['name'];
            var qid = source=='Concatenated' ? item['qid'] : '';
            var url = source=='Concatenated' ? item['link'] : '';
            var backgroundColor = cellColorBasic;//'#dddddd';

            if (tokenAssignedItemGlobal.has(name)){
                backgroundColor = cellColorSelectedGlobal;
                containsHighlightedName = true;
            } else if (tokenAssignedItemLocal.has(name) && annotated['local'][tokenContent]['mathEnv'] == mathEnv) {
                //console.log('FOOOO: ', annotated['local'][tokenContent]);
                backgroundColor = cellColorSelectedLocal;
            }

            var cellID = "cell" + cellCounter;
            var args = [
                name,
                qid,
                source,
                backgroundColor,
                cellID,
                containsHighlightedName
            ];
            var argsString = args.join('---');
            myTable+="<tr><td id="+ cellID +" style='background-color:" +  backgroundColor + "'" + "onclick='selected(\"" + argsString + "\")'>" + name + "</td><td style='width: 20px'><a target='_blank' rel='noopener noreferrer' href='" + url + "'>" + qid + "</a></td></tr>";

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




function setAnnotatedColor(id) {
    console.log('setAnnotatedColor ' + typeof(id));
    document.getElementById(id).style.color = annotatedColor;
    //document.getElementById('4---4').style.color = annotatedColor;
}

function setBasicColor(id) {
    if (tokenType == 'Identifier') {
        document.getElementById(id).style.color = identifierColorBasic;
    } else if (tokenType == 'Formula'){
        document.getElementById(id).style.color = formulaColorBasic;
    }
}


function selected(argsString){
    /*
    This function is called when the user annotates a token with an element from the created table (e.g. from the
    retrieved wikidata results).
     */


    var argsArray = argsString.split('---');
    var name = argsArray[0];
    var qid = argsArray[1];
    var source = argsArray[2];
    var backgroundColor = argsArray[3];
    var cellID = argsArray[4];
    var containsHighlightedName = (argsArray[5] === 'true');

    console.log(argsString);


    if (containsHighlightedName && backgroundColor == cellColorBasic) {
        //select a cell & global annotation has been made
        document.getElementById(cellID).style.backgroundColor = cellColorSelectedLocal;
        tokenAssignedItemLocal.add(name);
        addToAnnotated(uniqueID, false);
        console.log(annotated);
        setAnnotatedColor(uniqueID);

    } else if(backgroundColor == cellColorSelectedLocal){
        //reverse local annotation
        document.getElementById(cellID).style.backgroundColor = cellColorBasic;
        tokenAssignedItemLocal.delete(name);
        delete annotated['local'][tokenContent];
        //setBasicColor(uniqueID);

    } else if (backgroundColor == cellColorBasic){
        //global annotation
        document.getElementById(cellID).style.backgroundColor = cellColorSelectedGlobal;
        tokenAssignedItemGlobal.add(name);
        setAnnotatedColor(uniqueID);
        //console.log('ADDED ENERGY: ', tokenAssignedItemGlobal);
        //addToAnnotated(uniqueID);
        handleLinkedTokens(addToAnnotated);
        handleLinkedTokens(setAnnotatedColor);
    } else {
        //reverse global annotation
        document.getElementById(cellID).style.backgroundColor = cellColorBasic;
        setBasicColor(uniqueID);
        tokenAssignedItemGlobal.delete(name);
        //remove element from array
        delete annotated['global'][tokenContent];
        handleLinkedTokens(setBasicColor);
    }

    populateTable2();


    /*console.log('ABOVE SWITCH STATEMENT ' + source);
    switch (source) {
        case 'Concatenated':
            populateTable(concatenatedResults, 'Concatenated');
            console.log('OPTION: CONCATENATED');
            break;
        case 'Wikidata':
            populateTable(wikidataResults, 'Wikidata');
            console.log('OPTION: WIKDIATA');
            break;
        case 'WordWindow':
            populateTable(wordWindow, 'WordWindow');
            console.log('OPTION: WORD WINDOW');
            break;
        case 'ArXiv':
            populateTable(arXivEvaluationItems, 'ArXiv');
            console.log('OPTION: arXiv');
            break;
        case 'Wikipedia':
            populateTable(wikipediaEvaluationItems, 'Wikipedia');
            console.log('OPTION: Wikipedia');
            break;
    }*/




    function addToAnnotated(id, global=true) {

        //console.log('ADD TO ANNOTATED!');


        if (!global) {
            //annotated['local'][tokenContent] = {
            annotated['local'][tokenContent] = {
            'name': name,
            //'wikidataInf': wikidataReference[qid],
            'uniqueID': [id],
            'mathEnv': mathEnv
            }
        } else if (tokenContent in annotated['global']) {
            annotated['global'][tokenContent]['uniqueIDs'].push(id);
        } else {
            annotated['global'][tokenContent] = {
            'name': name,
            //'wikidataInf': wikidataReference[qid],
            'uniqueIDs': [id]
            };
        }
    }
    fillAnnotationsTable();
}





function handleLinkedTokens(func) {
    /*
    This function is used to annotate, mark the identical tokens in the document.
    i.e. if a word, identifier, formula is marked by the user, then all other
    occurences of the same token are marked accross the entire document.
    This function takes a function f as argument, since a lot of differnen functions need this
    functionality.
     */

    //console.log('linkedWords: ', linkedWords);
    //console.log('linkedMathSymbols: ', linkedMathSymbols);


    console.log('in handleLinkedTokens ' + tokenType);

    if (tokenType == 'Word') {
        dicToCheck = linkedWords;
    }
    else {
        dicToCheck = linkedMathSymbols;
    }

    if (tokenContent in dicToCheck) {
        console.log(tokenContent +  ' in linkedMathSymbols');
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
    console.log('RadioButtonClicked ' + option);
    switch (String(option)) {
        case 'Concatenated':
            populateTable(concatenatedResults, 'Concatenated');
            console.log('OPTION: CONCATENATED');
            break;
        case 'Wikidata':
            populateTable(wikidataResults, 'Wikidata');
            console.log('OPTION: WIKDIATA');
            break;
        case 'WordWindow':
            populateTable(wordWindow, 'WordWindow');
            console.log('OPTION: WORD WINDOW');
            break;
        case 'arXiv':
            populateTable(arXivEvaluationItems, 'arXiv');
            console.log('OPTION: arXiv');
            break;
        case 'Wikipedia':
            populateTable(wikipediaEvaluationItems, 'Wikipedia');
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
    console.log('LINKED MATH SYMBOLS: ',linkedMathSymbols);
}


function handlefileName(fileName) {
    window.fileName = fileName;
    //console.log(fileName);
}


function fillAnnotationsTable(){
    var breaks = "</br>";
    var annotationsTable= breaks + "<table><tr><td>Token</td><td>Annotated with</td><td>Type</td></tr>";

    function fill(d, type){
        for (var token in d){
            var item = d[token];
            var name = item['name'];
            annotationsTable+="<tr><td>" + token + "</td><td>" + name + "</td><td>" + type + "</td></tr>";
        }
    }

    fill(annotated['global'], 'Global');
    fill(annotated['local'], 'Local');


    //console.log(annotatedGLobal);
    //console.log(tokenAssignedItemGlobal)
    //annotationsTable += breaks;
    document.getElementById("annotationsHolder").innerHTML = annotationsTable;
    //document.getElementById("annotationsHolder").style.color = "red";
}

function handleAnnotations(existing_annotations){
    //console.log(typeof(existing_annotations));
    json = JSON.parse(existing_annotations)['existingAnnotations'];
    if (json != null){

        console.log(existing_annotations);

        //var existingAnnotationsGlobal = JSON.parse(existing_annotations)['existingAnnotations']['global'];
        //var existingAnnotationsLocal = JSON.parse(existing_annotations)['existingAnnotations']['local'];
        //console.log('Existing annotations: ', existingAnnotations);
        var existingAnnotationsGlobal = json['global'];
        var existingAnnotationsLocal = json['local'];

        for (var token in existingAnnotationsGlobal){
            var item = existingAnnotationsGlobal[token];
            var name = item['name'];
            annotated['global'][token] = item;
            tokenAssignedItemGlobal.add(name);
        }

        for (var token in existingAnnotationsLocal){
            var item = existingAnnotationsLocal[token];
            var name = item['name'];
            annotated['local'][token] = item;
            tokenAssignedItemLocal.add(name);
        }


        function colourExisting(ann){
            for (identifier in ann) {
                ids = ann[identifier]['uniqueIDs'];
                for (id in ids) {
                    setAnnotatedColor(ids[id]);
                }
            }
        }

        colourExisting(existingAnnotationsGlobal);
        colourExisting(existingAnnotationsLocal);

        fillAnnotationsTable();

    }

}


/*
AJAX FUNCTIONS USED TO POST THE REQUEST BACK TO DJANGO, WHERE THE WIKIDATA SPARQL QUERY IS EXECUTED
 */

function clickToken(jsonContent, tokenUniqueId, tokenType, jsonMathEnv, tokenHighlight) {
    /*
    This function is called when the user mouse clicks a token (identifier, formula, named entity or any other word).
    The popup modal is opened, an post request is made to the backend to retreive suggestions for the selected token,
    and the table is rendered with the correct search results.
     */


    //Display the selected token.
    //If the clicked token is the delimiter of a math environment (entire formula), the presented text will be the
    //string for the entire math environment and not the delimiter.

    var content = JSON.parse(jsonContent)['content'];
    var mathEnv = JSON.parse(jsonMathEnv)['math_env'];


    console.log(tokenUniqueId);

    //document.getElementById(tokenUniqueId).style.color = annotatedColor;
    //document.getElementById('2---2').style.color = identifierColorBasic;


    if (tokenType != 'Formula') {
        var fillText = content
    }
    else {
        var fillText = mathEnv;
    }
    //document.getElementById("highlightedText").innerHTML = fillText;

    console.log(fillText);


    //hide both buttons for math environments
    /*if (tokenType == 'Identifier' || tokenType == 'Formula') {
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

    //check wikidata option (default)
    if (tokenType == 'Word'){
        document.getElementById("wikidataBtn").checked = true;
    }
    else {
        document.getElementById("concatenatedLabel").checked = true;
    }*/


    //Not the best way of doing this
    //https://stackoverflow.com/questions/5786851/define-global-variable-in-a-javascript-function
    window.uniqueID = tokenUniqueId;
    //window.tokenContent = tokenContent;
    window.tokenContent = content;
    window.tokenType = tokenType;
    window.mathEnv = mathEnv;

    console.log('Content: ' +  content);

    let data_dict = { the_post : $("#" + tokenUniqueId).val(),
                  'csrfmiddlewaretoken': getCookie("csrftoken"),
                  'queryDict': content,
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


          /*window.concatenatedResults = json['concatenatedResults'];
          window.wikidataResults = json['wikidataResults'];
          window.arXivEvaluationItems = json['arXivEvaluationItems'];
          window.wikipediaEvaluationItems = json['wikipediaEvaluationItems'];
          window.wordWindow = json['wordWindow'];*/

          window.jsonResults = json;

          switch (tokenType) {
              case 'Identifier':
                  populateTable2();
                  break;
          }


          /*switch (tokenType) {
              case 'Identifier':
                  console.log('Identifier');
                  document.getElementById("concatenatedLabel").hidden = false;
                  document.getElementById("wordWindowLabel").hidden = false;
                  document.getElementById("arXivLabel").hidden = false;
                  document.getElementById("wikipediaLabel").hidden = false;
                  document.getElementById("concatenatedBtn").checked = true;
                  populateTable(concatenatedResults, 'Concatenated');
                  break;
              case 'Word':
                  console.log('Word');
                  document.getElementById("concatenatedLabel").hidden = true;
                  document.getElementById("wordWindowLabel").hidden = true;
                  document.getElementById("arXivLabel").hidden = true;
                  document.getElementById("wikipediaLabel").hidden = true;
                  document.getElementById("wikidataBtn").checked = true;
                  populateTable(wikidataResults, 'Wikidata');
                  break;
              case 'Formula':
                  console.log('Formula');
                  document.getElementById("concatenatedLabel").hidden = false;
                  document.getElementById("wordWindowLabel").hidden = false;
                  document.getElementById("arXivLabel").hidden = true;
                  document.getElementById("wikipediaLabel").hidden = true;
                  document.getElementById("concatenatedBtn").checked = true;
                  populateTable(concatenatedResults, 'Concatenated');
                  break;
          }*/
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
    var fileNameDict = {'f': fileName};
    function create_post() {
      let data_dict = { the_post : $('#post-text').val(),
                        //'csrfmiddlewaretoken': '{{ csrf_token }}',
                        'csrfmiddlewaretoken': getCookie("csrftoken"),
                        'marked': $.param(marked),
                        'annotated': $.param(annotated),
                        'annotatedLocal': $.param(annotated['local']),
                        'unmarked': $.param(unmarked),
                        'fileName': $.param(fileNameDict)
                        };

      console.log(annotated);


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
              $('#results').html("<div class='alert-box alert radius' data-alert>error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); //add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); //more information about error
          }
      });
    }
});
