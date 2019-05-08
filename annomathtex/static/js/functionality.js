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
// source: [nrow, ...]
// e.g.: 'arXiv': [0,4,2,...]

var tokenAssignedItemGlobal = {};
//var tokenAssignedItemLocal = new Set([]);

var cellColorBasic = '#dddddd';
var cellColorSelectedGlobal = 'pink';
var cellColorSelectedLocal = 'blue';

var identifierColorBasic = '#c94f0c';
var formulaColorBasic = '#ffa500';
var annotatedColor = '#04B404';
var noMatchIdentifierColor = '#2b332f';

var nmStr = 'NOMATCH';
var blockMatch = false;

//var identifierColorAnnotated = '#F88000';
var cellCounter = 0;


function createCell(item, source, rowNum) {
    var name = item['name'];
    var backgroundColor = cellColorBasic;
    var containsHighlightedName = false;
    if (tokenContent in tokenAssignedItemGlobal && tokenAssignedItemGlobal[tokenContent] == name){
        backgroundColor = cellColorSelectedGlobal;
        containsHighlightedName = true;

    } else if (tokenContent in annotated['local']) {
        if (uniqueID in annotated['local'][tokenContent]) {
            if (annotated['local'][tokenContent][uniqueID]['name'] == name) {
                backgroundColor = cellColorSelectedLocal;
            } else {
                //delete annotated['local'][tokenContent];
                backgroundColor = cellColorBasic;
            }
        }
    }
    var qid = '';
    var cellID = "cell" + source + rowNum;
    var args = [
        name,
        qid,
        source,
        backgroundColor,
        cellID,
        containsHighlightedName,
        rowNum
    ];


    if (name in sourcesWithNums){
        sourcesWithNums[name][source] = rowNum;
    } else {
        sourcesWithNums[name] = {};
        sourcesWithNums[name][source] = rowNum;
    }


    //not possible to pass multiple arguments, that's why they are concatenated to one argument string
    var argsString = args.join('---');

    var td = "<td id=" + cellID;
    td += " style='background-color:" + backgroundColor + "'";
    td += "onclick='selected(\"" + argsString + "\")' >";
    //td += "<div onclick='selectedDouble()'>";
    td += name;
    //td += "</div>";
    td += "</td>";

    return td;
}


function checkNoMatch() {
    var g = annotated['global'];
    var l = annotated['local'];

    if (tokenContent in g) {
        if (g[tokenContent]['name'] == nmStr) {
            return true;
        }
    }
    if (tokenContent in l){
        if (uniqueID in l[tokenContent]){
            if (l[tokenContent][uniqueID]['name'] == nmStr) {
                return true;
            }
        }
    }
    return false;
}

function populateTable(random=true) {

    if (blockMatch){
        document.getElementById('noMatch').style.color = cellColorSelectedGlobal;
    } else {
        document.getElementById('noMatch').style.color = 'black';
    }


    window.sourcesWithNums = {};
    //console.log(sourcesWithNums);

    arXivEvaluationItems = jsonResults['arXivEvaluationItems'];
    wikipediaEvaluationItems = jsonResults['wikipediaEvaluationItems'];
    wikidataResults = jsonResults['wikidataResults'];
    wordWindow = jsonResults['wordWindow'];

    var resultList = [[arXivEvaluationItems, 'ArXiv'],
                      [wikipediaEvaluationItems, 'Wikipedia'],
                      [wikidataResults, 'Wikidata'],
                      [wordWindow, 'WordWindow']];

    var table= "<table><tr><td>Source 0</td><td>Source 1</td><td>Source 2</td><td>Source 3</td></tr>";

    if (preservedResultList != null) {
        resultList = preservedResultList;
    } else if (random) {
        resultList = shuffle([[arXivEvaluationItems, 'ArXiv'],
                                    [wikipediaEvaluationItems, 'Wikipedia'],
                                    [wikidataResults, 'Wikidata'],
                                    [wordWindow, 'WordWindow']]);
        var table= "<table><tr><td>Source 0</td><td>Source 1</td><td>Source 2</td><td>Source 3</td></tr>";
    }

    preservedResultList = resultList;


    var source0 = resultList[0][0];
    var source1 = resultList[1][0];
    var source2 = resultList[2][0];
    var source3 = resultList[3][0];

    var name0 = resultList[0][1];
    var name1 = resultList[1][1];
    var name2 = resultList[2][1];
    var name3 = resultList[3][1];


    for (i = 0; i<10; i++) {
        if (source0.length >= i && source0.length > 0){
            var tdSource0 = createCell(source0[i], name0, i);
        }
        if (source1.length >= i && source1.length > 0) {
            var tdSource1 = createCell(source1[i], name1, i);
        }
        if (source2.length >= i && source2.length > 0) {
            var tdSource2 = createCell(source2[i], name2, i);
        }
        if (source3.length >= i && source3.length > 0) {
            var tdSource3 = createCell(source3[i], name3, i);
        }
        var tr = '<tr>' + tdSource0 + tdSource1 + tdSource2 + tdSource3 + '</tr>';
        table += tr;

    }


    document.getElementById('tableholder').innerHTML = table;
    var modal = document.getElementById("popupModal");
    modal.style.display = "block";

    var span = document.getElementById("span");
    span.onclick = function () {
      modal.style.display = "none";
      preservedResultList = null;
    };

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
        preservedResultList = null;
      }
    };
}


function setAnnotatedColor(id) {
    try {
        document.getElementById(id).style.color = annotatedColor;
    } catch (e) {
        //console.log(e);
        console.log('error: ' + id);

    }
}

function setBasicColor(id) {
    if (tokenType == 'Identifier') {
        document.getElementById(id).style.color = identifierColorBasic;
    } else if (tokenType == 'Formula'){
        document.getElementById(id).style.color = formulaColorBasic;
    }
}


function handleNoMatch(){
    if (document.getElementById('noMatch').style.color == 'black') {
        console.log('true');
        document.getElementById('noMatch').style.color = cellColorSelectedGlobal;
        //document.getElementById(uniqueID).style.color = noMatchIdentifierColor;
        blockMatch = true;
        var local = document.getElementById('localSwitch').checked;
        if (local) {
            if (tokenContent in annotated['local']){
                annotated['local'][tokenContent][id] = {
                    'name': nmStr,
                    'mathEnv': '',
                    'source': '',
                    'rowNum': '',
                    'sourcesWithNums': {}
                }
            } else {
                annotated['local'][tokenContent] = {};
                annotated['local'][tokenContent][nmStr] = {
                    'name': nmStr,
                    'mathEnv': '',
                    'source': '',
                    'rowNum': '',
                    'sourcesWithNums': {}
                }
            }
        } else {
            annotated['global'][tokenContent] = {
            'name': nmStr,
            //'wikidataInf': wikidataReference[qid],
            'uniqueIDs': [],
            'sourcesWithNums': {}
            };
        }

    }
    else {
        console.log('else');
        document.getElementById('noMatch').style.color = 'black';
        //document.getElementById(uniqueID).style.color = identifierColorBasic;
        blockMatch = false;

        var g = annotated['global'];
        var l = annotated['local'];

        if (tokenContent in g) {
            if (g[tokenContent]['name'] == nmStr) {
                console.log('delete');
                delete annotated['global'][tokenContent];
            }
        }
        if (tokenContent in l){
            if (uniqueID in l[tokenContent]){
                if (l[tokenContent][uniqueID]['name'] == nmStr) {
                    delete annotated['local'][tokenContent][uniqueID];
                }
            }
        }
    }
    populateTable();
    fillAnnotationsTable();

}


function selected(argsString){
    /*
    This function is called when the user annotates a token with an element from the created table (e.g. from the
    retrieved wikidata results).
     */

    if (blockMatch) {
        alert('No Match selected');
        return;
    }

    var argsArray = argsString.split('---');
    var name = argsArray[0];
    var qid = argsArray[1];
    var source = argsArray[2];
    var backgroundColor = argsArray[3];
    var cellID = argsArray[4];
    var containsHighlightedName = (argsArray[5] === 'true');
    var rowNum = argsArray[6];

    var local = document.getElementById('localSwitch').checked;

    if (local) {

        //local annotations
        if (backgroundColor == cellColorBasic) {
            //make local annotation
            document.getElementById(cellID).style.backgroundColor = cellColorSelectedLocal;
            //tokenAssignedItemLocal.add(name);
            addToAnnotated(uniqueID, false);
            console.log(annotated);
            setAnnotatedColor(uniqueID);
        } else if (backgroundColor == cellColorSelectedLocal) {
            //reverse local annotation
            document.getElementById(cellID).style.backgroundColor = cellColorBasic;
            //tokenAssignedItemLocal.delete(name);
            delete annotated['local'][tokenContent][uniqueID];
        }
    } else {
        //global annotations
        if (backgroundColor == cellColorBasic) {
            //make global annotation
            document.getElementById(cellID).style.backgroundColor = cellColorSelectedGlobal;
            tokenAssignedItemGlobal[tokenContent] = name;
            setAnnotatedColor(uniqueID);
            //delete any existing global annotation for this identifier and concept
            //use case: changing the selected annotation
            if (tokenContent in annotated['global']) {
                console.log('Changing annotation...');
                delete annotated['global'][tokenContent];
            }
            handleLinkedTokens(addToAnnotated);
            handleLinkedTokens(setAnnotatedColor);
            console.log('adding to annotated ' + name);

            console.log(annotated);

            //document.getElementById('284---4').style.color = annotatedColor;

        } else if(backgroundColor == cellColorSelectedGlobal) {
            //reverse global annotation
            document.getElementById(cellID).style.backgroundColor = cellColorBasic;
            setBasicColor(uniqueID);
            delete tokenAssignedItemGlobal[tokenContent];
            delete annotated['global'][tokenContent];
            handleLinkedTokens(setBasicColor);
        }
    }



    populateTable();


    function addToAnnotated(id, global=true) {

        if (!global) {

            if (tokenContent in annotated['local']){
                annotated['local'][tokenContent][id] = {
                    'name': name,
                    'mathEnv': mathEnv,
                    'source': source,
                    'rowNum': rowNum,
                    'sourcesWithNums': sourcesWithNums[name]
                }
            } else {
                annotated['local'][tokenContent] = {};
                annotated['local'][tokenContent][id] = {
                    'name': name,
                    'mathEnv': mathEnv,
                    'source': source,
                    'rowNum': rowNum,
                    'sourcesWithNums': sourcesWithNums[name]
                }
            }

            console.log(annotated['local']);
        } else if (tokenContent in annotated['global']) {
            annotated['global'][tokenContent]['uniqueIDs'].push(id);
        } else {
            annotated['global'][tokenContent] = {
            'name': name,
            //'wikidataInf': wikidataReference[qid],
            'uniqueIDs': [id],
            'sourcesWithNums': sourcesWithNums[name]
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
        //console.log(word);
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




function linkTokens(linked_words, linked_math_symbols) {
    /*
    Linked tokens are stored in a variable, to enable only having to annotate an identifier, word, formula once for
    entire document.
     */
    window.linkedWords = JSON.parse(linked_words)['linkedWords'];
    window.linkedMathSymbols = JSON.parse(linked_math_symbols)['linkedMathSymbols'];
    //console.log('LINKED MATH SYMBOLS: ',linkedMathSymbols);
}


function handlefileName(fileName) {
    window.fileName = fileName;
    //console.log(fileName);
}


function fillAnnotationsTable(){

    console.log('')

    var breaks = "</br>";
    var annotationsTable= breaks + "<table><tr><td>Token</td><td>Annotated with</td><td>Type</td></tr>";

    function fill(d, type){
        for (var token in d){
            var item = d[token];
            var name = item['name'];
            annotationsTable+="<tr><td>" + token + "</td><td>" + name + "</td><td>" + type + "</td></tr>";
        }
    }


    function fillLocal(d, type){
        for (var token in d){
            for (var uID in d[token]){
                var dict = d[token][uID];
                var name = dict['name']
                annotationsTable+="<tr><td>" + token + "</td><td>" + name + "</td><td>" + type + "</td></tr>";
            }

        }
    }

    fill(annotated['global'], 'Global');
    fillLocal(annotated['local'], 'Local');
    document.getElementById("annotationsHolder").innerHTML = annotationsTable;
}

function handleAnnotations(existing_annotations){
    json = JSON.parse(existing_annotations)['existingAnnotations'];
    if (json != null){

        var existingAnnotationsGlobal = json['global'];
        var existingAnnotationsLocal = json['local'];

        for (var token in existingAnnotationsGlobal){
            var item = existingAnnotationsGlobal[token];
            var name = item['name'];
            annotated['global'][token] = item;
            //tokenAssignedItemGlobal.add(name);
            tokenAssignedItemGlobal[token] = name;
        }

        for (var token in existingAnnotationsLocal){
            var item = existingAnnotationsLocal[token];
            var name = item['name'];
            annotated['local'][token] = item;
            //tokenAssignedItemLocal.add(name);
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

    if (tokenType != 'Formula') {
        var fillText = content
    }
    else {
        var fillText = mathEnv;
    }
    document.getElementById("highlightedText").innerHTML = fillText;


    //Not the best way of doing this
    //https://stackoverflow.com/questions/5786851/define-global-variable-in-a-javascript-function
    window.uniqueID = tokenUniqueId;
    //window.tokenContent = tokenContent;
    window.tokenContent = content;
    window.tokenType = tokenType;
    window.mathEnv = mathEnv;
    window.preservedResultList = null;


    if (checkNoMatch()){
        blockMatch = true;
    } else {
        blockMatch = false;
    }

    //console.log('Content: ' +  content);

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


          window.jsonResults = json;

          switch (tokenType) {
              case 'Identifier':
                  populateTable();
                  break;
          }


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
                        //'annotatedLocal': $.param(annotated['local']),
                        'unmarked': $.param(unmarked),
                        'fileName': $.param(fileNameDict)
                        };

      //console.log(annotated);


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
