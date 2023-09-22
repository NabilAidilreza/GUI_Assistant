def readFile(file_name):
    with open(file_name,"r") as f:
        page = f.readlines()
        text_string = ""
        for p in page:
            text_string += p
        return text_string
