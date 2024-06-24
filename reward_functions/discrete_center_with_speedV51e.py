def reward_function(params):    
    WORST_REWARD = 1e-4
    BAD_REWARD = 1e-3
    CENTER_REWARD = 0.5
    SPEED_REWARD = 0.25
    STEP_REWARD = 1 - CENTER_REWARD - SPEED_REWARD
    STEP_WINDOW_REWARD = 15
    TARGET_STEPS = 150


    # tuples of (distance relative to the track width, percent of center reward)
    CENTER_MARKER_DIST_TO_COEF = [
        (0.25, 0.75), (0.5, 0.5), (0.75, 0.25)
    ]

    # tuples of (steering angle, speed range, percent of speed reward)
    STEERING_ANGLE_SPEED_TO_COEF = [
        (20.0, 0.75, 0.2), (20.0, 1.25, 0.4), (20.0, 5.0, 0.4),
        (5.0, 1.75, 0.1), (5.0, 2.75, 0.4), (5.0, 5.0, 0.5),
        (0.0, 2.5, 0.1), (0.0, 3.5, 0.2), (0.0, 5.0, 0.7),
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
        if (steps % STEP_WINDOW_REWARD) == 0 and progress > (steps / TARGET_STEPS)*100:
            reward += STEP_REWARD
    
    return float(reward)


    # Bowtie track lenght: 17.43 m
    """
    {
        "x": float,                            # agent's x-coordinate in meters
        "y": float,                            # agent's y-coordinate in meters
        "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
        "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not.  
        "heading": float,                      # agent's yaw in degrees
        "track_length": float,                 # track length in meters.
        "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
    }
    """
