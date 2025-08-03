# 🚀 QUICK START REFERENCE CARD
## Exposure Solutions Recon Agent v2.0 Pro

---

## ⚡ INSTANT SETUP (2 MINUTES)

```bash
# 1. Navigate to package
cd "C:\Users\danga\OneDrive - Exposure Solutions\Exposureai\AI Agents\Exposure Solutions Recon Agent"

# 2. Run installer
INSTALL.bat

# 3. Test system
python exposure_solutions_recon_agent.py recon --target "The Valley House"
```

---

## 📁 REQUIRED FILES (Must be together)

```
✅ exposure_solutions_recon_agent.py  (34KB) - Main system
✅ drone_simulation.py               (19KB) - Drone module  
✅ requirements.txt                  (168B) - Dependencies
✅ recon_config.json                 (938B) - Configuration
✅ deploy_recon_agent.py             (11KB) - Auto-installer
```

**⚠️ DO NOT SEPARATE THESE FILES - System will not work!**

---

## 🔑 API KEYS (Optional but recommended)

```json
{
  "openai_api_key": "sk-your-key-here",        // $20/month - AI analysis
  "google_maps_api_key": "AIza-your-key",     // $2/1000 - High-quality imagery  
  "twitter_bearer_token": "AAA-your-token"    // Free - Social monitoring
}
```

**Get keys:**
- OpenAI: https://platform.openai.com/api-keys
- Google: https://console.cloud.google.com/google/maps-apis
- Twitter: https://developer.twitter.com/portal/dashboard

---

## 🎮 GAME INTEGRATION (3 methods)

### Method 1: Direct Import
```python
from exposure_solutions_recon_agent import GameIntegrationAPI
game_api = GameIntegrationAPI()
location = game_api.get_location_data("The Valley House", "Achill Island")
```

### Method 2: API Server
```bash
python -c "from exposure_solutions_recon_agent import GameIntegrationAPI; GameIntegrationAPI().run_server()"
# Access: GET http://localhost:8000/api/discover/The%20Valley%20House
```

### Method 3: CLI Commands
```bash
python exposure_solutions_recon_agent.py recon --target "Keel Beach"
python google_maps_flyover.py  # Drone simulation demo
```

---

## 📊 WHAT YOU GET

**Input:** `"The Valley House"`
**Output:**
- 🤖 AI analysis with strategic insights
- 🛰️ High-quality satellite imagery
- 🚁 Interactive drone flyover simulation
- 📄 Professional HTML reconnaissance report
- 🎮 Game-ready JSON data with challenge levels, lore, coordinates

---

## 🔧 COMMON COMMANDS

```bash
# Basic reconnaissance
python exposure_solutions_recon_agent.py recon --target "POI Name"

# Drone mission only
python exposure_solutions_recon_agent.py drone --target "POI Name"

# Google Maps flyover demo
python google_maps_flyover.py

# Start API server
python -c "from exposure_solutions_recon_agent import GameIntegrationAPI; GameIntegrationAPI().run_server()"

# Test configuration
python exposure_solutions_recon_agent.py config --test

# View logs
tail -f logs/recon_agent.log

# Health check
python -c "from exposure_solutions_recon_agent import ExposureSolutionsReconAgent; print('✅ Working!' if ExposureSolutionsReconAgent() else '❌ Error')"
```

---

## 🚨 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `OpenAI API key not found` | Add key to `recon_config.json` |
| `FileNotFoundError: recon_config.json` | Ensure you're in the correct directory |
| `Permission denied` | `mkdir logs recon_reports drone_missions` |
| `Geocoding failed` | Internet connection required |
| Import errors | Files must be in same directory |

---

## 📂 GENERATED FILES

System automatically creates:
```
recon_reports/          # HTML reconnaissance reports
drone_missions/         # KML mission files  
google_maps_flyover/    # Satellite imagery with HUD
logs/                   # System logs
recon_cache/           # Performance cache (24hr)
```

---

## 🎯 GAME DATA STRUCTURE

```json
{
  "success": true,
  "location_id": "achill_valley_house",
  "display_name": "The Valley House",
  "coordinates": {"lat": 53.9889, "lon": -10.0661},
  "game_mechanics": {
    "challenge_level": 3,     // 1-5 scale
    "reward_tier": "bronze",  // bronze/silver/gold
    "accessibility": "medium" // easy/medium/hard
  },
  "lore_elements": {
    "mythology_connection": "Celtic legends",
    "historical_significance": "Moderate"
  },
  "player_interactions": {
    "can_explore": true,
    "photo_opportunities": true,
    "quest_potential": "medium"
  }
}
```

---

## 🎮 READY FOR YOUR GAME!

**✅ Perfect for "Achill AI Avengers - Island of Legends"**

This system transforms real Achill Island locations into engaging game content with:
- Real satellite imagery for authentic environments
- AI-generated lore and strategic insights  
- Dynamic challenge levels based on location data
- Professional reconnaissance reports for immersive gameplay
- Interactive drone missions as mini-games

**🚁 Your players will experience Achill Island like never before!**

---

## 📞 SUPPORT

- 📖 **Full Manual**: USER_MANUAL.md (15,000+ words)
- 🔧 **DevOps Guide**: DEVOPS_INSTRUCTIONS.md
- 💡 **Examples**: game_integration_example.py
- 📊 **Logs**: logs/recon_agent.log
- 🏥 **Health**: GET http://localhost:8000/health

**Package Location:**
`C:\Users\danga\OneDrive - Exposure Solutions\Exposureai\AI Agents\Exposure Solutions Recon Agent`

---

*🎯 Exposure Solutions Recon Agent v2.0 Pro - Ready to transform your game! 🎮🏝️*
