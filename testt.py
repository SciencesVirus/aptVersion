import pygame
from pygamevideo import Video

FPS=60

pygame.init()

windows_w=800
windows_h=600
windows = pygame.display.set_mode((windows_w, windows_h))
# clock = pygame.time.Clock()
video = Video('video.mp4')
original_video_width = video.frame_width
original_video_height = video.frame_height
video.play()

playing=True
while playing:
    ...

    current_frame_surface = video.get_frame()
    if current_frame_surface:
        scaled_frame_surface = pygame.transform.scale(current_frame_surface,(640,480))
        video_x = (windows_w-640)//2
        video_y = (windows_h-480)//2

        windows.blit(scaled_frame_surface,(video_x,video_y))
    pygame.display.flip()

video.stop()
video.release()
pygame.quit()