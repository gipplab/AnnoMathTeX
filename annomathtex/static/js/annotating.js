function handleNoMatch(){
    /*
    The "No Match" button was clicked: The user did not find any of the recommendations to be fitting.
    This means that this information has to be added to the "annotations" dictionary, which will later be written to the
    evaluation csv file, along with the other annotations.

    This method is also called if the user deselects the "No Match" button, i.e. if he found a matching recommendation
    after all.
     */

    var name = document.getElementById('noMatchInput').value;
    var uIDs = getLinkedIDs(tokenContent);
    addToAnnotations(uniqueID, name, 'user', '-', true, uIDs);
    addToMannualRecommendations(name);
    var local = document.getElementById('localSwitch').checked;

    if (local) {
        setAnnotatedColor([uniqueID]);
    } else {
        setAnnotatedColor(uIDs);
    }
    populateTable();
    renderAnnotationsTable();
}



function addToMannualRecommendations(name) {
    if (tokenContent in manualRecommendations){
        manualRecommendations[tokenContent].push({'name': name});
    } else {
        manualRecommendations[tokenContent] = [{'name': name}];
    }
}


function addToAnnotations(uID, name, source, rowNum, noMatch=false, uIDs = null) {



    function localDict() {
        return {
                'name': name,
                'mathEnv': mathEnv,
                'source': source,
                'rowNum': rowNum,
                'sourcesWithNums': noMatch ? {} : sourcesWithNums[name]
            };
    }

    var local = document.getElementById('localSwitch').checked;
    if (local) {
        if (tokenContent in annotations['local']){
            annotations['local'][tokenContent][uID] = localDict();
        } else {
            annotations['local'][tokenContent] = {};
            annotations['local'][tokenContent][uID] = localDict();
        }
    } else {

        console.log(tokenContent);

        annotations['global'][tokenContent] = {
        'name': name,
        'uniqueIDs': uIDs,
        'sourcesWithNums': noMatch ? {} : sourcesWithNums[name]
        };
    }
}




function deleteLocalAnnotation(token, uID) {
    delete annotations['local'][token][uID];
}

function deleteGlobalAnnotation(token) {
    delete annotations['global'][token];
    console.log(annotations);
}

function deleteFromAnnotations(argsString) {
    var argsArray = argsString.split('----');

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
    annotations = JSON.parse(existing_annotations)['existingAnnotations'];
    if (annotations) {
        uIDs = getLocalUniqueIDs().concat(getGlobalUniqueIDs());
        setAnnotatedColor(uIDs);
        renderAnnotationsTable();
    } else {
        annotations = {};
    }

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

