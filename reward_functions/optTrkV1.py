def reward_function(params):
    """
    from optTrkV1 import reward_function
    reward_function({'is_crashed': False, 'is_offtrack': False, 'is_reversed': False, 'all_wheels_on_track': True, 'track_width': 20.0, 'distance_from_center': 7.0, 'speed': 2.5, 'steering_angle': 0.0, 'steps': 5, 'progress': 30.0, 'closest_waypoints': (5, 6), 'heading': 90.0})
    """
    WORST_REWARD = 1e-4
    BAD_REWARD = 1e-3
    CENTER_REWARD = 0.3
    SPEED_REWARD = 0.2
    STEP_REWARD = 1 - CENTER_REWARD - SPEED_REWARD
    STEP_WINDOW_REWARD = 10
    TARGET_STEPS = 300

    def get_heading_bonus_range(heading, speed, next_waypoint, waypoint_range, heading_range):
        bonus = 1.0
        if len(waypoint_range) == 2:
            waypoint_range += (waypoint_range[0], waypoint_range[1])
        if len(heading_range) == 2:
            heading_range += (heading_range[0], heading_range[1])

        if (waypoint_range[0] <= next_waypoint <= waypoint_range[1]) or (waypoint_range[2] <= next_waypoint <= waypoint_range[3]):
            if (heading_range[0] <= heading <= heading_range[1]) or (heading_range[2] <= heading <= heading_range[3]):
                bonus = 1.1
                if speed >= 3.0:
                    bonus *= 1.1
        return bonus

    def get_heading_bonus(heading, speed, next_waypoint):
        WAYPOINT_HEADING = [
            ((0, 10, 140, 155), (87.0, 93.0)),
            ((20, 34), (177.0, 180.0, -180.0, -177.0)),
            ((108, 133), (-3.0, 3.0)),
        ]
        for wh in WAYPOINT_HEADING:
            bonus = get_heading_bonus_range(heading, speed, next_waypoint, wh[0], wh[1])
            if bonus > 1.0:
                return bonus
        return 1.0

    # tuples of (distance relative to the track width, percent of center reward)
    CENTER_MARKER_DIST_TO_COEF = [
        (0.37, 0.75), (0.5, 0.5),
    ]

    # tuples of (steering angle, speed range, percent of speed reward)
    STEERING_ANGLE_SPEED_TO_COEF = [
        (20.0, 0.75, 0.1), (20.0, 1.25, 0.45), (20.0, 5.0, 0.45),
        (5.0, 1.75, 0.1), (5.0, 2.75, 0.4), (5.0, 5.0, 0.5),
        (0.0, 2.5, 0.01), (0.0, 3.5, 0.6), (0.0, 5.0, 0.9),
    ]

    if params['is_crashed'] or params['is_offtrack'] or params['is_reversed']: #is clockwise
        return WORST_REWARD
    
    if not params['all_wheels_on_track']:
        return BAD_REWARD

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steering_angle = params['steering_angle']
    steps = params['steps']
    progress = params['progress']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    reward = BAD_REWARD
    for cmc in CENTER_MARKER_DIST_TO_COEF:
        if distance_from_center <= cmc[0]*track_width:
            reward = cmc[1] * CENTER_REWARD
            break

    if reward != BAD_REWARD:
        for sasc in STEERING_ANGLE_SPEED_TO_COEF:
            if abs(steering_angle) >= sasc[0] and speed <= sasc[1]:
                reward += sasc[2] * SPEED_REWARD
                break
        if (steps % STEP_WINDOW_REWARD) == 0 and progress >= (steps / TARGET_STEPS)*100:
            reward += STEP_REWARD * STEP_WINDOW_REWARD
        
    reward *= get_heading_bonus(heading, speed, closest_waypoints[1])
    
    return float(reward)
