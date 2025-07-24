import pygame
import cv2
import numpy as np # blit_array 會需要

pygame.init()

# ... (視窗、字體等設定與之前相同) ...
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("APT - 進階優化")

video_filepath = 'video.mp4'
try:
    capV = cv2.VideoCapture(video_filepath)
    if not capV.isOpened():
        raise IOError("無法打開影片檔案")
except IOError as e:
    print(f"錯誤：{e}。")
    pygame.quit()
    exit()

original_video_width = int(capV.get(cv2.CAP_PROP_FRAME_WIDTH))
original_video_height = int(capV.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = capV.get(cv2.CAP_PROP_FPS)
if video_fps == 0:
    video_fps = 30

# 計算縮放尺寸 (這部分邏輯不變)
target_video_width = window_width
target_video_height = int(original_video_height * (window_width / original_video_width))
if target_video_height > window_height:
    target_video_height = window_height
    target_video_width = int(original_video_width * (window_height / original_video_height))
target_video_size = (target_video_width, target_video_height) # 將目標尺寸存成元組

x_pos = (window_width - target_video_width) // 2
y_pos = (window_height - target_video_height) // 2

# --- ★★ 關鍵優化 ★★ ---
# 1. 在迴圈外只創建一次用於顯示影片的 Surface
#    注意尺寸是縮放後的目標尺寸
video_surface = pygame.Surface(target_video_size, 0, 24)
# -------------------------

# ... (其他 UI 設定) ...
font = pygame.font.SysFont("arial", 36)
value = 100

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = capV.read()

    if ret:
        window.fill((0, 0, 0))

        # --- ★★ 關鍵優化 ★★ ---
        # 1. 使用 cv2.resize() 進行縮放，這比 pygame.transform.scale() 快得多
        frame_resized = cv2.resize(frame, target_video_size)

        # 2. 轉換顏色空間
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        # 3. 將 NumPy 陣列的內容直接更新到已存在的 video_surface 上
        #    需要先旋轉軸 (swapaxes) 以匹配 Pygame 的座標系
        pygame.surfarray.blit_array(video_surface, frame_rgb.swapaxes(0, 1))
        # -------------------------
        
        # 現在 video_surface 已經是正確尺寸和內容了，直接 blit
        window.blit(video_surface, (x_pos, y_pos))
        
        # ... (繪製右上角文字和背景的程式碼不變) ...
        text_to_display = f"{value}"
        text_surface = font.render(text_to_display,True,(0,0,255))
        text_rect = text_surface.get_rect()
        box_padding = 10
        box_w = text_rect.width + 2 * box_padding
        box_h = text_rect.height +2 * box_padding
        box_x = window_width - box_w - 10
        box_y = 10
        pygame.draw.rect(window,(96,184,188,255),(box_x, box_y, box_w, box_h),border_radius=5)
        text_x = box_x + box_padding
        text_y = box_y + box_padding
        window.blit(text_surface, (text_x,text_y))

    else:
        running = False

    pygame.display.flip()
    clock.tick(video_fps)

capV.release()
pygame.quit()
