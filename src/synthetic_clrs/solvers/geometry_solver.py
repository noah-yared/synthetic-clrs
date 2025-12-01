class GeometrySolver:
    @staticmethod
    def graham_scan(xs, ys):
        points = list(zip(xs, ys))

        if not points:
            return []

        if len(points) == 1:
            return [1]

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
        def polar_angle_key(v):
            dx = v[0] - lowest_point[0]
            dy = v[1] - lowest_point[1]
            import math
            return math.atan2(dy, dx)

        other_points = [(i, p) for i, p in enumerate(points) if i != i_low]
        sorted_points = list(sorted(
            other_points,
            key=lambda e: polar_angle_key(e[1]),
        ))

        # iterate through points, only accepting into 
        # convex hull if it forms right turn
        def forms_left_turn(p0, p1, p2):
            v0 = (p1[0] - p0[0], p1[1] - p0[1])
            v1 = (p2[0] - p1[0], p2[1] - p1[1])
            cross_prod = v0[0] * v1[1] - v0[1] * v1[0]
            return cross_prod > 0

        convex_hull.append(sorted_points[0][0])
        for i, n in sorted_points[1:]:
            # pop points from convex hull until
            # we form a left turn
            while len(convex_hull) >= 2:
                p = points[convex_hull[-2]]
                c = points[convex_hull[-1]]
                if forms_left_turn(p, c, n):
                    break
                convex_hull.pop()
            convex_hull.append(i)

        selected = [0 for _ in range(len(points))]
        for i in convex_hull:
            selected[i] = 1
        
        return selected
            
    
    @staticmethod
    def jarvis_march(xs, ys):
        points = list(zip(xs, ys))

        if not points:
            return []
        
        # choose leftmost point (tiebreak with lower y)
        leftmost_point = (float('inf'), float('inf'))
        for x, y in points:
            if x > leftmost_point[0]:
                continue
            if x == leftmost_point[0] and y > leftmost_point[1]:
                continue
            leftmost_point = (x, y)

        i_left = next((
            i for i, p in enumerate(points)
            if p == leftmost_point 
        ))

        # iteratively choose p_i+1 such that all 
        # points are to the right of p_ip_i+1
        def compute_score(p0, p1, p2):
            if p0 is None:
                v0 = (0, -1) if p1[0] < 0 else (0, 1)
            else:
                v0 = (p1[0] - p0[0], p1[1] - p0[1])
            v = (p2[0] - p1[0], p2[1] - p1[1])
            mag_v0_sq = sum(x**2 for x in v0)
            mag_v_sq = sum(x**2 for x in v)
            if mag_v0_sq == 0 or mag_v_sq == 0:
                # skip degenerate cases
                return -float('inf'), 0
            dotprod = sum(x*y for x, y in zip(v0, v))
            cos_theta = dotprod / ((mag_v0_sq * mag_v_sq) ** 0.5)
            # Return (cos_theta, mag_v_sq) to use distance
            # from the origin as a tiebreaker for collinear points
            # when choosing next point to add to convex hull
            return cos_theta, mag_v_sq

        convex_hull = [i_left]

        prev, curr = None, leftmost_point
        while len(convex_hull) < len(points):
            # completed convex hull
            if curr == leftmost_point and prev is not None:
                convex_hull.pop()
                break
            i_selected = max(
                range(len(points)),
                key=lambda i: compute_score(prev, curr, points[i])
            )
            convex_hull.append(i_selected)
            prev = curr
            curr = points[i_selected]
             
        selected = [0 for _ in range(len(points))]
        for i in convex_hull:
            selected[i] = 1

        return selected


    @staticmethod
    def segment_intersect(xs, ys):
        # algorithm adopted from:
        # https://github.com/vlecomte/cp-geo
        a, b, c, d = list(zip(xs, ys))

        def cross(x, y):
            return x[0] * y[1] - x[1] * y[0]

        def orient(x, y, z):
            return cross((y[0] - x[0], y[1] - x[1]), (z[0] - y[0], z[1] - y[1]))
        
        oa = orient(c, d, a)
        ob = orient(c, d, b)
        oc = orient(a, b, c)
        od = orient(a, b, d)

        return 1 if (oa * ob < 0) and (oc * od < 0) else 0
