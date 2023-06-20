import pygame
import subprocess
from best_path import path_finder
winforms_app_path = 'C:\\Users\\ntpdtrainee6\\source\\repos\\C#py\\C#py\\bin\\Debug'
subprocess.Popen(winforms_app_path)
grid_size = (23, 13)
cell_size = (30, 30)

pygame.init()

class objects:
    def __init__(self):
        self.output_path = []
        self.path = path_finder()

    def moving_obj(self, pointss):
        screen_size = (grid_size[0] * cell_size[0], grid_size[1] * cell_size[1])
        screen = pygame.display.set_mode(screen_size)

        rectangles = [[] for _ in range(len(pointss))]
        for k in range(len(pointss)):
            points = pointss[k]

            rectangle = pygame.Rect(0, 0, cell_size[0] - 10, cell_size[1] - 10)
            rectangle.center = (
                points[0][0] * cell_size[0] + cell_size[0] // 2,
                points[0][1] * cell_size[1] + cell_size[1] // 2)
            rectangles[k].append(rectangle)

        speed = 10
        
        point_indices = [0] * len(pointss)
        completed = [False] * len(pointss)
        all_completed = False

        while not all_completed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            all_completed = all(completed)

            for k in range(len(pointss)):
                if completed[k]:
                    continue

                points = pointss[k]
                rectangle = rectangles[k][0]

                if all(abs(rectangle.center[0] - (
                        points[point_indices[k]][0] * cell_size[0] + cell_size[0] // 2 + k * cell_size[0])) < 1 and abs(
                    rectangle.center[1] - (points[point_indices[k]][1] * cell_size[1] + cell_size[1] // 2)) < 1 for
                       rectangle in rectangles[k]):
                    point_indices[k] = (point_indices[k] + 1) % len(points)

                    if point_indices[k] == len(points) - 1:
                        completed[k] = True
                        if all(completed):
                            all_completed = True
                            break

                target_position = (points[point_indices[k]][0] * cell_size[0] + cell_size[0] // 2 + k * cell_size[0],
                                   points[point_indices[k]][1] * cell_size[1] + cell_size[1] // 2)
                dx = target_position[0] - rectangle.center[0]
                dy = target_position[1] - rectangle.center[1]

                if dx != 0:
                    new_rect = rectangle.move((dx / abs(dx) * cell_size[0] / speed, 0))
                    if self.check_collision(new_rect, rectangles, k):
                        rectangle.move_ip((dx / abs(dx) * cell_size[0] / speed, 0))
                    else:
                        alt_points = self.find_alternative_path(rectangle.center, target_position, rectangles, k)
                        if alt_points:
                            points[point_indices[k]:] = alt_points
                elif dy != 0:
                    new_rect = rectangle.move((0, dy / abs(dy) * cell_size[1] / speed))
                    if self.check_collision(new_rect, rectangles, k):
                        rectangle.move_ip((0, dy / abs(dy) * cell_size[1] / speed))
                    else:
                        alt_points = self.find_alternative_path(rectangle.center, target_position, rectangles, k)
                        if alt_points:
                            points[point_indices[k]:] = alt_points

            screen.fill((255, 255, 255))
            for x in range(grid_size[0]):
                for y in range(grid_size[1]):
                    cell_rect = pygame.Rect(x * cell_size[0], y * cell_size[1], cell_size[0], cell_size[1])
                    pygame.draw.rect(screen, (200, 200, 200), cell_rect, 1)

            for k in range(len(pointss)):
                color = (255, 0, 0) if k == 0 else (255, 255, 0)
                for rectangle in rectangles[k]:
                    pygame.draw.rect(screen, color, rectangle)

            pygame.display.flip()
            pygame.time.wait(50)

    def check_collision(self, rect, rectangles, current_index):
        for i, rect_list in enumerate(rectangles):
            if i != current_index:
                for other_rect in rect_list:
                    if rect.colliderect(other_rect):
                        return False
        return True

    def find_alternative_path(self, start_position, target_position, rectangles, current_index):
        # Implement your path planning algorithm here to find an alternative path
        return []

    def run_animation(self):
        agvs = int(input("ENTER THE NO OF AGVS: "))
        for j in range(agvs):
            points = self.path.final_path_detector()
            points.append(points[0])  # Append starting point at the end
            self.output_path.append(points)
        self.moving_obj(self.output_path)
        return agvs


a = objects()
a.run_animation()
