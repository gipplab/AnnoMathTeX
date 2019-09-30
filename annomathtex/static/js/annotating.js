function noMatchInputListener() {
    /*
    Starts the timer when the user starts inputting a manual recommendation
     */

    window.manualRecommendationStartTime = Date.now();
    window.manualSelectionTime = Date.now() - window.tokenClickedTime;
    //var manualRecommendationStartTime = Date.now();
    //console.log(manualRecommendationStartTime);
}


function handleNoMatch(){
    /*
    The user did not find any of the recommendations to be fitting and added his own suggestion.
    This means that this information has to be added to the "annotations" dictionary, which will later be written to the
    evaluation csv file, along with the other annotations.
     */

    let manualRecommendationsSubmitTime = Date.now() - window.manualRecommendationStartTime;
    var name = document.getElementById('noMatchInput').value;
    var uIDs = getLinkedIDs(content);

    addToAnnotations(uniqueID, name, 'user', '-', 'N/A', manualRecommendationsSubmitTime, manualSelectionTime, true, uIDs);
    addToMannualRecommendations(name);
    var local = document.getElementById('localSwitch').checked;

    if (local) {
        setAnnotatedColor([uniqueID]);
    } else {
        setAnnotatedColor(uIDs);
    }

    handlePopupTable();
    renderAnnotationsTable();
}


function addToMannualRecommendations(name) {



    if (content in manualRecommendations) {
        manualRecommendations[content].push({'name': name, 'qid': 'N/A'});
    } else {
        manualRecommendations[content] = [{'name': name, 'qid': 'N/A'}];
    }

}


function addToAnnotations(uID, name, source, rowNum, qid, selectionTime, manualSelectionTime=-1000, noMatch=false, uIDs = null) {
    /*
    manualSelectionTime: the time from when the token was clicked until MANUAL INSERTION was selected
    (only for manual annotation)

    An annotation was made and the information is added to the annotations dictionary
     */
    if (isFormula) {
        var type = 'Formula';
    } else {
        var type = 'Identifier';
    }

    console.log(uIDs);

    function localDict() {
        return {
                'name': name,
                'mathEnv': mathEnv,
                'source': source,
                'rowNum': rowNum,
                'qid': qid,
                'time': selectionTime,
                'manualSelectionTime': manualSelectionTime,
                'sourcesWithNums': noMatch ? {} : sourcesWithNums[name],
                'type': type //identifier or formula
            };
    }

    var local = document.getElementById('localSwitch').checked;
    if (local) {
        if (content in annotations['local']){
            annotations['local'][content][uID] = localDict();
        } else {
            annotations['local'][content] = {};
            annotations['local'][content][uID] = localDict();
        }
    } else {

        //console.log(content);

        //todo: unify with function localDict()
        annotations['global'][content] = {
        'name': name,
        'mathEnv': mathEnv,
        'uniqueIDs': uIDs,
        'qid': qid,
        'time': selectionTime,
        'manualSelectionTime': manualSelectionTime,
        'sourcesWithNums': noMatch ? {} : sourcesWithNums[name],
        'type': type
        };
        //annotations['global'][content] = {localDict};
    }
}




function deleteLocalAnnotation(token, uID) {
    delete annotations['local'][token][uID];
}

function deleteGlobalAnnotation(token) {
    delete annotations['global'][token];
}

function deleteFromAnnotations(argsString) {

    var argsArray = argsString.split('----');
    console.log(argsArray);

    var token = argsArray[0];
    var local = (argsArray[1] == 'true');
    var uIDs = argsArray[2].split(',');
    if (local) {
        deleteLocalAnnotation(token, uIDs[0]);
        setBasicColor(uIDs);
    } else {
        deleteGlobalAnnotation(token);
        setBasicColor(uIDs);
    }

    renderAnnotationsTable();
}




function handleExistingAnnotations(existing_annotations) {
    /*
    If any previous annotations for the same document exist, a number of actions are made:
        - The annotations are added to the dictionary "annotations".
        - The table at the top of the document containing the current annotations is filled with the existing ones.
        - The tokens that were annotated are colored accordingly.
     */
    //annotations = JSON.parse(existing_annotations)['existingAnnotations'];
    tmp = JSON.parse(existing_annotations)['existingAnnotations'];
    annotations = JSON.parse(tmp);
    if (annotations) {
        uIDs = getLocalUniqueIDs().concat(getGlobalUniqueIDs());
        setAnnotatedColor(uIDs);
        renderAnnotationsTable();
    } else {
        annotations = {};
    }

    console.log(typeof annotations);
    console.log(typeof existing_annotations);

    if ('global' in annotations) {
        var g = true;
    } else {
        var g = false;
    }

    if ('local' in annotations) {
        var l = true;
    } else {
        var l = false;
    }

    if (!g) {
        annotations['global'] = {};
    }

    if (!l) {
        annotations['local'] = {};
    }

}

