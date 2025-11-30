import Math

class GeometrySolver:
    @staticmethod
    def _graham_scan_solver(xs, ys):
        points = list(zip(xs, ys))

        # extract lowest point to initialize convex hull
        lowest_point = (float('inf'), float('inf'))
        for x, y in points:
            if y > lowest_point[-1]:
                continue
            elif y == lowest_point[-1] and x > lowest_point[0]:
                continue
            # lower y than current lowest_point
            # or same y but smaller x
            lowest_point = (x, y)

        i_low = next((
            i for i, p in enumerate(points)
            if p == lowest_point
        ))

        # initialize convex hull with lowest point
        convex_hull = [i_low]
            
        # sort other points by ccw angle from lowest point
        def cos_angle_to_vector(v):
            v0 = lowest_point
            dotprod = sum(x*y for x, y in zip(v0, v))
            mag1 = sum(x ** 2 for x in v0) ** 0.5
            mag2 = sum(x ** 2 for x in v) ** 0.5
            return dotprod / (mag1 * mag2)

        other_points = [i, p for i, p in enumerate(points) if i != i_low]
        sorted_points = list(sorted(
            other_points,
            key=lambda e: cos_angle_to_vector(e[1]),
            reverse=True
        ))

        # iterate through points, only accepting into 
        # convex hull if it forms right turn
        def forms_left_turn(p0, p1, p2)
            v0 = (p1[0] - p0[0], p1[1] - p0[1])
            v1 = (p2[0] - p1[0], p2[1] - p1[1])
            cross_prod = v0[0] * v1[1] - v0[1] * v1[0]
            return cross_prod < 0

        convex_hull.append(sorted_points[0][0])
        for i, n in other_points[1:]:
            p = points[convex_hull[-2]]
            n = points[convex_hull[-1]]
            if forms_left_turn(p, c, n):
                convex_hull.append(i)
            else:
                convex_hull[-1] = i

        selected = [0 for _ in range(len(points))]
        for i in convex_hull:
            selected[i] = 1
        
        return selected
            
    
    @staticmethod
    def _jarvis_match_solver(xs, ys):
        points = list(zip(xs, ys))
        
        # choose leftmost point (tiebreak with lower y)
        leftmost_point = (float('inf'), float('inf'))
        for x, y in points:
            if x > leftmost_point[0]:
                continue
            if x == leftmost_point[0] and y > leftmost_point:
                continue
            leftmost_point = (x, y)

        i_left = next((
            i for i, p in enumerate(points)
            if p == leftmost_point 
        ))

        # iteratively choose p_i+1 such that all 
        # points are to the right of p_ip_i+1
        def compute_cos_theta(p0, p1, p2):
            v0 = (0, 1) if p0 is None else (p1[0] - p0[0], p1[1] - p0[1])
            v = p2[0] - p1[0], p2[1] - p1[1]
            dotprod = sum(x*y for x, y in zip(v0, v))
            mag_v0 = sum(x**2 for x in v0) ** 0.5
            mag_v = sum(x**2 for x in v) ** 0.5
            return dotprod / (mag_v0 * mag_v)


        convex_hull = [i_left]

        prev = None, curr = leftmost_point
        while True:
            # completed convex hull
            if curr == leftmost_point and prev is not None:
                convex_hull.pop()
                break
            candidates = [
                i, p for i, p in enumerate(points)
                if p != curr
            ]
            i_selected, p_selected = max(
                candidates,
                key=lambda n: compute_cos_theta(prev, curr, n[1])
            )
            convex_hull.append(i_selected)
            prev = curr
            curr = p_selected
             
        selected = [0 for _ in range(len(points))]
        for i in convex_hull:
            selected[i] = 1

        return selected


    @staticmethod
    def _segements_intersect_solver(xs, ys):
        # algorithm adopted from:
        # https://github.com/vlecomte/cp-geo
        a, b, c, d = list(zip(xs, ys))

        def cross(x, y):
            return x[0] * y[1] - x[1] * y[0]

        def orient(x, y, z):
            return cross(y - x, z - y)
        
        oa = orient(c, d, a)
        ob = orient(c, d, b)
        oc = orient(a, b, c)
        od = orient(a, b, d)

        return 1 if (oa * ob < 0) and (oc * od < 0) else 0


    @staticmethod
    def solve(id, **kwargs):
        solvers = [
            GeometrySolver._graham_scan_solver(),
            GeometrySolver._jarvis_match_solver(),
            GeometrySolver._segments_intersect_solver(),
        ]
        assert 0 <= id < len(solvers), "id is out of range!"
        return solvers[id](**kwargs)