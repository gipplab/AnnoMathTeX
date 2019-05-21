var cellColorBasic = '#dddddd';
var cellColorSelectedGlobal = 'pink';
var cellColorSelectedLocal = 'blue';

var identifierColorBasic = '#c94f0c';
var formulaColorBasic = '#ffa500';
var annotationsColor = '#04B404';


/*
Setting colours
 */

function setAnnotatedColor(uIDs) {
    /*
    Set the color of annotations tokens.
     */

    for (var i=0 in uIDs) {
        document.getElementById(uIDs[i]).style.color = annotationsColor;
    }
}

function setBasicColor(uIDs) {
    /*
    Set the color of tokens back to basic, if the user changed his mind.
     */
    console.log(uIDs);
    for (var i=0 in uIDs) {
        document.getElementById(uIDs[i]).style.color = identifierColorBasic;
    }
}

function setCellColorBasic(cellID) {
    document.getElementById(cellID).style.backgroundColor = cellColorBasic;
}

function setCellColorSelectedLocal(cellID) {
    document.getElementById(cellID).style.backgroundColor = cellColorSelectedLocal;
}

function setCellColorSelectedGlobal(cellID) {
    document.getElementById(cellID).style.backgroundColor = cellColorSelectedGlobal;
}


/*
Rendering of table in popup modal
 */

function populateTable(random=false) {
    /*
    The entire table, containing the recommendations, that is shown to the user in the popup modal is created as html
    code in this function. The function createCell() is called upon, to create the individual cells in the table.

    random: The sources are shuffled and anonymized (The user does not know which recommendations come from which
    source, which is important for the evaluation)
     */

    sourcesWithNums = {};

    arXivEvaluationItems = recommendations['arXivEvaluationItems'];
    wikipediaEvaluationItems = recommendations['wikipediaEvaluationItems'];
    wikidataResults = recommendations['wikidataResults'];
    wordWindow = recommendations['wordWindow'];

    var resultList = [[arXivEvaluationItems, 'ArXiv'],
                      [wikipediaEvaluationItems, 'Wikipedia'],
                      [wikidataResults, 'Wikidata'],
                      [wordWindow, 'WordWindow']];

    if (preservedResultList) {
        resultList = preservedResultList;
    } else if (random) {
        resultList = shuffle([[arXivEvaluationItems, 'ArXiv'],
                                    [wikipediaEvaluationItems, 'Wikipedia'],
                                    [wikidataResults, 'Wikidata'],
                                    [wordWindow, 'WordWindow']]);
        var table= "<table><tr><td>Source 1</td><td>Source 2</td><td>Source 3</td><td>Source 4</td></tr>";
    } else {
        var table= "<table><tr><td>arXiv</td><td>Wikipedia</td><td>Wikidata</td><td>WordWindow</td></tr>";
    }


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

function createCell(item, source, rowNum) {
    /*
    The cells, that populate the table in the popup modal are created in this method.
     */
    var name = item['name'];
    var backgroundColor = cellColorBasic;
    var containsHighlightedName = false;
    if (tokenContent in annotations['global']) {
        if (annotations['global'][tokenContent]['name'] == name) {
            backgroundColor = cellColorSelectedGlobal;
            containsHighlightedName = true;
        }

    } else if (tokenContent in annotations['local']) {
        if (uniqueID in annotations['local'][tokenContent]) {
            if (annotations['local'][tokenContent][uniqueID]['name'] == name) {
                backgroundColor = cellColorSelectedLocal;
            } else {
                backgroundColor = cellColorBasic;
            }
        }
    }
    rowNum += 1;
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
    td += name;
    td += "</td>";

    return td;
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
    var rowNum = argsArray[6];

    var local = document.getElementById('localSwitch').checked;

    if (local) {
        //local annotations
        switch (backgroundColor) {
            case cellColorBasic:
                //make local annotation
                //todo: is case that user changes his mind covered?
                setCellColorSelectedLocal(cellID);
                addToAnnotations(uniqueID, name, source, rowNum);
                setAnnotatedColor([uniqueID]);
                break;
            case cellColorSelectedLocal:
                //reverse local annotation
                console.log('set cell col basic');
                setCellColorBasic(cellID);
                setBasicColor([uniqueID]);
                deleteLocalAnnotation(tokenContent, uniqueID);
                console.log(annotations);
                break;
        }

    } else {
        //global annotations

        switch (backgroundColor) {
            case cellColorBasic:
                setCellColorSelectedGlobal(cellID);
                //tokenAssignedItemGlobal[tokenContent] = name;

                if (tokenContent in annotations['global']) {
                    deleteGlobalAnnotation(tokenContent);
                }

                var uIDs = getLinkedIDs(tokenContent);
                addToAnnotations(uniqueID, name, source, rowNum, false, uIDs);
                setAnnotatedColor(uIDs);
                break;

            case cellColorSelectedGlobal:
                setCellColorBasic(cellID);
                var uIDs = annotations['global'][tokenContent]['uniqueIDs'];
                setBasicColor(uIDs);
                deleteGlobalAnnotation(tokenContent);
                break;
        }
    }
    populateTable();
    renderAnnotationsTable();
}







function renderAnnotationsTable() {
    /*
    The table at the top of the document, that is constantly being updated with the latest annotations is generated in
    this function.
     */

    function createRow(token, name, local, uIDs) {
        var args = [
                token,
                local,
                uIDs
            ];
        var type = local ? 'Local' : 'Global';
        var argsString = args.join('----');
        var tr ="<tr><td>" + token + "</td><td>" + name + "</td><td>" + type + "</td>";
        tr += "<td onclick='deleteFromAnnotations(\"" + argsString + "\")'>x</td></tr>";
        return tr;
    }

    var annotationsTable = "</br><table><tr><td>Token</td><td>Annotated with</td><td>Type</td><td>Delete</td></tr>";

    var l = annotations['local'];
    for (var token in l) {
        for (var uID in l[token]){
            tr = createRow(token, l[token][uID]['name'], true, [uID]);
            annotationsTable += tr;
        }
    }

    var g = annotations['global'];
    for (var token in g) {
        tr = createRow(token, g[token]['name'], false, g[token]['uniqueIDs']);
        annotationsTable += tr;
    }

    document.getElementById("annotationsHolder").innerHTML = annotationsTable;
}
