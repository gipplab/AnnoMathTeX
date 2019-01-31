
/*
FUNCTIONALITY USED TO SEND THE INFORMATION ABOUT ANNOTATIONS AND HIGHLIGHTING BACK TO DJANGO
 */





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
    };

});
