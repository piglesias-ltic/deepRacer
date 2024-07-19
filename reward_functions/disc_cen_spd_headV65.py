import math

def reward_function(params):
    WORST_REWARD = 1e-4
    BAD_REWARD = 1e-3
    CENTER_REWARD = 0.5
    SPEED_REWARD = 0.25
    STEP_REWARD = 1 - CENTER_REWARD - SPEED_REWARD
    STEP_WINDOW_REWARD = 15
    TARGET_STEPS = 300
    HEADING_PENALTY = 0.8

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

    HEADING_HORIZON = 2
    HEADING_MARGIN = 5.0
    HEADING_GAP = 2.5    

    def get_upcoming_track_direction(waypoints, closest_waypoints):
        # closest_waypoints[0] -> prev waypoint index
        # closest_waypoints[1] -> next waypoint index        
        upcoming_index = (closest_waypoints[1] + HEADING_HORIZON) % len(waypoints)
        upcoming_next_index = (closest_waypoints[1] + HEADING_HORIZON+1) % len(waypoints)
        upcoming_point = waypoints[upcoming_index]
        upcoming_next_point = waypoints[upcoming_next_index]
        # each point is a tuple of (x,y) coordinates
        # atan2(dy, dx) -> return between [-pi ; +pi]
        track_dir_rad = math.atan2(upcoming_next_point[1]-upcoming_point[1], upcoming_next_point[0]-upcoming_point[0])
        return math.degrees(track_dir_rad)

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
    heading = params['heading']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']


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
        
        track_dir = get_upcoming_track_direction(waypoints, closest_waypoints)
        if (abs(track_dir) <= HEADING_MARGIN/2) or (90-HEADING_MARGIN/2 <= track_dir <= 90+HEADING_MARGIN/2) or (-90-HEADING_MARGIN/2 <= track_dir <= -90+HEADING_MARGIN/2):
            # around 0, 90 and -90
            if not (track_dir-HEADING_GAP <= heading <= track_dir+HEADING_GAP):
                reward *= HEADING_PENALTY
        elif abs(track_dir) >= 180-HEADING_MARGIN/2:
            # around 180 (or -180)
            min_val = track_dir - HEADING_GAP/2
            if min_val < -180:
                min_val += 360
            max_val = track_dir + HEADING_GAP/2
            if max_val > 180:
                max_val -= 360                
            if max_val < min_val:
                aux = min_val
                min_val = max_val
                max_val = aux
            if min_val*max_val > 0:
                # same side (either positive or negative)
                if not (min_val <= heading <= max_val):
                    reward *= HEADING_PENALTY
            else:
                # min is negative (GT -180) and max is positive (LT 180)
                if not(-180 <= heading <= min_val) and not(max_val <= heading <= 180):
                    reward *= HEADING_PENALTY
        elif (0 < track_dir < 90) or (-180 < track_dir < -90):
            # quadrants 1 and 3
            if not(track_dir-HEADING_GAP <= heading <= track_dir):
                reward *= HEADING_PENALTY
        elif (90 < track_dir < 180) or (-90 < track_dir < 0):
            # quadrants 2 and 4
            if not(track_dir <= heading <= track_dir+HEADING_GAP):
                reward *= HEADING_PENALTY

        if (steps % STEP_WINDOW_REWARD) == 0 and progress > (steps / TARGET_STEPS)*100:
            reward += STEP_REWARD * STEP_WINDOW_REWARD
    
    return float(reward)


    # Bowtie track lenght: 17.43 m
    """
    {
        "x": float,                            # agent's x-coordinate in meters
        "y": float,                            # agent's y-coordinate in meters
        "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
        "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not.  
        "track_length": float,                 # track length in meters.
        "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
    }
    """
