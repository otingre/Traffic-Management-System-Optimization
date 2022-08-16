import sys
import re
import math

class Point(object):
    def __init__ (self, x, y):
        self.x = float(x)
        self.y = float(y)
    def __str__ (self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

class Line(object):
    def __init__ (self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return str(self.src) + '-->' + str(self.dst)

def intersect (l1, l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    a1 = y2-y1
    b1 = x1-x2
    c1 = a1*x1 + b1*y1

    a2 = y4-y3
    b2 = x3-x4
    c2 = a2*x3 + b2*y3

    determinant = a1*b2 - a2*b1

    if determinant == 0:
        return None,None
    else:
        x_temp = b2*c1 - b1*c2
        y_temp = a1*c2 - a2*c1
        
        if x_temp == 0:
            x = 0
        else:
            x = x_temp/determinant
            x = round(x,2)
        
        if y_temp == 0:
            y = 0
        else:
            y = y_temp/determinant
            y = round(y,2)
        
        return Point(x,y)

def onSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
 
def orientation(p, q, r):
     
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        
    if (val > 0):
        return 1
    
    elif (val < 0):
        return 2
    
    else:
        return 0
 
def doIntersect(p1,q1,p2,q2):
     
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
 
    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True
 
    # Special Cases
 
    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True
 
    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True
 
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True
 
    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True
 
    # If none of the cases
    return False

def point_on_segment(x1,y1,x2,y2,x3,y3):
    if (x2-x1!=0):
        slope = (y2 - y1) / (x2 - x1)
        slope = round(slope,2)
        pt3_on = (y3 - y1) == slope * (x3 - x1)
        if math.isclose(y3-y1,slope*(x3-x1),abs_tol = 0.05):
            pt3_on = True
        pt3_between = (min(x1, x2) <= x3 <= max(x1, x2)) and (min(y1, y2) <= y3 <= max(y1, y2))
        on_and_between = pt3_on and pt3_between
        return on_and_between
    else:
        on_and_between = (x3 == x2) and ((y1 <= y3 <= y2) or (y2 <= y3 <=y1))
        return on_and_between
 
def main():

    streets=[]

    points = []

    lines = []

    intersection_points = []

    edges = []

    final_points = []

    while(1):

        input_string = input()
        formatted_string = input_string.split('"')
        
        if (formatted_string[0]=="add "):

            pattern = re.compile(r'([A-Za-z]+( [A-Za-z]+)*)( \(-?[0-9]+,-?[0-9]+\))+')

            if re.fullmatch(pattern, str(formatted_string[1]+""+formatted_string[2])):
                get_coordinates = re.findall(r'[-]?[\d]+',formatted_string[2])
                if len(get_coordinates) == 2:
                    print("Error : Street should have atleast 2 points.")
                else:
                    temp_same_street = 0
                    if len(streets) > 0:
                        for i in range(len(streets)):
                            if streets[i][0] == formatted_string[1].lower():
                                print("Error : You have enter same street twice")
                                temp_same_street = 1
                                break
                    if temp_same_street == 0:
                        duplicate_coordinates = 0
                        for i in range(0,len(get_coordinates)-2,2):
                            for j in range(i+2,len(get_coordinates),2):
                                if (get_coordinates[i] == get_coordinates[j]) and (get_coordinates[i+1] == get_coordinates[j+1]):
                                    duplicate_coordinates = 1
                                    break
                        if duplicate_coordinates == 0:
                            get_coordinates.insert(0, formatted_string[1].lower())
                            streets.append(get_coordinates)
                        else:
                            print("Error : You have entered same coordinates")
            else:
                print("Error : Please enter valid input.")
            
        if (formatted_string[0]=="rm "):
            if formatted_string[2]=="":
                deleted_street = 0
                for i in range(len(streets)):
                    if(streets[i][0] == formatted_string[1].lower()):
                        del streets[i]
                        deleted_street = 1
                        break
                if deleted_street == 0:
                    print("Error : Please enter valid street name to be removed.")
            else:
                print("Error : Please enter valid input (rm Street_Name)")

        if (formatted_string[0]=="mod "):

            pattern = re.compile(r'([A-Za-z]+( [A-Za-z]+)*)( \(-?[0-9]+,-?[0-9]+\))+')

            if re.fullmatch(pattern, str(formatted_string[1]+""+formatted_string[2])):

                deleted_street = 0
                get_coordinates = re.findall(r'[-+]?[\d]+',formatted_string[2])
                if len(get_coordinates) == 2:
                    print("Error : Street should have 2 points.")
                else:
                    for i in range(len(streets)):
                        if(streets[i][0] == formatted_string[1].lower()):
                            duplicate_coordinates = 0
                            for j in range(0,len(get_coordinates)-2,2):
                                for k in range(j+2,len(get_coordinates),2):
                                    if (get_coordinates[j] == get_coordinates[k]) and (get_coordinates[j+1] == get_coordinates[k+1]):
                                        duplicate_coordinates = 1
                                        break
                            if (duplicate_coordinates == 0):
                                del streets[i]
                                deleted_street = 1
                                get_coordinates.insert(0, formatted_string[1].lower())
                                streets.append(get_coordinates)   
                            break
                    if duplicate_coordinates == 1:
                        print("Error : You have entered same coordinates")
                        
                    elif deleted_street == 0:
                        print("Error : Please enter valid street name to be modified.")

            else:
                print("Error : Please enter valid input.")

        if (formatted_string[0]=="gg"):
            # Clearing all the lists to generate the output for statements after gg
            points.clear()
            lines.clear()
            intersection_points.clear()
            edges.clear()
            final_points.clear()

            # Creating points for the added streets
            for i in range(len(streets)):
                for j in range(1,len(streets[i]),2):
                    points.append(Point(streets[i][j],streets[i][j+1]))

            # Creating lines for the generated points
            for i in range(len(streets)):
                for j in range(1,len(streets[i])-3,2):
                    lines.append(Line(Point(streets[i][j],streets[i][j+1]),Point(streets[i][j+2],streets[i][j+3])))

            line_iterator = 0
            for i in range(len(streets)-1):
                temp_len = int(((len(streets[i])-1)/2)-1)
                for j in range(line_iterator,line_iterator+temp_len):
                    for k in range(line_iterator+temp_len,len(lines)):
                        if (lines[j].src.x == lines[k].src.x and lines[j].src.y == lines[k].src.y) or (lines[j].src.x == lines[k].dst.x and lines[j].src.y == lines[k].dst.y) or (lines[j].dst.x == lines[k].src.x and lines[j].dst.y == lines[k].src.y) or (lines[j].dst.x == lines[k].dst.x and lines[j].dst.y == lines[k].dst.y):
                                edges.append(lines[j])
                                edges.append(lines[k])
                                final_points.append(Point(lines[j].src.x,lines[j].src.y))
                                final_points.append(Point(lines[j].dst.x,lines[j].dst.y))
                                final_points.append(Point(lines[k].src.x,lines[k].src.y))
                                final_points.append(Point(lines[k].dst.x,lines[k].dst.y))
                        elif doIntersect(Point(lines[j].src.x, lines[j].src.y), Point(lines[j].dst.x, lines[j].dst.y), Point(lines[k].src.x, lines[k].src.y), Point(lines[k].dst.x, lines[k].dst.y)):
                            intersec_point = intersect(lines[j],lines[k])
                            
                            temp_var = 1
                            for m in range(len(points)):
                                if float(intersec_point.x)==float(points[m].x) and float(intersec_point.y)==float(points[m].y):
                                    temp_var = 0
                            for l in range(len(intersection_points)):
                                if float(intersec_point.x)==float(intersection_points[l].x) and float(intersec_point.y)==float(intersection_points[l].y):
                                    temp_var = 0
                            if temp_var == 1:
                                intersection_points.append(intersec_point)
                            if lines[j].src.x == intersec_point.x and lines[j].src.y == intersec_point.y:
                                pass
                            else:
                                edges.append(Line(Point(lines[j].src.x,lines[j].src.y),intersec_point))
                            if lines[j].dst.x == intersec_point.x and lines[j].dst.y == intersec_point.y:
                                pass
                            else:
                                edges.append(Line(intersec_point,Point(lines[j].dst.x,lines[j].dst.y)))
                            if lines[k].src.x == intersec_point.x and lines[k].src.y == intersec_point.y:
                                pass
                            else:
                                edges.append(Line(Point(lines[k].src.x,lines[k].src.y),intersec_point))
                            if lines[k].dst.x == intersec_point.x and lines[k].dst.y == intersec_point.y:
                                pass
                            else:
                                edges.append(Line(intersec_point,Point(lines[k].dst.x,lines[k].dst.y)))
                            final_points.append(Point(lines[j].src.x,lines[j].src.y))
                            final_points.append(intersec_point)
                            final_points.append(Point(lines[j].dst.x,lines[j].dst.y))
                            final_points.append(Point(lines[k].src.x,lines[k].src.y))
                            final_points.append(Point(lines[k].dst.x,lines[k].dst.y))
                line_iterator = line_iterator + temp_len

            i = 0
            while i < len(edges):
                for j in range(len(points)):
                    if (edges[i].src.x == points[j].x and edges[i].src.y == points[j].y) or (edges[i].dst.x == points[j].x and edges[i].dst.y == points[j].y):
                        pass
                    else:
                        if point_on_segment(edges[i].src.x,edges[i].src.y,edges[i].dst.x,edges[i].dst.y,points[j].x,points[j].y):
                            edges.append(Line(Point(edges[i].src.x,edges[i].src.y),points[j]))
                            edges.append(Line(points[j],Point(edges[i].dst.x,edges[i].dst.y)))
                            del edges[i]
                            # i = i - 1
                for k in range(len(intersection_points)):
                    if (edges[i].src.x == intersection_points[k].x and edges[i].src.y == intersection_points[k].y) or (edges[i].dst.x == intersection_points[k].x and edges[i].dst.y == intersection_points[k].y):
                        pass
                    else:
                        if point_on_segment(edges[i].src.x,edges[i].src.y,edges[i].dst.x,edges[i].dst.y,intersection_points[k].x,intersection_points[k].y):
                            edges.append(Line(Point(edges[i].src.x,edges[i].src.y),intersection_points[k]))
                            edges.append(Line(intersection_points[k],Point(edges[i].dst.x,edges[i].dst.y)))
                            del edges[i]
                            # i = i - 1
                i = i + 1

            a = 0
            while a < len(edges)-1:
                b = a + 1
                while b < len(edges):
                    if (edges[a].src.x == edges[b].src.x and edges[a].src.y == edges[b].src.y and edges[a].dst.x == edges[b].dst.x and edges[a].dst.y == edges[b].dst.y):
                        del edges[a]
                        a = a - 1
                        b = b - 1
                        break
                    b = b + 1
                a = a + 1
            
            a = 0
            while a < len(final_points)-1:
                b = a + 1
                while b < len(final_points):
                    if (final_points[a].x == final_points[b].x and final_points[a].y == final_points[b].y):
                        del final_points[a]
                        a = a - 1
                        b = b - 1
                        break
                    b = b + 1
                a = a + 1

            print("V = {")
            for i in range(len(final_points)):
                print("{} : {}".format(i+1,final_points[i]))
            print("}")

            print("E = {")
            for i in range(len(edges)):
                for j in range(len(final_points)):
                    for k in range(len(final_points)):
                        if (edges[i].src.x == final_points[j].x and edges[i].src.y == final_points[j].y):
                            if (edges[i].dst.x == final_points[k].x and edges[i].dst.y == final_points[k].y):
                                print("<{},{}>".format(j+1,k+1))
            print("}")
                    
        elif (formatted_string[0]!="add " and formatted_string[0]!="rm " and formatted_string[0]!="mod " and formatted_string[0]!="gg"):
            print("Error : Please enter valid input")

if __name__ == "__main__" :
    main()