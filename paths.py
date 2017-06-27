
def marker(a,b,string,mark):
    """ This function marks in a string
        objects
    """
    mark=mark*(b-a)
    begin=string[0:a]
    final=string[b:]
    return begin+mark+final
def pathfinder(string,objectsize,emptymark):
    """ this function returns an path free of
        objects
    """
    emptymark=emptymark*objectsize
    index=string.find(emptymark)
    if(index== -1):
        return "Colision"
    else:
        return marker(index,index+objectsize,string,"Y")
