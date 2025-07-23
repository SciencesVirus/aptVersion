@echo off
echo ====================================
echo Posture Training System - Setup
echo ====================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/
    echo Recommended: Python 3.8-3.12
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip not found!
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo ====================================
echo Installing packages...
echo ====================================
echo.

echo [1/10] Installing NumPy (version 1.26.4)...
pip install "numpy>=1.21.0,<2.0"
if %errorlevel% neq 0 (
    echo ERROR: NumPy installation failed!
    pause
    exit /b 1
)

echo [2/10] Installing OpenCV (version 4.11.0.86)...
pip install opencv-python==4.11.0.86
if %errorlevel% neq 0 (
    echo Trying alternative OpenCV (headless)...
    pip install opencv-python-headless==4.11.0.86
    if %errorlevel% neq 0 (
        echo ERROR: OpenCV installation failed!
        pause
        exit /b 1
    )
)

echo [3/10] Installing Pygame (version 2.6.1)...
pip install pygame==2.6.1
if %errorlevel% neq 0 (
    echo ERROR: Pygame installation failed!
    pause
    exit /b 1
)

echo [4/10] Installing Pillow... (No specific version provided, installing latest compatible)
pip install Pillow
if %errorlevel% neq 0 (
    echo ERROR: Pillow installation failed!
    pause
    exit /b 1
)

echo [5/10] Installing MediaPipe... (No specific version provided, installing latest compatible)
pip install mediapipe
if %errorlevel% neq 0 (
    echo ERROR: MediaPipe installation failed!
    echo Trying alternative method...
    pip install mediapipe --no-cache-dir
    if %errorlevel% neq 0 (
        echo ERROR: MediaPipe installation completely failed!
        echo Please check your Python version
        pause
        exit /b 1
    )
)

echo [6/10] Installing Librosa (version 0.11.0)...
pip install librosa==0.11.0
if %errorlevel% neq 0 (
    echo ERROR: Librosa installation failed!
    pause
    exit /b 1
)

echo [7/10] Installing NCNN (version 1.0.20250612)...
pip install ncnn==1.0.20250612
if %errorlevel% neq 0 (
    echo ERROR: NCNN installation failed!
    pause
    exit /b 1
)

echo [8/10] Installing Pygamevideo (version 2.1.0)...
pip install pygamevideo==2.1.0
if %errorlevel% neq 0 (
    echo ERROR: Pygamevideo installation failed!
    pause
    exit /b 1
)

echo [9/10] Installing Python-OSC (version 1.9.3)...
pip install python-osc==1.9.3
if %errorlevel% neq 0 (
    echo ERROR: Python-OSC installation failed!
    pause
    exit /b 1
)

echo [10/10] Installing Ultralytics (version 8.3.156)...
pip install ultralytics==8.3.156
if %errorlevel% neq 0 (
    echo ERROR: Ultralytics installation failed!
    pause
    exit /b 1
)

echo.
echo ====================================
echo Installing extras...
echo ====================================
echo.

pip install setuptools wheel matplotlib
if %errorlevel% neq 0 (
    echo WARNING: Some extras failed to install
)

echo.
echo ====================================
echo Testing installations...
echo ====================================
echo.

python -c "import cv2; print('OpenCV: OK')" 2>nul
if %errorlevel% neq 0 (
    echo OpenCV: FAILED
    set TEST_FAILED=1
) else (
    echo OpenCV: OK
)

python -c "import numpy; print('NumPy: OK')" 2>nul
if %errorlevel% neq 0 (
    echo NumPy: FAILED
    set TEST_FAILED=1
) else (
    echo NumPy: OK
)

python -c "import pygame; print('Pygame: OK')" 2>nul
if %errorlevel% neq 0 (
    echo Pygame: FAILED
    set TEST_FAILED=1
) else (
    echo Pygame: OK
)

python -c "import PIL; print('Pillow: OK')" 2>nul
if %errorlevel% neq 0 (
    echo Pillow: FAILED
    set TEST_FAILED=1
) else (
    echo Pillow: OK
)

python -c "import mediapipe; print('MediaPipe: OK')" 2>nul
if %errorlevel% neq 0 (
    echo MediaPipe: FAILED
    set TEST_FAILED=1
) else (
    echo MediaPipe: OK
)

python -c "import librosa; print('Librosa: OK')" 2>nul
if %errorlevel% neq 0 (
    echo Librosa: FAILED
    set TEST_FAILED=1
) else (
    echo Librosa: OK
)

python -c "import ncnn; print('NCNN: OK')" 2>nul
if %errorlevel% neq 0 (
    echo NCNN: FAILED
    set TEST_FAILED=1
) else (
    echo NCNN: OK
)

python -c "import pygamevideo; print('Pygamevideo: OK')" 2>nul
if %errorlevel% neq 0 (
    echo Pygamevideo: FAILED
    set TEST_FAILED=1
) else (
    echo Pygamevideo: OK
)

python -c "import python_osc; print('Python-OSC: OK')" 2>nul
if %errorlevel% neq 0 (
    echo Python-OSC: FAILED
    set TEST_FAILED=1
) else (
    echo Python-OSC: OK
)

python -c "import ultralytics; print('Ultralytics: OK')" 2>nul
if %errorlevel% neq 0 (
    echo Ultralytics: FAILED
    set TEST_FAILED=1
) else (
    echo Ultralytics: OK
)

echo.
if defined TEST_FAILED (
    echo ====================================
    echo WARNING: Some tests failed!
    echo ====================================
    echo.
    echo Try running setup.bat again
    echo or check Python version (3.8-3.11 recommended)
    pause
) else (
    echo ====================================
    echo Setup completed successfully!
    echo ====================================
    echo.
    echo All packages installed and tested:
    echo - OpenCV (computer vision)
    echo - MediaPipe (AI pose detection)
    echo - NumPy (numerical computing)
    echo - Pygame (game engine)
    echo - Pillow (image processing)
    echo - Librosa (audio analysis)
    echo - NCNN (neural network inference)
    echo - Pygamevideo (video playback in Pygame)
    echo - Python-OSC (Open Sound Control)
    echo - Ultralytics (YOLO models)
    echo.
    echo You can now run:
    echo - run.bat (start game)
    echo - debugL1.bat (test Level 1)
    echo.
    echo Notes:
    echo 1. Connect your camera
    echo 2. Use good lighting
    echo 3. Check camera permissions if needed
    echo.
    pause
)
