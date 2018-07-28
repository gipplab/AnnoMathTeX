def read_doc():

    #open and read in document
    filename = input("Enter document filename: ")
    #filename = "test.tex"
    file = open(filename,'r')
    content = file.read()

    #remove linebreaks
    content = content.replace('\r', '').replace('\n', '')

    return content
