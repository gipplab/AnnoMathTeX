var AnnotationDict = function(type) {
    this.type = type;
    this.annotations = {}
};

var LocalAnnotation = function(source, rowNum, sourcesContaining) {
    //this.mathEnv = mathEnv;
    this.source = source;
    this.rowNum = rowNum;
    this.sourcesContaining = sourcesContaining
};

var GlobalAnnotation = function(name, source, uniqueIDs, sourcesContaining) {
    this.name = name;
    this.source = source;
    this.uniqueIDs = uniqueIDs;
    this.sourcesContaining = sourcesContaining;
};
