import pygame
import cv2 # 需要安裝 opencv-python

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("APT")

video_filepath = 'video.mp4' 


capV = cv2.VideoCapture(video_filepath)

if not capV.isOpened():
    print("錯誤：無法打開影片檔案。請檢查檔案路徑、GStreamer pipeline 或 OpenCV 安裝。")
    # print(f"嘗試開啟的 pipeline: {pipeline}")
    pygame.quit()
    exit()

# 獲取影片的原始尺寸，以便後續縮放
original_video_width = int(capV.get(cv2.CAP_PROP_FRAME_WIDTH))
original_video_height = int(capV.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 計算影片應該縮放到的目標尺寸 (例如，保持比例填滿視窗寬度)
target_video_width = window_width
target_video_height = int(original_video_height * (window_width / original_video_width))

# 如果按寬度縮放後高度溢出視窗，則按高度縮放
if target_video_height > window_height:
    target_video_height = window_height
    target_video_width = int(original_video_width * (window_height / original_video_height))

font = pygame.font.SysFont("arial",36)
value = 100

box_padding = 10
border_radius = 5
# 主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = capV.read()

    if ret:

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        video_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))

        scaled_video_surface = pygame.transform.scale(video_surface, (target_video_width, target_video_height))
        window.fill((0, 0, 0)) # 黑色背景
        
        x_pos = (window_width - target_video_width) // 2
        y_pos = (window_height - target_video_height) // 2
        window.blit(scaled_video_surface, (x_pos, y_pos))
        text_to_display = f"{value}"
        text_surface = font.render(text_to_display,True,(0,0,255))
        text_rect = text_surface.get_rect()
        box_w = text_rect.width + 2 * box_padding
        box_h = text_rect.height +2 * box_padding

        box_x = window_width - box_w - 10
        box_y = 10

        background_surface = pygame.Surface((box_w,box_h),pygame.SRCALPHA)
        background_color = (96,184,188,255)

        pygame.draw.rect(background_surface,background_color,(0, 0, box_w, box_h),border_radius=border_radius)
        window.blit(background_surface,(box_x,box_y))
        padding = 10
        text_x = box_x + box_padding
        text_y = box_y + box_padding
        window.blit(text_surface, (text_x,text_y))
    else:
        print("影片播放結束或無法讀取幀。")
        running = False 

    pygame.display.flip()


capV.release() 
pygame.quit() 
