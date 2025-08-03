#!/usr/bin/env python3
"""
Google Maps Drone Flyover Demo
High-quality satellite imagery using Google Maps Static API
"""

import os
import requests
import time
import json
from math import cos, sin, radians
from PIL import Image, ImageDraw, ImageFont

def create_google_maps_flyover():
    """Create high-quality drone flyover using Google Maps"""
    
    # The Valley House coordinates
    lat = 53.9889
    lon = -10.0661
    
    print("🎬 GOOGLE MAPS DRONE FLYOVER SIMULATION")
    print("=" * 60)
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 The Valley House - Achill Island, Ireland")
    print(f"📍 Coordinates: {lat}, {lon}")
    print("🛰️ Using Google Maps Static API (High Quality)")
    print("=" * 60)
    
    # Create output directory
    output_dir = "google_maps_flyover"
    os.makedirs(output_dir, exist_ok=True)
    
    # Google Maps Static API base URL
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    
    # You can get a free API key at: https://console.cloud.google.com/google/maps-apis
    # For demo purposes, we'll try without a key first (limited requests)
    api_key = ""  # Add your API key here for production use
    
    successful_frames = []
    
    # Generate flyover sequence with multiple angles
    radius_km = 0.4  # 400m radius for good coverage
    num_frames = 8
    
    for i in range(num_frames):
        angle_deg = i * 45  # 45-degree intervals
        angle_rad = radians(angle_deg)
        
        # Calculate offset coordinates for different viewpoints
        lat_offset = radius_km * cos(angle_rad) / 111.32
        lon_offset = radius_km * sin(angle_rad) / (111.32 * cos(radians(lat)))
        
        view_lat = lat + lat_offset
        view_lon = lon + lon_offset
        
        print(f"📸 Capturing frame {i+1}/{num_frames} - Angle: {angle_deg}°")
        
        # Google Maps Static API parameters for high-quality satellite imagery
        params = {
            'center': f"{view_lat},{view_lon}",
            'zoom': 18,  # High detail zoom level
            'size': '800x800',  # Higher resolution
            'maptype': 'satellite',
            'format': 'jpg',
            'scale': 2  # Retina/high-DPI quality
        }
        
        # Add API key if available
        if api_key:
            params['key'] = api_key
        
        # Build URL
        url = base_url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        try:
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                # Save high-quality satellite image
                base_path = os.path.join(output_dir, f'gmaps_frame_{i+1:02d}_satellite.jpg')
                with open(base_path, 'wb') as f:
                    f.write(response.content)
                
                # Add professional drone HUD overlay
                hud_path = add_professional_hud(base_path, i+1, angle_deg, view_lat, view_lon)
                
                successful_frames.append({
                    'frame': i+1,
                    'angle': angle_deg,
                    'lat': view_lat,
                    'lon': view_lon,
                    'base_path': base_path,
                    'hud_path': hud_path
                })
                
                print(f"✅ Frame {i+1} captured - High quality Google Maps imagery")
                time.sleep(1)  # Rate limiting
                
            else:
                print(f"⚠️ Frame {i+1} failed: HTTP {response.status_code}")
                if response.status_code == 403:
                    print("   📝 Note: Add Google Maps API key for unlimited access")
                
        except Exception as e:
            print(f"❌ Error capturing frame {i+1}: {e}")
    
    # Create center overhead view with maximum detail
    print("📸 Capturing center overhead view (maximum zoom)...")
    center_params = {
        'center': f"{lat},{lon}",
        'zoom': 19,  # Maximum detail for center view
        'size': '800x800',
        'maptype': 'satellite',
        'format': 'jpg',
        'scale': 2
    }
    
    if api_key:
        center_params['key'] = api_key
    
    center_url = base_url + "?" + "&".join([f"{k}={v}" for k, v in center_params.items()])
    
    try:
        response = requests.get(center_url, timeout=15)
        if response.status_code == 200:
            center_base = os.path.join(output_dir, 'gmaps_center_satellite.jpg')
            with open(center_base, 'wb') as f:
                f.write(response.content)
            
            center_hud = add_professional_hud(center_base, 'CENTER', 'overhead', lat, lon)
            
            successful_frames.append({
                'frame': 'center',
                'angle': 'overhead',
                'lat': lat,
                'lon': lon,
                'base_path': center_base,
                'hud_path': center_hud
            })
            print("✅ Center view captured - Ultra high quality")
    except Exception as e:
        print(f"❌ Error capturing center view: {e}")
    
    # Create professional HTML viewer
    create_professional_viewer(output_dir, successful_frames, lat, lon)
    
    # Save metadata
    metadata = {
        'poi_name': 'The Valley House, Achill Island, Ireland',
        'center_coordinates': {'lat': lat, 'lon': lon},
        'successful_frames': len(successful_frames),
        'image_source': 'Google Maps Static API',
        'image_quality': 'High (800x800, scale=2)',
        'zoom_levels': '18-19',
        'api_key_used': bool(api_key),
        'frames': successful_frames,
        'creation_date': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    metadata_path = os.path.join(output_dir, 'google_maps_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "=" * 60)
    print("🎉 GOOGLE MAPS FLYOVER COMPLETE!")
    print(f"📁 Output: {output_dir}/")
    print(f"🎬 Frames: {len(successful_frames)}")
    print(f"📊 Metadata: {metadata_path}")
    
    if not api_key:
        print("\n🔑 TO GET UNLIMITED HIGH-QUALITY ACCESS:")
        print("1. Go to: https://console.cloud.google.com/google/maps-apis")
        print("2. Create a project and enable 'Maps Static API'")
        print("3. Create credentials and get your API key")
        print("4. Add the key to this script in the 'api_key' variable")
        print("5. Enjoy unlimited high-resolution satellite imagery!")
    
    return metadata

def add_professional_hud(image_path, frame_number, angle, lat, lon):
    """Add professional military-style drone HUD overlay"""
    try:
        # Open high-resolution image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts (fallback to default)
        try:
            font_large = ImageFont.truetype("arial.ttf", 28)
            font_medium = ImageFont.truetype("arial.ttf", 20)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Professional military colors
        hud_green = (0, 255, 0)
        warning_amber = (255, 191, 0)
        target_red = (255, 0, 0)
        info_cyan = (0, 255, 255)
        
        # Draw advanced crosshairs
        center_x, center_y = img.width // 2, img.height // 2
        
        # Main crosshairs
        cross_size = 40
        draw.line([(center_x - cross_size, center_y), (center_x + cross_size, center_y)], 
                 fill=target_red, width=3)
        draw.line([(center_x, center_y - cross_size), (center_x, center_y + cross_size)], 
                 fill=target_red, width=3)
        
        # Center dot
        draw.ellipse([(center_x-3, center_y-3), (center_x+3, center_y+3)], fill=target_red)
        
        # Corner reticles
        reticle_size = 25
        corners = [
            (30, 30), (img.width-30-reticle_size, 30),
            (30, img.height-30-reticle_size), (img.width-30-reticle_size, img.height-30-reticle_size)
        ]
        
        for x, y in corners:
            # L-shaped corner brackets
            draw.line([(x, y), (x + reticle_size, y)], fill=hud_green, width=3)
            draw.line([(x, y), (x, y + reticle_size)], fill=hud_green, width=3)
        
        # Advanced telemetry display (left side)
        telemetry_data = [
            f"FRAME: {frame_number:02d}" if frame_number != 'CENTER' else "FRAME: CTR",
            f"BEARING: {angle}°" if angle != 'overhead' else "BEARING: 000°",
            f"LAT: {lat:.6f}",
            f"LON: {lon:.6f}",
            "ALT: 120m AGL",
            "SPD: 5.2 m/s",
            "HDG: 045°",
            "BATT: 78%",
            "GPS: LOCK",
            "SAT: 12",
            "RSSI: -45dB",
            "TEMP: 12°C"
        ]
        
        # Draw telemetry background
        draw.rectangle([(10, 80), (220, 80 + len(telemetry_data) * 22 + 10)], 
                      fill=(0, 0, 0, 180))
        
        # Draw telemetry text
        y_pos = 90
        for line in telemetry_data:
            draw.text((20, y_pos), line, fill=hud_green, font=font_small)
            y_pos += 22
        
        # Mission status (top right)
        status_lines = [
            "RECON MISSION ACTIVE",
            "TARGET: VALLEY HOUSE",
            "STATUS: OPERATIONAL",
            "MODE: AUTO SURVEY"
        ]
        
        # Calculate position for right-aligned text
        max_width = max([draw.textbbox((0, 0), line, font=font_small)[2] for line in status_lines])
        status_x = img.width - max_width - 20
        
        # Draw status background
        draw.rectangle([(status_x - 10, 20), (img.width - 10, 20 + len(status_lines) * 22 + 10)], 
                      fill=(0, 0, 0, 180))
        
        # Draw status text
        y_pos = 30
        for line in status_lines:
            draw.text((status_x, y_pos), line, fill=warning_amber, font=font_small)
            y_pos += 22
        
        # Target identification (bottom center)
        target_text = "🎯 THE VALLEY HOUSE - ACHILL ISLAND"
        bbox = draw.textbbox((0, 0), target_text, font=font_medium)
        text_width = bbox[2] - bbox[0]
        target_x = img.width // 2 - text_width // 2
        
        # Target background
        draw.rectangle([(target_x - 10, img.height - 60), (target_x + text_width + 10, img.height - 30)], 
                      fill=(0, 0, 0, 180))
        draw.text((target_x, img.height - 55), target_text, fill=info_cyan, font=font_medium)
        
        # Coordinates display (bottom left)
        coord_text = f"COORDS: {lat:.4f}, {lon:.4f}"
        draw.rectangle([(10, img.height - 40), (250, img.height - 10)], fill=(0, 0, 0, 180))
        draw.text((20, img.height - 35), coord_text, fill=info_cyan, font=font_small)
        
        # Time stamp (bottom right)
        timestamp = time.strftime("%H:%M:%S UTC")
        time_text = f"TIME: {timestamp}"
        bbox = draw.textbbox((0, 0), time_text, font=font_small)
        time_width = bbox[2] - bbox[0]
        draw.rectangle([(img.width - time_width - 20, img.height - 40), (img.width - 10, img.height - 10)], 
                      fill=(0, 0, 0, 180))
        draw.text((img.width - time_width - 15, img.height - 35), time_text, fill=hud_green, font=font_small)
        
        # Save enhanced image
        hud_path = image_path.replace('.jpg', '_hud.jpg')
        img.save(hud_path, 'JPEG', quality=95)
        
        return hud_path
        
    except Exception as e:
        print(f"Error adding HUD overlay: {e}")
        return image_path

def create_professional_viewer(output_dir, frames, lat, lon):
    """Create professional HTML viewer for Google Maps flyover"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Maps Drone Flyover - The Valley House</title>
    <style>
        body {{
            font-family: 'Consolas', 'Courier New', monospace;
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ff00;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            background: rgba(0,0,0,0.9);
            border: 3px solid #00ff00;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 0 40px rgba(0,255,0,0.4);
        }}
        .title {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 0 0 20px #00ff00;
        }}
        .subtitle {{
            font-size: 1.5em;
            color: #ffff00;
            margin: 10px 0;
        }}
        .quality-badge {{
            background: linear-gradient(45deg, #ff6b00, #ff8e00);
            color: #000;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 10px;
        }}
        .viewer-section {{
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .image-viewer {{
            background: rgba(0,0,0,0.8);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        .drone-image {{
            max-width: 100%;
            max-height: 700px;
            border: 3px solid #00ff00;
            border-radius: 10px;
            box-shadow: 0 0 30px rgba(0,255,0,0.6);
            transition: all 0.3s ease;
        }}
        .drone-image:hover {{
            box-shadow: 0 0 50px rgba(0,255,0,0.8);
        }}
        .controls-panel {{
            background: rgba(0,0,0,0.9);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
        }}
        .control-group {{
            margin-bottom: 25px;
        }}
        .control-group h3 {{
            color: #ffff00;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        .btn {{
            background: linear-gradient(45deg, #00ff00, #00cc00);
            color: #000;
            border: none;
            padding: 12px 15px;
            margin: 3px;
            cursor: pointer;
            font-family: inherit;
            font-weight: bold;
            border-radius: 8px;
            transition: all 0.3s;
            width: 100%;
            font-size: 14px;
        }}
        .btn:hover {{
            background: linear-gradient(45deg, #ffff00, #ffcc00);
            box-shadow: 0 0 15px rgba(255,255,0,0.7);
            transform: translateY(-2px);
        }}
        .btn.active {{
            background: linear-gradient(45deg, #ff0000, #cc0000);
            color: #fff;
        }}
        .play-btn {{
            background: linear-gradient(45deg, #ffff00, #ffaa00);
            font-size: 16px;
            padding: 15px;
        }}
        .telemetry {{
            background: rgba(0,20,0,0.8);
            border: 1px solid #00ff00;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            font-size: 12px;
            line-height: 1.8;
        }}
        .status-good {{ color: #00ff00; }}
        .status-warning {{ color: #ffff00; }}
        .status-critical {{ color: #ff6600; }}
        .coordinates {{ color: #00ffff; }}
        .footer {{
            background: rgba(0,0,0,0.9);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 25px;
            text-align: center;
        }}
        .api-info {{
            background: rgba(0,30,60,0.8);
            border: 2px solid #0099ff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .api-info h4 {{
            color: #0099ff;
            margin-top: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🚁 GOOGLE MAPS DRONE FLYOVER</h1>
            <h2 class="subtitle">The Valley House - Achill Island, Ireland</h2>
            <div class="quality-badge">HIGH QUALITY SATELLITE IMAGERY</div>
            <div class="quality-badge">800x800 RESOLUTION</div>
            <p class="coordinates">Target Coordinates: {lat:.6f}, {lon:.6f}</p>
        </div>
        
        <div class="viewer-section">
            <div class="image-viewer">
                <img id="droneImage" class="drone-image" src="gmaps_frame_01_satellite_hud.jpg" 
                     alt="Drone Flyover View" onerror="handleImageError(this)">
                <div style="margin-top: 15px; color: #ffff00;">
                    <strong>Current View: </strong><span id="currentView">Frame 1</span>
                </div>
            </div>
            
            <div class="controls-panel">
                <div class="control-group">
                    <h3>🎮 PLAYBACK CONTROLS</h3>
                    <button class="btn play-btn" onclick="playFlyover()">▶️ PLAY FLYOVER</button>
                    <button class="btn" onclick="stopFlyover()">⏹️ STOP</button>
                    <button class="btn" onclick="previousFrame()">⬅️ PREVIOUS</button>
                    <button class="btn" onclick="nextFrame()">➡️ NEXT</button>
                </div>
                
                <div class="control-group">
                    <h3>📸 FRAME SELECTION</h3>"""
    
    # Add frame buttons
    regular_frames = [f for f in frames if f['frame'] != 'center']
    for frame in regular_frames:
        html_content += f'<button class="btn" onclick="showFrame({frame["frame"]})">Frame {frame["frame"]} ({frame["angle"]}°)</button>\n'
    
    if any(f['frame'] == 'center' for f in frames):
        html_content += '<button class="btn" onclick="showCenter()">📍 CENTER OVERHEAD</button>\n'
    
    html_content += f"""
                </div>
                
                <div class="telemetry">
                    <h4 style="color: #ffff00; margin-top: 0;">📊 MISSION TELEMETRY</h4>
                    <strong>Mission:</strong> Reconnaissance Survey<br>
                    <strong>Target:</strong> The Valley House<br>
                    <strong>Location:</strong> Achill Island, Ireland<br>
                    <strong>Frames Captured:</strong> {len(frames)}<br>
                    <strong>Coverage:</strong> 400m radius<br>
                    <strong>Altitude:</strong> <span class="status-good">120m AGL</span><br>
                    <strong>GPS Status:</strong> <span class="status-good">LOCKED</span><br>
                    <strong>Battery:</strong> <span class="status-warning">78%</span><br>
                    <strong>Signal:</strong> <span class="status-good">STRONG</span><br>
                    <strong>Weather:</strong> <span class="status-good">CLEAR</span><br>
                </div>
            </div>
        </div>
        
        <div class="api-info">
            <h4>🗺️ Google Maps Integration</h4>
            <p>This simulation uses Google Maps Static API for ultra-high quality satellite imagery. 
            The 800x800 resolution with scale=2 provides exceptional detail for professional reconnaissance.</p>
            
            <p><strong>Image Quality:</strong> Professional grade satellite imagery<br>
            <strong>Resolution:</strong> 800x800 pixels (High-DPI ready)<br>
            <strong>Zoom Levels:</strong> 18-19 (Maximum detail)<br>
            <strong>Update Frequency:</strong> Google's latest satellite data</p>
            
            <div style="background: rgba(255,100,0,0.1); padding: 10px; border-radius: 5px; margin-top: 15px;">
                <strong style="color: #ff6600;">⚠️ API Key Required for Production:</strong><br>
                Get unlimited access at <a href="https://console.cloud.google.com/google/maps-apis" 
                style="color: #00ffff;">Google Cloud Console</a>
            </div>
        </div>
        
        <div class="footer">
            <h3>🎯 EXPOSURE SOLUTIONS RECON AGENT</h3>
            <p>Professional reconnaissance capabilities with Google Maps integration</p>
            <p style="color: #999;">Satellite imagery © Google, Data © Google Maps</p>
        </div>
    </div>

    <script>
        let currentFrame = 1;
        let flyoverInterval = null;
        let totalFrames = {len(regular_frames)};
        
        const frameData = {json.dumps([{'frame': f['frame'], 'angle': f['angle']} for f in regular_frames])};
        
        function handleImageError(img) {{
            // Try base image if HUD version fails
            if (img.src.includes('_hud.jpg')) {{
                img.src = img.src.replace('_hud.jpg', '.jpg');
            }} else {{
                img.alt = 'Image not available';
                img.style.background = '#333';
            }}
        }}
        
        function showFrame(frameNum) {{
            currentFrame = frameNum;
            document.getElementById('droneImage').src = `gmaps_frame_${{frameNum.toString().padStart(2, '0')}}_satellite_hud.jpg`;
            document.getElementById('currentView').textContent = `Frame ${{frameNum}}`;
            
            // Update telemetry
            const frameInfo = frameData.find(f => f.frame === frameNum);
            if (frameInfo) {{
                console.log(`Showing frame ${{frameNum}} at ${{frameInfo.angle}}°`);
            }}
        }}
        
        function showCenter() {{
            document.getElementById('droneImage').src = 'gmaps_center_satellite_hud.jpg';
            document.getElementById('currentView').textContent = 'Center Overhead';
        }}
        
        function nextFrame() {{
            if (currentFrame < totalFrames) {{
                showFrame(currentFrame + 1);
            }} else {{
                showFrame(1);
            }}
        }}
        
        function previousFrame() {{
            if (currentFrame > 1) {{
                showFrame(currentFrame - 1);
            }} else {{
                showFrame(totalFrames);
            }}
        }}
        
        function playFlyover() {{
            if (flyoverInterval) return;
            
            flyoverInterval = setInterval(() => {{
                nextFrame();
            }}, 2500);
        }}
        
        function stopFlyover() {{
            if (flyoverInterval) {{
                clearInterval(flyoverInterval);
                flyoverInterval = null;
            }}
        }}
        
        // Initialize
        showFrame(1);
        
        // Auto-demo
        setTimeout(() => {{
            console.log('Google Maps Flyover Ready');
        }}, 1000);
    </script>
</body>
</html>"""
    
    # Save professional viewer
    viewer_path = os.path.join(output_dir, 'google_maps_flyover.html')
    with open(viewer_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return viewer_path

if __name__ == "__main__":
    create_google_maps_flyover()
