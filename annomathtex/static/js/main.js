/*
This file contains the functionality for the frontend of the project.
It is called in annotation_template.html.
*/

/*
The tokens (identifier, formula, word) that are annotated with an item from wikidata, the arXiv evaluation list, the
wikipedia evaluation list or the word window are stored in this dictionary. Upon saving, the dictionary is sent to the
backend for further processing (saving, writing to database).
 */
var tokenAssignedItemGlobal = {};



function handleLinkedTokens(func, dicToCheck) {
    /*
    This function is used to annotate, mark the identical tokens in the document.
    i.e. if a word, identifier, formula is marked by the user, then all other
    occurences of the same token are marked accross the entire document.
    This function takes a function f as argument, since a lot of differnen functions need this
    functionality.
     */

    if (tokenContent in dicToCheck) {
        console.log(tokenContent +  ' in linkedMathSymbols');
        var word = dicToCheck[tokenContent];
        for (i in word) {
            var id = word[i];
            func(id)
        }
    }
}






function clickToken(jsonContent, jsonMathEnv, tokenUniqueId, tokenType) {
    /*
    This function is called when the user mouse clicks a token (identifier, formula, named entity or any other word).
    The popup modal is opened, an post request is made to the backend to retreive suggestions for the selected token,
    and the table is rendered with the correct search results.
     */

    var content = JSON.parse(jsonContent)['content'];
    var mathEnv = JSON.parse(jsonMathEnv)['math_env'];

    //todo: unify content & tokenContent / tokenUniqueId & uniqueID
    tokenContent = content;
    uniqueID = tokenUniqueId;


    //Display the selected token in the element "highlightedText".
    //If the clicked token is the delimiter of a math environment (entire formula), the presented text will be the
    //string for the entire math environment and not the delimiter.
    if (tokenType != 'Formula') {
        var fillText = content
    }
    else {
        var fillText = mathEnv;
    }
    document.getElementById("highlightedText").innerHTML = fillText;



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

      //successful response
      success : function(json) {
          $("#" + tokenUniqueId).val(''); // remove the value from the input
          window.jsonResults = json;
          recommendations = json;
          switch (tokenType) {
              case 'Identifier':
                  populateTable();
                  break;
          }
      },

      //non-successful response
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>");
          console.log(xhr.status + ": " + xhr.responseText);
      }
    });
}
