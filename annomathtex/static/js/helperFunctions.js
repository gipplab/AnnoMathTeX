/*
This file contains helper functions that are used by the script functionality.js
 */

//function to format strings
//https://coderwall.com/p/flonoa/simple-string-format-in-javascript
String.prototype.format = function() {
    a = this;
    for (k in arguments) {
      a = a.replace("{" + k + "}", arguments[k])
    }
    return a
};

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
 }


//from: https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

//https://stackoverflow.com/questions/1144783/how-to-replace-all-occurrences-of-a-string-in-javascript
function replaceAllEqualsPlusAnn(ann) {
    /*
    This function is called from posting.js
    It replaces all equals and plus signs in the annotations that the user made. This is necessary, because Django can't
    recognise equals and plus signs when receiving an ajax post.
     */


    var newGlobal = {};
    var newLocal = {};

    function replaceAll(str) {
        //console.log(str, typeof str);
        var noEquals = str.replace(new RegExp('=', 'g'), '__EQUALS__');
        //var newStr = noEquals.replace(new RegExp('/\+/', 'g'), '__PLUS__');
        return noEquals;
    }

    //remove equals sign, becuase Django splits at equals sign
    for (var name in ann['global']) {
        var nameReplaced = replaceAll(name);
        newGlobal[nameReplaced] = ann['global'][name];
    }
    for (var name in ann['local']) {
        //for (var num in ann['local'])
        var nameReplaced = replaceAll(name);
        newLocal[nameReplaced] = ann['local'][name];
    }

    var newAnn = {'global': newGlobal, 'local': newLocal};

    return newAnn;

}

function replaceAllEqualsPlusManualRecommendations(manualRecommendations) {
    /*
    This function is called from posting.js
    It replaces all equals signs in the manual recommendations that the user made. This is necessary, because Django
    can't recognise equals signs when receiving an ajax post.
     */
    function replaceAll(str) {
        var noEquals = str.replace(new RegExp('=', 'g'), '__EQUALS__');
        //var newStr = noEquals.replace(new RegExp('/\+/', 'g'), '__EQUALS__');
        return noEquals;
    }

    newManualRecommendations = {};
    for (var identifierOrFormula in manualRecommendations) {
        var replaced = replaceAll(identifierOrFormula);
        newManualRecommendations[replaced] = manualRecommendations[identifierOrFormula];
    }
    return newManualRecommendations;

}



function getLocalUniqueIDs(){
    /*
    Get all the uniqueIDs for a certain token.
     */
    var uniqueIDs = [];
    for (var token in annotations['local']) {
        for (uniqueID in annotations['local'][token]) {
            uniqueIDs.push(uniqueID);
        }
    }
    return uniqueIDs;
}

function getGlobalUniqueIDs() {
    /*
    Get all the uniqueIDs for a certain token.
     */
    var uniqueIDs = new Array();
    for (var token in annotations['global']) {
        var tmpIDs = annotations['global'][token]['uniqueIDs'];
        uniqueIDs = uniqueIDs.concat(tmpIDs);
    }
    return uniqueIDs;
}


function getLinkedIDs(contentSymbol) {
    /*
    Get the uniqueIDs of all the identifiers/formulae that appear multiple times in the document. This allows for global
    annotating.
     */
    var uIDs = [];
    if (contentSymbol in linkedMathSymbols) {
        for (var i in linkedMathSymbols[contentSymbol]) {
            uIDs.push(linkedMathSymbols[contentSymbol][i]);
        }
    }
    return uIDs;
}


function ratioRemaining() {
    /*
    get the ratio of the remaining identifiers/formulae to be annotated
     */

    var annotatedFormulae = 0;
    var annotatedIdentifiers = 0;

    for (var ann in annotations['global']){
        let count = annotations['global'][ann]['uniqueIDs'].length;
        if (annotations['global'][ann]['type'] == 'Formula') {
            annotatedFormulae += count;
        } else {
            annotatedIdentifiers += count;
        }
    }

    for (var ann in annotations['local']) {
        for (var uid in annotations['local'][ann]) {
            if (annotations['local'][ann][uid]['type'] == 'Formula') {
                annotatedFormulae += 1;
            } else {
                annotatedIdentifiers += 1;
            }
        }
    }

    return [annotatedIdentifiers, annotatedFormulae/2];
}
