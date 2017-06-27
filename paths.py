
def marker(a,b,string,mark):
    """ This function marks "objects" in a string with a "mark" acording to
        its position.

        a--(int)        --   Lowest value of position in x of an object
        b--(int)        --   Bigest value of position in x of an object
        string--(str)   --   String you want to mark
        mark --(char)   --   Mark you want to put in your string
    """
    mark=mark*(b-a)
    begin=string[0:a]
    final=string[b:]
    return begin+mark+final
def pathfinder(string,objectsize,emptymark):
    """ This function find free way in a "strign of obstacles".
        and write a mark in
        string--(str)       --   String you want to be analized
        objectsize--(int)   --   "Object" size for looking for a path
        emtpymark --(char)  --   The mark of empty spaces in the string analized
    """
    emptymark=emptymark*objectsize
    index=string.find(emptymark)
    if(index== -1):
        return "Colision"
    else:
        return marker(index,index+objectsize,string,"|")
