def reward_function(params):    
    WORST_REWARD = 1e-4
    BAD_REWARD = 1e-3
    CENTER_REWARD = 0.75
    SPEED_REWARD = 1 - CENTER_REWARD

    # tuples of (distance relative to the track width, percent of center reward)
    CENTER_MARKER_DIST_TO_COEF = [
        (0.1, 1), (0.25, 0.5), (0.5, 0.1)
    ]

    # tuples of (speed range, percent of speed reward)
    SPEED_RANGE_TO_COEF = [
        (1, 0.1), (2, 0.2), (3, 0.3), (4, 0.5), (5, 1)
    ]

    if params['is_crashed'] or params['is_offtrack'] or params['is_reversed']: #is clockwise
        return WORST_REWARD
    
    if not params['all_wheels_on_track']:
        return BAD_REWARD

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']

    reward = BAD_REWARD
    for m in CENTER_MARKER_DIST_TO_COEF:
        if distance_from_center <= m[0]*track_width:
            reward = m[1] * CENTER_REWARD
            break

    if reward != BAD_REWARD:
        for s in SPEED_RANGE_TO_COEF:
            if speed <= s[0]:
                reward += s[1] * SPEED_REWARD
                break
    
    return reward


    # Bowtie track lenght: 17.43 m
    """
    {
        "x": float,                            # agent's x-coordinate in meters
        "y": float,                            # agent's y-coordinate in meters
        "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
        "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not.  
        "heading": float,                      # agent's yaw in degrees
        "progress": float,                     # percentage of track completed
        "steering_angle": float,               # agent's steering angle in degrees
        "steps": int,                          # number steps completed
        "track_length": float,                 # track length in meters.
        "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
    }
    """
