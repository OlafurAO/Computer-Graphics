import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from cannon import Cannon;
from objects import *;

screen_size = (800, 600);
clock = pygame.time.Clock();
delta_time = clock.tick() / 1000;

goal = Goal(screen_size);
obstacle_list = [];
cannon = Cannon(20, 0, obstacle_list, goal);

player_points = 0;


def init_game():
    pygame.display.init();
    pygame.display.set_mode((screen_size[0], screen_size[1]), DOUBLEBUF | OPENGL);

    glClearColor(1.0, 1.0, 1.0, 1.0);


def update():
    global delta_time;
    delta_time = clock.tick() / 1000;

    cannon.update_cannon(delta_time);


def display():
    glClear(GL_COLOR_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glViewport(0, 0, 800, 600);
    gluOrtho2D(0, 800, 0, 600);

    cannon.draw_cannon();
    goal.draw_goal();

    if(goal.goal_score):
        global player_points;
        global obstacle_list;

        goal.goal_score = False;

        player_points += 100;
        obstacle_list = [];

        cannon.set_obstacles(obstacle_list)

        print(player_points)

    for obst in obstacle_list:
        obst.draw_obstacle();

    pygame.display.flip();


def game_loop():
    init_game();

    click_and_drag_left_button = False;
    click_and_drag_right_button = False;

    while True:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit();
                quit();

            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RIGHT):
                    cannon.start_rotation(-1);
                elif(event.key == pygame.K_LEFT):
                    cannon.start_rotation(1);

                if(event.key == pygame.K_z):
                    cannon.fire_cannon();

            elif(event.type == pygame.KEYUP):
                if(event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    cannon.stop_rotation();

            # NOTE: obstacle collision only works with obstacles drawn from left to right
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 1):
                    if not(click_and_drag_left_button):
                        obstacle_list.append(Box(pygame.mouse.get_pos(), screen_size[1]));
                        click_and_drag_left_button = True;

                elif(event.button == 3):
                    if not(click_and_drag_right_button):
                        obstacle_list.append(Line(pygame.mouse.get_pos(), screen_size[1]));
                        click_and_drag_right_button = True;

            if(event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1):
                    click_and_drag_left_button = False;

                elif (event.button == 3):
                    click_and_drag_right_button = False;

        if(click_and_drag_left_button or click_and_drag_right_button):
            obstacle_list[-1].resize_obstacle(pygame.mouse.get_pos());

        update();
        display();


if __name__ == '__main__':
    game_loop();