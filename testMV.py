import pygame
import cv2
import numpy as np
from moviepy.editor import VideoFileClip # Import moviepy

pygame.init()

# ... (視窗、字體等設定與之前相同) ...
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("APT - 進階優化")

video_filepath = 'video.mp4'

# --- ★★ MoviePy Integration ★★ ---
try:
    clip = VideoFileClip(video_filepath)
    # Get video properties from moviepy clip
    original_video_width = clip.w
    original_video_height = clip.h
    video_fps = clip.fps
    if video_fps == 0: # Fallback if fps is not detected
        video_fps = 30
except Exception as e:
    print(f"錯誤：無法打開影片檔案或處理MoviePy：{e}。")
    pygame.quit()
    exit()

# Initialize audio playback with Pygame mixer
pygame.mixer.init()
# If you want to play the audio separately, you might extract it or let moviepy handle it
# For seamless integration, moviepy can manage both.
# We'll use moviepy's get_frame for video and let it handle audio internally.

# --- Original video capture (still useful for traditional frame reading if moviepy doesn't fit all needs)
# For the combined approach, you might not directly use capV.read() in the loop.
# Instead, moviepy's get_frame will provide the numpy array.
# However, if you want to use cv2 for frame processing and moviepy for audio, you'd manage both.
# For simplicity, let's stick with moviepy providing frames and audio.

# Calculate scaling dimensions (這部分邏輯不變)
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

# Start playing the audio through moviepy (it uses pygame.mixer internally if available)
clip.audio.write_audiofile("temp_audio.mp3") # Extract audio to a temporary file
pygame.mixer.music.load("temp_audio.mp3")
pygame.mixer.music.play(0) # Play once

start_time = pygame.time.get_ticks() # Get the initial time for video synchronization

frame_number = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Optional: Allow stopping audio when video ends or program quits
        if event.type == pygame.USEREVENT: # Custom event for when music ends
            if pygame.mixer.music.get_busy() == False:
                # Music has finished playing
                pass # Or stop video playback if synchronized closely

    # --- Synchronize video frames with elapsed time ---
    current_time_ms = pygame.time.get_ticks() - start_time
    # Ensure current_time is within clip duration
    if current_time_ms / 1000.0 >= clip.duration:
        running = False # End playback if video finishes
        continue

    # Get the frame at the current time
    try:
        # moviepy's get_frame returns an RGB numpy array
        # It's already the correct orientation for pygame.surfarray.blit_array
        # No need for cv2.cvtColor or .swapaxes if moviepy provides it correctly
        frame_rgb = clip.get_frame(current_time_ms / 1000.0) # Time in seconds
    except Exception as e:
        print(f"Error getting frame: {e}")
        running = False
        continue

    window.fill((0, 0, 0))

    # --- ★★ 關鍵優化 ★★ ---
    # 1. moviepy's get_frame already gives us the desired frame.
    #    We still need to resize it if moviepy doesn't do it automatically to target_video_size.
    #    moviepy's get_frame can take a size argument, which is more efficient.
    #    However, if we already scaled for initial setup, we might need to rescale here.
    #    Let's assume get_frame gives original resolution, and we resize with cv2.
    #    Or, even better, let moviepy scale:
    if target_video_size != (original_video_width, original_video_height):
        # Moviepy's get_frame can take a size parameter for efficient resizing
        frame_rgb = clip.get_frame(current_time_ms / 1000.0, target_resolution=target_video_size[::-1]) # MoviePy expects (height, width) for target_resolution
        # Note: target_resolution is for the *output* frame.
        # It handles the scaling, so no need for cv2.resize after this.
    else:
        frame_rgb = clip.get_frame(current_time_ms / 1000.0)


    # 2. 將 NumPy 陣列的內容直接更新到已存在的 video_surface 上
    #    pygame.surfarray.blit_array expects (width, height, channels)
    #    MoviePy's get_frame returns (height, width, channels)
    #    So, we need to swapaxes(0, 1) to convert (height, width, channels) to (width, height, channels)
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


    pygame.display.flip()
    # clock.tick(video_fps) # We synchronize by time, not necessarily by fixed FPS for smoother playback
    # Instead, we should try to keep up with the video's actual frame rate for smoother animation.
    # A small delay to avoid consuming 100% CPU when not needed.
    # This also helps in not running through frames too quickly if get_frame takes time.
    time_to_next_frame = (frame_number + 1) * (1000 / video_fps) - (pygame.time.get_ticks() - start_time)
    if time_to_next_frame > 0:
        pygame.time.delay(int(time_to_next_frame))
    frame_number += 1

# Clean up
if pygame.mixer.music.get_busy():
    pygame.mixer.music.stop()
pygame.mixer.quit()
clip.close() # Important to close moviepy clip
pygame.quit()
