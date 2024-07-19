def reward_function(params):
    """
    from optTrkV2 import reward_function
    reward_function({'is_crashed': False, 'is_offtrack': False, 'is_reversed': False, 'all_wheels_on_track': True, 'track_width': 20.0, 'distance_from_center': 7.0, 'speed': 2.5, 'steering_angle': 0.0, 'steps': 5, 'progress': 30.0, 'closest_waypoints': (5, 6), 'heading': 90.0, 'is_left_of_center': True})
    """
    WORST_REWARD = 1e-4
    BAD_REWARD = 1e-3
    BASE_REWARD = 1.0
    STEP_WINDOW_REWARD = 10
    TARGET_STEPS = 300

    def get_side_of_track_penalty(is_left_of_center, next_waypoint):
        WAYPOINT_SIDE = [
            ((0, 12), False),
            ((14, 22), True),
            ((24, 38), False),
            ((40, 46), True),
            ((48, 50), False),
            ((52, 60), True),
            ((63, 68), False),
            ((70, 72), True),
            ((73, 93), False),
            ((95, 100), True),
            ((102, 104), False),
            ((106, 121), True),
            ((124, 155), False),
        ]
        for ws in WAYPOINT_SIDE:
            w = ws[0]
            side = ws[1]
            if w[0] <= next_waypoint <= w[1]:
                if is_left_of_center != side:
                    return 0.1
        return 1.0

    def get_heading_bonus_range(heading, speed, next_waypoint, waypoint_range, heading_range):
        bonus = 1.0
        if len(waypoint_range) == 2:
            waypoint_range += (waypoint_range[0], waypoint_range[1])
        if len(heading_range) == 2:
            heading_range += (heading_range[0], heading_range[1])

        if (waypoint_range[0] <= next_waypoint <= waypoint_range[1]) or (waypoint_range[2] <= next_waypoint <= waypoint_range[3]):
            if (heading_range[0] <= heading <= heading_range[1]) or (heading_range[2] <= heading <= heading_range[3]):
                bonus = 1.1
                if speed >= 4.0:
                    bonus *= 1.3
                elif speed >= 3.5:
                    bonus *= 1.2
                elif speed >= 2.5:
                    bonus *= 1.1
        return bonus

    def get_heading_bonus(heading, speed, next_waypoint):
        WAYPOINT_HEADING = [
            ((0, 10, 140, 155), (88.5, 90.0)),
            ((12, 25), (155.5, 157.0)),
            ((27, 35), (178.5, 180.0)),
            ((37, 48), (-130.0, -129.5)),
            ((50, 69), (-19.0, -18.5)),
            ((71, 79), (-126.0, -125.5)),
            ((81, 91), (178.5, 180.0)),
            ((93, 102), (-119.0, -118.5)),
            ((104, 130), (-6.0, -5.5)),
            ((132, 138), (36.5, 37.0)),
        ]
        for wh in WAYPOINT_HEADING:
            bonus = get_heading_bonus_range(heading, speed, next_waypoint, wh[0], wh[1])
            if bonus > 1.0:
                return bonus
        return 1.0

    if params['is_crashed'] or params['is_offtrack'] or params['is_reversed']: #is clockwise
        return WORST_REWARD
    
    if not params['all_wheels_on_track']:
        return BAD_REWARD

    steps = params['steps']
    progress = params['progress']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    is_left_of_center = params['is_left_of_center']

    reward = BASE_REWARD
    if (steps % STEP_WINDOW_REWARD) == 0 and progress >= (steps / TARGET_STEPS)*100:
        reward = 10 * BASE_REWARD * STEP_WINDOW_REWARD

    reward *= get_side_of_track_penalty(is_left_of_center, closest_waypoints[1])
    reward *= get_heading_bonus(heading, speed, closest_waypoints[1])
    
    return float(reward)