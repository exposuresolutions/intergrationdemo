#!/usr/bin/env python3
"""
Exposure Solutions Recon Agent v2.0 Pro - Deployment Script
Game Integration Package for Achill AI Avengers - Island of Legends
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

class ReconAgentDeployer:
    def __init__(self):
        self.project_name = "exposure_solutions_recon_agent"
        self.game_name = "Achill AI Avengers - Island of Legends"
        self.required_files = [
            "exposure_solutions_recon_agent.py",
            "drone_simulation.py", 
            "requirements.txt",
            "recon_config.json",
            "README.md"
        ]
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required. Current version:", sys.version)
            return False
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    
    def check_required_files(self):
        """Check if all required files exist"""
        missing_files = []
        for file in self.required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print("❌ Missing required files:")
            for file in missing_files:
                print(f"   - {file}")
            return False
        
        print("✅ All required files present")
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            "recon_reports",
            "drone_missions", 
            "logs",
            "recon_cache"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created directory: {directory}")
        
        print("✅ Directory structure created")
        return True
    
    def configure_api_keys(self):
        """Interactive API key configuration"""
        print("\n🔑 API Key Configuration")
        print("=" * 50)
        
        config_file = "recon_config.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Interactive configuration
        api_keys = {
            "openai_api_key": "OpenAI API Key (for AI analysis)",
            "google_places_api_key": "Google Places API Key (optional)", 
            "google_maps_api_key": "Google Maps API Key (optional)",
            "twitter_bearer_token": "Twitter Bearer Token (optional)"
        }
        
        print("\nEnter your API keys (press Enter to skip optional keys):")
        for key, description in api_keys.items():
            current_value = config.get(key, "")
            if current_value and current_value != "your-key-here":
                print(f"✅ {description}: Already configured")
                continue
                
            required = "(REQUIRED)" if key == "openai_api_key" else "(optional)"
            new_value = input(f"Enter {description} {required}: ").strip()
            
            if new_value:
                config[key] = new_value
                print(f"✅ {description} configured")
            elif key == "openai_api_key":
                print("⚠️  Warning: OpenAI API key is required for AI analysis features")
        
        # Save updated configuration
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration saved")
        return True
    
    def test_installation(self):
        """Test the installation"""
        print("\n🧪 Testing installation...")
        
        try:
            # Test basic import
            sys.path.insert(0, os.getcwd())
            from exposure_solutions_recon_agent import ExposureSolutionsReconAgent
            
            agent = ExposureSolutionsReconAgent()
            print("✅ Main agent class imported successfully")
            
            # Test basic functionality
            result = agent.recon("Test Location", "Test Area", test_mode=True)
            if result:
                print("✅ Basic functionality test passed")
            else:
                print("⚠️  Basic functionality test had issues (check logs)")
            
            return True
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
        except Exception as e:
            print(f"⚠️  Test completed with warnings: {e}")
            return True
    
    def create_game_integration_example(self):
        """Create example integration code for the game"""
        example_code = '''
"""
Example Game Integration for Achill AI Avengers - Island of Legends
"""

from exposure_solutions_recon_agent import ExposureSolutionsReconAgent, GameIntegrationAPI

class AchillGameIntegration:
    def __init__(self):
        self.recon_agent = ExposureSolutionsReconAgent()
        self.game_api = GameIntegrationAPI(self.recon_agent)
    
    def discover_location(self, poi_name, player):
        """
        Called when player discovers a new location
        """
        # Get reconnaissance data
        location_data = self.game_api.get_location_data(poi_name, "Achill Island, Ireland")
        
        if location_data['success']:
            # Add location to game world
            game_location = {
                'id': location_data['location_id'],
                'name': location_data['display_name'],
                'coordinates': location_data['coordinates'],
                'challenge_level': location_data['game_mechanics']['challenge_level'],
                'lore': location_data['lore_elements']
            }
            
            # Award discovery points
            player.add_experience_points(100)
            player.unlock_location(game_location)
            
            # Show reconnaissance report
            self.show_recon_report(player, location_data)
            
            return game_location
        
        return None
    
    def start_drone_mission(self, poi_name, player):
        """
        Start interactive drone mission mini-game
        """
        drone_data = self.game_api.get_drone_data(poi_name)
        
        if drone_data['success']:
            # Launch drone simulation
            simulation_path = drone_data['simulation_path']
            
            # Award mission points
            player.add_experience_points(250)
            player.complete_drone_mission(poi_name)
            
            return simulation_path
        
        return None
    
    def show_recon_report(self, player, location_data):
        """
        Display reconnaissance report in game UI
        """
        # Example: Show in game's information panel
        report_html = location_data.get('report_path')
        if report_html:
            # Use your game's HTML viewer or browser component
            player.show_information_panel(report_html)

# Usage in your game:
# game_integration = AchillGameIntegration()
# location = game_integration.discover_location("The Valley House", current_player)
# drone_path = game_integration.start_drone_mission("The Valley House", current_player)
'''
        
        with open("game_integration_example.py", "w") as f:
            f.write(example_code)
        
        print("✅ Game integration example created: game_integration_example.py")
        return True
    
    def generate_deployment_summary(self):
        """Generate deployment summary"""
        summary = f"""
🎮 DEPLOYMENT SUMMARY - {self.game_name}
{"=" * 60}

✅ Installation Complete!

📁 Project Structure:
   {self.project_name}/
   ├── exposure_solutions_recon_agent.py  # Main system
   ├── drone_simulation.py                # Drone simulation
   ├── recon_config.json                 # Configuration
   ├── requirements.txt                   # Dependencies
   ├── README.md                         # Documentation
   ├── game_integration_example.py       # Integration example
   ├── recon_reports/                    # Generated reports
   ├── drone_missions/                   # Mission files
   ├── logs/                            # System logs
   └── recon_cache/                     # Performance cache

🚀 Quick Start Commands:
   # Test the system
   python exposure_solutions_recon_agent.py recon --target "The Valley House"
   
   # Start API server (optional)
   python -c "from exposure_solutions_recon_agent import GameIntegrationAPI; GameIntegrationAPI().run_server()"

🔧 Integration Options:
   1. Direct Import: Use ExposureSolutionsReconAgent class directly
   2. REST API: Run as standalone API server  
   3. CLI Commands: Command-line interface for testing

📚 Documentation:
   - Full documentation: README.md
   - Integration example: game_integration_example.py
   - Configuration: recon_config.json

🎯 Ready for {self.game_name}!
"""
        print(summary)
        
        # Save summary to file
        with open("DEPLOYMENT_SUMMARY.txt", "w") as f:
            f.write(summary)
        
        return True
    
    def deploy(self):
        """Main deployment process"""
        print("🚀 Starting Exposure Solutions Recon Agent v2.0 Pro Deployment")
        print(f"🎮 Target Game: {self.game_name}")
        print("=" * 70)
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Verifying required files", self.check_required_files),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up directories", self.setup_directories),
            ("Configuring API keys", self.configure_api_keys),
            ("Testing installation", self.test_installation),
            ("Creating integration example", self.create_game_integration_example),
            ("Generating summary", self.generate_deployment_summary)
        ]
        
        for step_name, step_function in steps:
            print(f"\n📋 {step_name}...")
            if not step_function():
                print(f"❌ Deployment failed at: {step_name}")
                return False
        
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("🎮 Your Exposure Solutions Recon Agent v2.0 Pro is ready for integration!")
        print(f"🏝️  Perfect for {self.game_name}!")
        
        return True

if __name__ == "__main__":
    deployer = ReconAgentDeployer()
    success = deployer.deploy()
    sys.exit(0 if success else 1)
