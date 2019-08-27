

function getRepoContent() {


    console.log('getRepoCOntent');

    let data_dict = {'csrfmiddlewaretoken': getCookie("csrftoken"),
              'getRepoContent': ""
              };


    $.ajax(
        {
      url : '/file_upload_wiki_suggestions_2.html/', // the endpoint
      type : "POST", // http method
      data : data_dict, // data sent with the post request



      //successful response
      success : function(json) {
          console.log('success');
          console.log(json);
          renderRepoFileNames(json['fileNames']);
      },

      //non-successful response
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>");
          console.log(xhr.status + ": " + xhr.responseText);
      }
    });


    function renderRepoFileNames(fileNames) {
        var table = "<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" width=\"325\">";
        table += "<tr><td>";
        table += "<table cellspacing=\"0\" cellpadding=\"1\" border=\"1\" width=\"300\" >";
        table += "<tr style=\"color:white;background-color:grey\">";
        table += "<th>Existing Files</th>";
        table += "</tr></table></td></tr><tr><td>";
        table += "<div style=\"width:320px; height:80px; overflow:auto;\">";
        table += "<table cellspacing=\"0\" cellpadding=\"1\" border=\"1\" width=\"300\" >";

        for (var i in fileNames){
            let fileName = fileNames[i];
            table += "<tr><td type='submit' onclick='getWikipediaArticleFromRepo(\"" + fileName + "\")'>" + fileName + "</td></tr>";
        }

        //table += "<tr><td>new item</td></tr>";
        table += "</table></div></td></tr></table>";


        document.getElementById('tableholderW').innerHTML = table;
        var modal = document.getElementById("popupW");
        modal.style.display = "block";

        /*var span = document.getElementById("spanW");
        span.onclick = function () {
          modal.style.display = "none";
        };*/

        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };

    }

}


function getWikipediaArticleFromRepo(fileName) {
    console.log(fileName);

    let data_dict = {'csrfmiddlewaretoken': getCookie("csrftoken"),
              'wikipediaArticleName': fileName
              };


    $.ajax(
        {
      url : 'annotation/', // the endpoint
      type : "POST", // http method
      data : data_dict, // data sent with the post request



      //successful response
      success : function(json) {
          console.log('success!');
          document.location.href = '/test/';//'annotation_template_tmp.html';
      },

      //non-successful response
      error : function(xhr,errmsg,err) {
          $('#results').html("<div class='alert-box alert radius' data-alert>error: "+errmsg+
              " <a href='#' class='close'>&times;</a></div>");
          console.log(xhr.status + ": " + xhr.responseText);
      }
    });

}

