import pygame
import random
from disc_flight import *
from parameters import *
from constants import *

pygame.init()

def draw_angle_ui(x, angle, title):
    mp_y = ANGLE_UI_Y + PB_HEIGHT/2
    angle_x = LINE_LEN * np.cos(np.radians(angle))
    angle_y = LINE_LEN * np.sin(np.radians(angle))

    text = ANGLE_FONT.render(title, True, WHITE)
    WIN.blit(text, (x + (LINE_LEN - text.get_width())/2, ANGLE_UI_Y - ANGLE_TITLE_Y_OFFSET))

    pygame.draw.line(WIN, BLACK, (x, ANGLE_UI_Y), (x, ANGLE_UI_Y + PB_HEIGHT), LINE_THICKNESS)
    pygame.draw.line(WIN, WHITE, (x, mp_y), (x + LINE_LEN, mp_y), LINE_THICKNESS)
    pygame.draw.line(WIN, RED, (x, mp_y), (x + angle_x, mp_y - angle_y), LINE_THICKNESS)
    pygame.draw.circle(WIN, BLACK, (x, mp_y), 5)

def draw_window(disc, goal, obstacle, parameters, graph_disc, time, ticks=0):
    WIN.fill(GREEN)
    WIN.blit(DISC, (disc.x, disc.y))

    timer = 0
    if time >= 0:
        timer = int(TIME_LIMIT / 1000 - int(time / 1000))

        #launch rotation
        cover_x = ROT_X + COVER_OFFSET + BAR_THICKNESS
        rotation_dir = "CW"
        rot_text_x = ROT_X + BAR_THICKNESS + BORDER
        if parameters.rotation == -1:
            rotation_dir = "CCW"
            rot_text_x = cover_x
            cover_x -= COVER_OFFSET
            
        rotation_text = ROTATION_FONT.render(rotation_dir, True, WHITE)
        rot_text_x = ROT_X + BAR_THICKNESS + (COVER_W - rotation_text.get_width())/2
        if parameters.rotation == -1:
            rot_text_x += COVER_OFFSET
        WIN.blit(rotation_text, (rot_text_x, ROT_TEXT_Y))
        cover = pygame.Rect(cover_x, COVER_Y, COVER_W, COVER_H)
        pygame.draw.rect(WIN, WHITE, ROT_BUTTON, BAR_THICKNESS)
        pygame.draw.rect(WIN, RED, cover, 0)
        
        #launch speed
        power_bar_fill = pygame.Rect(PB_X + BAR_THICKNESS, PB_Y + PIXELS_PER_MS*(27 - parameters.launch_speed), PB_WIDTH - 2*BAR_THICKNESS, parameters.launch_speed * PIXELS_PER_MS - 3)
        pygame.draw.rect(WIN, WHITE, POWER_BAR, BAR_THICKNESS)
        pygame.draw.rect(WIN, RED, power_bar_fill, 0)

        WIN.blit(POWER_TITLE, (POWER_TITLE_X, POWER_TITLE_Y))
        WIN.blit(ROT_TITLE, (ROT_TITLE_X, ROT_TITLE_Y))

        #draw goal and obstacle
        pygame.draw.rect(WIN, GREY, goal, 0)
        pygame.draw.rect(WIN, BROWN, obstacle, 0)

        #draw angles ui
        draw_angle_ui(VA_BL_X, parameters.launch_va, "Launch Angle")
        draw_angle_ui(HA_BL_X, parameters.launch_ha, "Launch Direction")
        draw_angle_ui(NA_BL_X, parameters.nose, "Nose Angle")
        draw_angle_ui(RA_BL_X, parameters.roll, "Roll Angle")

    else:
        timer = int(ticks/20)

        #graph bars
        graph_title = GRAPH_FONT.render("Elevation (y) vs Forward Distance (x)", True, WHITE)
        pygame.draw.rect(WIN, GREY, goal, 0)
        pygame.draw.rect(WIN, BROWN, obstacle, 0)
        WIN.blit(graph_title, (GRAPH_TITLE_X, GRAPH_TITLE_Y))
        pygame.draw.rect(WIN, WHITE, Z_BAR, 1)
        pygame.draw.rect(WIN, WHITE, X_BAR, 1)
        
        #graph objects
        graph_obs = pygame.Rect(GRAPH_LOWER_X_BOUND + obstacle.x/FT_TO_PIXELS, GRAPH_LOWER_Y_BOUND - OBSTACLE_Z, OBJ_SIZE/FT_TO_PIXELS, OBSTACLE_Z + 6)
        graph_goal = pygame.Rect(GRAPH_LOWER_X_BOUND + goal.x/FT_TO_PIXELS, GRAPH_LOWER_Y_BOUND - GOAL_UPPER_Z, OBJ_SIZE/FT_TO_PIXELS, GOAL_UPPER_Z - GOAL_LOWER_Z)
        graph_goal_post = pygame.Rect(GRAPH_LOWER_X_BOUND + goal.x/FT_TO_PIXELS + (OBJ_SIZE/FT_TO_PIXELS)/2 - 2, GRAPH_LOWER_Y_BOUND - GOAL_UPPER_Z, 2, GOAL_LOWER_Z * FT_TO_PIXELS)
        pygame.draw.rect(WIN, BROWN, graph_obs, 0)
        pygame.draw.rect(WIN, BLACK, graph_goal_post, 0)
        pygame.draw.rect(WIN, GREY, graph_goal, 0)
        pygame.draw.rect(WIN, RED, graph_disc, 0)

    timer_text = TIMER_FONT.render(str(timer), True, WHITE)
    WIN.blit(timer_text, (BORDER, BORDER))

    pygame.display.update()

def controls(keys_pressed, parameters):
    #e for ccw, r for cw
    #1,2 for power (0 - 27 in intervals of 0.25)
    #3,4 for launch angle (-90 - 90, intervals of 1)
    #5,6 for launch direction (-90 - 90, intervals of 1)
    #7,8 for nose (-90 - 90, intervals of 1)
    #9,0 for roll (-90 - 90, intervals of 1)
    if keys_pressed[pygame.K_e]:
        parameters.rotation = -1
    if keys_pressed[pygame.K_r]:
        parameters.rotation = 1
    if keys_pressed[pygame.K_1]:
        if parameters.launch_speed > 0:
            parameters.launch_speed -= POWER_SCALE
    if keys_pressed[pygame.K_2]:
        if parameters.launch_speed < 27:
            parameters.launch_speed += POWER_SCALE
    if keys_pressed[pygame.K_3]:
        if parameters.launch_va > -90:
            parameters.launch_va -= DEGREE_SCALE
    if keys_pressed[pygame.K_4]:
        if parameters.launch_va < 90:
            parameters.launch_va += DEGREE_SCALE
    if keys_pressed[pygame.K_5]:
        if parameters.launch_ha > -90:
            parameters.launch_ha -= DEGREE_SCALE
    if keys_pressed[pygame.K_6]:
        if parameters.launch_ha < 90:
            parameters.launch_ha += DEGREE_SCALE
    if keys_pressed[pygame.K_7]:
        if parameters.nose > -90:
            parameters.nose -= DEGREE_SCALE
    if keys_pressed[pygame.K_8]:
        if parameters.nose < 90:
            parameters.nose += DEGREE_SCALE
    if keys_pressed[pygame.K_9]:
        if parameters.roll > -90:
            parameters.roll -= DEGREE_SCALE
    if keys_pressed[pygame.K_0]:
        if parameters.roll < 90:
            parameters.roll += DEGREE_SCALE


# (lx, ly)----(ux, ly)
#    |             |
#    |             |
#    |             |
# (lx, uy)----(ux, uy)
# may break if a and b are switched
def is_intersect(a_lx, a_ux, a_ly, a_uy, b_lx, b_ux, b_ly, b_uy):
    if a_lx < b_ux and b_ux < a_ux and a_ly < b_uy and b_uy < a_uy:
        return True
    if a_lx < b_ux and b_ux < a_ux and a_ly < b_ly and b_ly < a_uy:
        return True
    if a_lx < b_lx and b_lx < a_ux and a_ly < b_uy and b_uy < a_uy:
        return True
    if a_lx < b_lx and b_lx < a_ux and a_ly < b_ly and b_ly < a_uy:
        return True
    return False


def generate_obj():
    goal_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
    goal_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    obstacle_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
    obstacle_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    while(is_intersect(goal_x, goal_x + OBJ_SIZE, goal_y, goal_y + OBJ_SIZE, obstacle_x, obstacle_x + OBJ_SIZE, obstacle_y, obstacle_y + OBJ_SIZE)):
        obstacle_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
        obstacle_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    goal = pygame.Rect(goal_x, goal_y, OBJ_SIZE, OBJ_SIZE)
    obstacle = pygame.Rect(obstacle_x, obstacle_y, OBJ_SIZE, OBJ_SIZE)
    return goal, obstacle

def get_distance(disc, goal):
    x_diff_sq = (disc[0] - goal[0])**2
    y_diff_sq = (disc[1] - goal[1])**2
    z_diff_sq = (disc[2] - goal[2])**2
    return np.sqrt(x_diff_sq + y_diff_sq + z_diff_sq)

def adjust_for_launch_angle(parameters, o_x, o_y, p_x, p_y):
    theta = parameters.launch_ha * -1
    diff_x = p_x - o_x
    diff_y = p_y - o_y
    x = (diff_x * np.cos(np.radians(theta))) - (diff_y * np.sin(np.radians(theta)))
    y = (diff_y * np.cos(np.radians(theta))) + (diff_x * np.sin(np.radians(theta)))
    return (x + o_x), (y + o_y)

def main():
    start_y = random.randrange(START_Y_LOWER, START_Y_UPPER)
    goal, obstacle = generate_obj()
    disc = pygame.Rect(START_X, start_y, DISC_SIZE, DISC_SIZE)
    graph_disc = pygame.Rect(GRAPH_LOWER_X_BOUND, GRAPH_LOWER_Y_BOUND, 5, 5)
    pre_launch = True
    current_time = 0
    transition_time = 0
    disc_pos_index = 0
    position_array = None
    disc_z = LAUNCH_HEIGHT
    min_distance = np.inf
    
    parameters = Parameters()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        current_time = pygame.time.get_ticks()
        if pre_launch and current_time >= TIME_LIMIT:
            position_array = throw_wrapper(parameters)
            pre_launch = False
            transition_time = current_time

        if pre_launch:
            draw_window(disc, goal, obstacle, parameters, graph_disc, current_time)
            keys_pressed = pygame.key.get_pressed()
            controls(keys_pressed, parameters)     
        else:
            launching_time = current_time - transition_time
            if launching_time > (disc_pos_index + 1) * INTERVAL_LEN:
                disc_pos_index += 1
                current_position = position_array[disc_pos_index]
                disc_z = current_position[2]
                if disc_z <= 0:
                    print("Landed")
                    break
                disc.x = START_X + current_position[0]*FT_TO_PIXELS
                disc.y = start_y + current_position[1]*FT_TO_PIXELS
                disc.x, disc.y = adjust_for_launch_angle(parameters, START_X, start_y, disc.x, disc.y)
                graph_disc.x = GRAPH_LOWER_X_BOUND + (disc.x - START_X)/FT_TO_PIXELS
                graph_disc.y = GRAPH_LOWER_Y_BOUND - disc_z
            draw_window(disc, goal, obstacle, parameters, graph_disc, -1, disc_pos_index)
            disc_mp_xyz = [disc.x + DISC_SIZE/2, disc.y + DISC_SIZE/2, disc_z*FT_TO_PIXELS]
            goal_mp_xyz= [goal.x + OBJ_SIZE/2, goal.y + OBJ_SIZE/2, GOAL_MP_Z*FT_TO_PIXELS]
            min_distance = min(min_distance, get_distance(disc_mp_xyz, goal_mp_xyz))
            if is_intersect(goal.x, goal.x + OBJ_SIZE, goal.y, goal.y + OBJ_SIZE, disc.x, disc.x + DISC_SIZE, disc.y, disc.y + DISC_SIZE):
                if GOAL_LOWER_Z <= disc_z and disc_z <= GOAL_UPPER_Z:
                    print("Previous minimum distance from goal (ft): ", min_distance/FT_TO_PIXELS)
                    min_distance = 0
                    print("Goal")
                    break
                else:
                    print("Not within goal height: ", disc_z)
            if is_intersect(obstacle.x, obstacle.x + OBJ_SIZE, obstacle.y, obstacle.y + OBJ_SIZE, disc.x, disc.x + DISC_SIZE, disc.y, disc.y + DISC_SIZE):
                if disc_z <= OBSTACLE_Z:
                    print("Hit Obstacle")
                    break
                #else:
                #    print("Above obstacle: ", disc_z)
    print("Minimum distance from goal (ft): ", min_distance/FT_TO_PIXELS)
    pygame.quit()

if __name__ == "__main__":
    main()