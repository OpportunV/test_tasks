import csv
from collections import defaultdict, namedtuple
from typing import List

PLACES = 'place_zone_coordinates.csv'
USERS = 'user_coordinates.csv'
RESULT = 'places_available.csv'
ATOL = 1e-10    # Absolute tolerance between two float values to consider them equal
Point = namedtuple('Point', ['x', 'y'])


def skip_rows(reader, n):
    for i in range(n):
        next(reader)


def parse_places(filename):
    places = defaultdict(list)
    with open(filename, 'r') as fn:
        reader = csv.reader(fn)
        skip_rows(reader, 2)
        for row in reader:
            places[int(row[0])].append(Point(float(row[1]), float(row[2])))
    
    return places


def parse_users(filename):
    users = {}
    with open(filename, 'r') as fn:
        reader = csv.reader(fn)
        skip_rows(reader, 2)
        for row in reader:
            users[int(row[0])] = Point(float(row[1]), float(row[2]))
    
    return users


def write_results(filename):
    with open(filename, 'w', newline='') as fn:
        writer = csv.writer(fn)
        writer.writerows([('id', 'number_of_places_available'), ''])
        pair: Point = yield  # where x is user_id and y is number of places available
        while pair is not None:
            writer.writerow([pair.x, pair.y])
            pair = yield


def check_point(point: Point, polygon: List[Point]):
    """
    Check if the point placed inside (including edges i hope) or outside the polygon using ray casting method.
    Ray goes from point to the right.
    """
    intersections = 0
    n = len(polygon)
    
    p1 = polygon[-1]
    print(point)
    # Checking every edge of the polygon inside for loop
    for i in range(n):
        p2 = polygon[i]
        print(p1, p2, '--------------')
        # if point higher or lower than edge we immediately go to the next edge
        if min(p1.y, p2.y) <= point.y <= max(p1.y, p2.y):
            # Here goes the check for horizontal edge case, if so - it doesn't counts
            if abs(point.y - p1.y) <= ATOL:
                if p1.y < p2.y:
                    intersections += 1
                    print('if1')
            
            # Here goes the check for vertical edge case, if point to the left - it's an intersection
            elif abs(p2.x - p1.x) <= ATOL:
                if point.x < p2.x:
                    intersections += 1
                    print('if3')
            # Here goes a "regular" edge case
            else:
                k = (p2.y - p1.y) / (p2.x - p1.x)  # y = k*x + b -- line equation
                b = p1.y - k * p1.x
                x_of_point_y = (point.y - b) / k
                
                print(x_of_point_y)
                if point.x <= x_of_point_y:
                    print(point, p1, p2)
                    intersections += 1
                    print('if4')
        
        p1 = p2
    
    print(intersections)
    
    return intersections % 2 == 1


def check_users(users, places):
    writer_coroutine = write_results(RESULT)
    next(writer_coroutine)
    
    for user_id, user_point in users.items():
        writer_coroutine.send(Point(user_id, sum({check_point(user_point, place) for place in places.values()})))


def main():
    users = parse_users(USERS)
    places = parse_places(PLACES)
    
    # check_users(users, places)
    
    # print(check_point(Point(3.0, 3.0), [Point(2.0, 1.0),
    #                                     Point(4.5, 2.5),
    #                                     Point(4.0, 4.0),
    #                                     Point(2.0, 4.0)]))
    print(check_point(Point(1.0, 1.0), [Point(1.0, 1.0),
                                        Point(3.0, 1.0),
                                        Point(3.0, 3.0),
                                        Point(1.0, 3.0)]))


if __name__ == '__main__':
    main()
