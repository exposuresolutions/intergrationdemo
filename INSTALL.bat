@echo off
REM Quick Installation Script for Exposure Solutions Recon Agent v2.0 Pro
REM For "Achill AI Avengers - Island of Legends"

echo.
echo ======================================================
echo  EXPOSURE SOLUTIONS RECON AGENT v2.0 PRO INSTALLER
echo ======================================================
echo  Game: Achill AI Avengers - Island of Legends
echo ======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python detected
python --version

echo.
echo 📦 Installing dependencies...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

echo 🔧 Running automated deployment...
python deploy_recon_agent.py

echo.
echo 🧪 Testing installation...
python -c "from exposure_solutions_recon_agent import ExposureSolutionsReconAgent; print('✅ Main agent imported successfully')"

if errorlevel 1 (
    echo ⚠️  Import test failed - check configuration
) else (
    echo ✅ Installation test passed
)

echo.
echo ======================================================
echo  INSTALLATION COMPLETE!
echo ======================================================
echo.
echo 🎮 Ready for "Achill AI Avengers - Island of Legends"
echo.
echo 📋 Next Steps:
echo 1. Configure API keys in recon_config.json
echo 2. Test: python exposure_solutions_recon_agent.py recon --target "The Valley House"
echo 3. Review game_integration_example.py for integration
echo 4. Read DEVOPS_INSTRUCTIONS.md for complete guide
echo.
echo 🎯 Your reconnaissance system is ready!
echo.
pause
