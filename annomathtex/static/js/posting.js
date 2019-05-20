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

      $.ajax({
          url : "file_upload/", // the endpoint
          type : "POST", // http method
          data : data_dict, // data sent with the post request

          //successful response
          success : function(json) {
              $('#post-text').val(''); // remove the value from the input
          },

          //non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>");
              console.log(xhr.status + ": " + xhr.responseText);
          }
      });
    }
});



function getRecommendations(content, mathEnv, tokenType, tokenUniqueId) {
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
          return json;
      },

      //non-successful response
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>");
          console.log(xhr.status + ": " + xhr.responseText);
      }
    });
}
