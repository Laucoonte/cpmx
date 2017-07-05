
def marker(a,b,string,mark):
    """ This function marks "objects" in a string with a "mark" acording to
        its position.

        a--(int)        --   Lowest value of position in x of an object
        b--(int)        --   Bigest value of position in x of an object
        string--(str)   --   String you want to mark
        mark --(char)   --   Mark you want to put in your string
    """
    mark=mark*(b-a)
    begin=string[:a]
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
    return index
        #return marker(index,index+objectsize,string,"|")

def giveme_the_ponits(  boxes,
                        scores,
                        width,
                        height,
                        ycloseness,
                        xwidthness,
                        max_boxes_to_draw=20,
                        min_score_thresh=.5,
                        route_char="|",
                        object_char="X",
                        freepath_char="-"
                        ):
  route=freepath_char*width
  index=-1 #Default Value
  if not max_boxes_to_draw:
    max_boxes_to_draw = boxes.shape[0]
  for i in range(min(max_boxes_to_draw, boxes.shape[0])):
    if scores is None or scores[i] > min_score_thresh:
      ymin=boxes[i][0]*height
      xmin=boxes[i][1]*width
      ymax=boxes[i][2]*height
      xmax=boxes[i][3]*width
      normalized=[int(ymin),int(xmin),int(ymax),int(xmax)]
      if normalized[2]<ycloseness:
        for i in range(width):
          route=marker(normalized[1],normalized[3],route,object_char)
        index=pathfinder(route,xwidthness,freepath_char)
        if(index!=-1):
          route=marker(index,index+xwidthness,route,route_char)
          print(route)
        else:
          print("I'm wider than space freespace")

      else:
        print("something is too near")
  return index
