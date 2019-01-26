//better way to get the type of object
var toType = function(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
}

var highlightedIDs = [];

function alertthis(unique_id, wikidata_result) {
    //Not the best way of doing this
    //https://stackoverflow.com/questions/5786851/define-global-variable-in-a-javascript-function
    window.uniqueID = unique_id;
    //highlightedIDs.push(unique_id);

    if (wikidata_result != "None") {
      var json = JSON.parse(wikidata_result);
      alert(json['w'][0]['qid']);
    }
    //alert(wikidata_result != "None");

    var modal = document.getElementById("foo");
    modal.style.display = "block";

    var span = document.getElementById("span");
    span.onclick = function () {
      modal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
    return;
  }

function highlightToken() {
    document.getElementById(uniqueID).style.color = 'blue';
    highlightedIDs.push(uniqueID);
    //document.getElementById("placeholder").innerHTML += uniqueID;
    console.log(highlightedIDs);
    updateData();
    return;
}

function unHighlightToken() {
    var index = highlightedIDs.indexOf(uniqueID);
    if (index > -1) {
      highlightedIDs.splice(index, 1);
      document.getElementById(uniqueID).style.color = 'black';
    }
    console.log(highlightedIDs);
    updateData();
    return
}

function updateData(){
    //TODO
    document.getElementById("test").innerHTML = highlightedIDs;
    return;
}

// AJAX for posting
function create_post() {
      console.log("create post is working!") // sanity check
      var data_dict = { the_post : $('#post-text').val(), 'csrfmiddlewaretoken': '{{ csrf_token }}', 'valuepass':42 };
      $.ajax({
          url : "file_upload/", // the endpoint
          type : "POST", // http method
          data : data_dict, // data sent with the post request

          // handle a successful response
          success : function(json) {
              $('#post-text').val(''); // remove the value from the input
              console.log(json); // log the returned json to the console
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

$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log('form submitted');
    create_post();
});
