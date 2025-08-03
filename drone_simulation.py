#!/usr/bin/env python3
"""
Drone Simulation Module
Enhanced satellite imagery and professional HUD overlays
"""

import os
import requests
import time
import json
from math import cos, sin, radians
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from typing import Dict, List, Any, Optional

class DroneSimulator:
    """Professional drone flyover simulation system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Exposure Solutions Drone Simulator v2.0'
        })
    
    def create_simulation(self, poi_name: str, location: str) -> Dict[str, Any]:
        """Create complete drone simulation"""
        try:
            # Get coordinates for the location
            coordinates = self.geocode_location(poi_name, location)
            if not coordinates:
                return {'status': 'error', 'error': 'Could not geocode location'}
            
            lat, lon = coordinates['lat'], coordinates['lon']
            
            # Create output directory
            output_dir = f"drone_simulation_{poi_name.replace(' ', '_').lower()}"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate satellite imagery sequence
            frames = self.generate_satellite_sequence(lat, lon, output_dir)
            
            # Create interactive HTML viewer
            html_path = self.create_interactive_viewer(output_dir, frames, poi_name, lat, lon)
            
            return {
                'status': 'success',
                'frames': frames,
                'html_viewer': html_path,
                'output_directory': output_dir,
                'coordinates': coordinates
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def geocode_location(self, poi_name: str, location: str) -> Optional[Dict[str, float]]:
        """Geocode location to coordinates"""
        try:
            # Try multiple geocoding services
            services = [
                f"https://nominatim.openstreetmap.org/search?q={poi_name} {location}&format=json&limit=1",
                f"https://api.mapbox.com/geocoding/v5/mapbox.places/{poi_name} {location}.json"
            ]
            
            for service_url in services:
                try:
                    response = self.session.get(service_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            if 'nominatim' in service_url:
                                return {'lat': float(data[0]['lat']), 'lon': float(data[0]['lon'])}
                            elif 'mapbox' in service_url:
                                coords = data['features'][0]['geometry']['coordinates']
                                return {'lat': coords[1], 'lon': coords[0]}
                except:
                    continue
            
            # Fallback to default Achill Island coordinates
            return {'lat': 53.9889, 'lon': -10.0661}
            
        except Exception as e:
            return {'lat': 53.9889, 'lon': -10.0661}  # Default fallback
    
    def generate_satellite_sequence(self, lat: float, lon: float, output_dir: str) -> List[Dict[str, Any]]:
        """Generate sequence of satellite images"""
        frames = []
        radius_km = self.config.get('drone_simulation', {}).get('coverage_radius_km', 0.35)
        frame_count = self.config.get('drone_simulation', {}).get('frame_count', 6)
        
        for i in range(frame_count):
            angle_deg = i * (360 / frame_count)
            angle_rad = radians(angle_deg)
            
            # Calculate offset coordinates
            lat_offset = radius_km * cos(angle_rad) / 111.32
            lon_offset = radius_km * sin(angle_rad) / (111.32 * cos(radians(lat)))
            
            view_lat = lat + lat_offset
            view_lon = lon + lon_offset
            
            # Get satellite image
            image_path = self.get_satellite_image(view_lat, view_lon, output_dir, i + 1)
            
            if image_path:
                # Enhance image
                enhanced_path = self.enhance_image(image_path)
                
                # Add professional HUD
                hud_path = self.add_professional_hud(enhanced_path, i + 1, angle_deg, view_lat, view_lon)
                
                frames.append({
                    'frame': i + 1,
                    'angle': angle_deg,
                    'lat': view_lat,
                    'lon': view_lon,
                    'base_path': image_path,
                    'enhanced_path': enhanced_path,
                    'hud_path': hud_path
                })
        
        # Add center overhead view
        center_path = self.get_satellite_image(lat, lon, output_dir, 'center', zoom=18)
        if center_path:
            enhanced_center = self.enhance_image(center_path)
            hud_center = self.add_professional_hud(enhanced_center, 'CENTER', 'overhead', lat, lon)
            
            frames.append({
                'frame': 'center',
                'angle': 'overhead',
                'lat': lat,
                'lon': lon,
                'base_path': center_path,
                'enhanced_path': enhanced_center,
                'hud_path': hud_center
            })
        
        return frames
    
    def get_satellite_image(self, lat: float, lon: float, output_dir: str, frame_id: Any, zoom: int = 17) -> Optional[str]:
        """Get satellite image from best available source"""
        # Calculate tile coordinates
        import math
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        xtile = int((lon + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        
        # Try multiple high-quality sources
        sources = [
            f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{ytile}/{xtile}",
            f"https://mt1.google.com/vt/lyrs=s&x={xtile}&y={ytile}&z={zoom}",
            f"https://tile.openstreetmap.org/{zoom}/{xtile}/{ytile}.png"
        ]
        
        for source_url in sources:
            try:
                response = self.session.get(source_url, timeout=10)
                if response.status_code == 200 and len(response.content) > 1000:
                    # Save image
                    image_path = os.path.join(output_dir, f'frame_{frame_id}_satellite.jpg')
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    return image_path
            except:
                continue
        
        return None
    
    def enhance_image(self, image_path: str) -> str:
        """Enhance satellite image quality"""
        try:
            img = Image.open(image_path)
            
            # Enhance contrast, sharpness, and color
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.3)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
            
            # Resize for better quality
            img = img.resize((800, 800), Image.Resampling.LANCZOS)
            
            # Save enhanced version
            enhanced_path = image_path.replace('.jpg', '_enhanced.jpg')
            img.save(enhanced_path, 'JPEG', quality=95)
            
            return enhanced_path
            
        except Exception as e:
            return image_path
    
    def add_professional_hud(self, image_path: str, frame_number: Any, angle: Any, lat: float, lon: float) -> str:
        """Add professional military-style HUD overlay"""
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # Load fonts
            try:
                font_large = ImageFont.truetype("arial.ttf", 28)
                font_medium = ImageFont.truetype("arial.ttf", 20)
                font_small = ImageFont.truetype("arial.ttf", 16)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Professional colors
            hud_green = (0, 255, 0)
            amber = (255, 191, 0)
            red = (255, 0, 0)
            cyan = (0, 255, 255)
            
            # Advanced targeting system
            center_x, center_y = img.width // 2, img.height // 2
            
            # Main targeting reticle
            reticle_size = 60
            draw.ellipse([(center_x-reticle_size, center_y-reticle_size), 
                         (center_x+reticle_size, center_y+reticle_size)], 
                        outline=red, width=3)
            
            # Crosshairs
            draw.line([(center_x-80, center_y), (center_x+80, center_y)], fill=red, width=4)
            draw.line([(center_x, center_y-80), (center_x, center_y+80)], fill=red, width=4)
            
            # Range markers
            for i in range(20, 101, 20):
                draw.ellipse([(center_x-i, center_y-i), (center_x+i, center_y+i)], 
                            outline=hud_green, width=1)
            
            # Corner HUD elements
            corner_size = 40
            corners = [(50, 50), (img.width-90, 50), (50, img.height-90), (img.width-90, img.height-90)]
            
            for x, y in corners:
                draw.line([(x, y), (x+corner_size, y)], fill=hud_green, width=4)
                draw.line([(x, y), (x, y+corner_size)], fill=hud_green, width=4)
            
            # Telemetry panel
            self.draw_telemetry_panel(draw, img, frame_number, angle, lat, lon, font_small, hud_green, amber)
            
            # Target information
            self.draw_target_panel(draw, img, font_medium, cyan)
            
            # Status bar
            self.draw_status_bar(draw, img, lat, lon, font_small, hud_green, cyan)
            
            # Save HUD version
            hud_path = image_path.replace('.jpg', '_hud.jpg')
            img.save(hud_path, 'JPEG', quality=98)
            
            return hud_path
            
        except Exception as e:
            return image_path
    
    def draw_telemetry_panel(self, draw, img, frame_number, angle, lat, lon, font, hud_green, amber):
        """Draw telemetry information panel"""
        panel_x, panel_y = 20, 120
        panel_width, panel_height = 280, 400
        
        # Background
        draw.rectangle([(panel_x, panel_y), (panel_x+panel_width, panel_y+panel_height)], 
                      fill=(0, 0, 0, 200), outline=hud_green, width=2)
        
        # Header
        draw.rectangle([(panel_x+2, panel_y+2), (panel_x+panel_width-2, panel_y+35)], 
                      fill=(0, 50, 0, 180))
        draw.text((panel_x+10, panel_y+8), "MISSION DATA", fill=amber, font=font)
        
        # Telemetry data
        telemetry = [
            f"FRAME: {frame_number:02d}" if frame_number != 'CENTER' else "FRAME: CTR",
            f"BEARING: {angle:03.0f}°" if angle != 'overhead' else "BEARING: 000°",
            f"LAT: {lat:.6f}",
            f"LON: {lon:.6f}",
            "ALT: 120m AGL",
            "SPD: 5.2 m/s",
            "HDG: 045° MAG",
            "GPS: LOCKED",
            "BATT: 78%",
            "TEMP: 12°C"
        ]
        
        y_pos = panel_y + 45
        for line in telemetry:
            draw.text((panel_x+15, y_pos), line, fill=hud_green, font=font)
            y_pos += 20
    
    def draw_target_panel(self, draw, img, font, cyan):
        """Draw target information panel"""
        target_text = "🎯 ACHILL ISLAND RECONNAISSANCE"
        bbox = draw.textbbox((0, 0), target_text, font=font)
        text_width = bbox[2] - bbox[0]
        target_x = img.width // 2 - text_width // 2
        
        # Background
        draw.rectangle([(target_x - 10, img.height - 60), (target_x + text_width + 10, img.height - 30)], 
                      fill=(0, 0, 0, 180))
        draw.text((target_x, img.height - 55), target_text, fill=cyan, font=font)
    
    def draw_status_bar(self, draw, img, lat, lon, font, hud_green, cyan):
        """Draw status bar at bottom"""
        status_y = img.height - 100
        draw.rectangle([(20, status_y), (img.width-20, img.height-70)], 
                      fill=(0, 0, 0, 200), outline=hud_green, width=2)
        
        coord_text = f"COORDS: {lat:.4f}, {lon:.4f}"
        time_text = f"TIME: {time.strftime('%H:%M:%S UTC')}"
        
        draw.text((30, status_y+10), coord_text, fill=cyan, font=font)
        
        # Right-align time
        bbox = draw.textbbox((0, 0), time_text, font=font)
        time_width = bbox[2] - bbox[0]
        draw.text((img.width - time_width - 30, status_y+10), time_text, fill=hud_green, font=font)
    
    def create_interactive_viewer(self, output_dir: str, frames: List[Dict], poi_name: str, lat: float, lon: float) -> str:
        """Create interactive HTML viewer"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone Simulation - {poi_name}</title>
    <style>
        body {{
            font-family: 'Consolas', monospace;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
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
            text-shadow: 0 0 20px #00ff00;
            margin-bottom: 15px;
        }}
        .viewer-section {{
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 30px;
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
        }}
        .controls {{
            background: rgba(0,0,0,0.9);
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
        }}
        .btn {{
            background: linear-gradient(45deg, #00ff00, #00cc00);
            color: #000;
            border: none;
            padding: 12px;
            margin: 3px 0;
            width: 100%;
            cursor: pointer;
            font-family: inherit;
            font-weight: bold;
            border-radius: 5px;
        }}
        .btn:hover {{
            background: linear-gradient(45deg, #ffff00, #ffcc00);
        }}
        .play-btn {{
            background: linear-gradient(45deg, #ffff00, #ffaa00);
            font-size: 16px;
            padding: 15px;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🚁 DRONE SIMULATION</h1>
            <h2>{poi_name}</h2>
            <p>Coordinates: {lat:.6f}, {lon:.6f}</p>
            <p>Game Integration: Achill AI Avengers - Island of Legends</p>
        </div>
        
        <div class="viewer-section">
            <div class="image-viewer">
                <img id="droneImage" class="drone-image" src="frame_1_satellite_enhanced_hud.jpg" alt="Drone View">
                <div style="margin-top: 15px; color: #ffff00;">
                    <strong>Current View:</strong> <span id="currentView">Frame 1</span>
                </div>
            </div>
            
            <div class="controls">
                <button class="btn play-btn" onclick="playFlyover()">▶️ PLAY FLYOVER</button>
                <button class="btn" onclick="stopFlyover()">⏹️ STOP</button>
                <button class="btn" onclick="previousFrame()">⬅️ PREVIOUS</button>
                <button class="btn" onclick="nextFrame()">➡️ NEXT</button>
                <hr style="border-color: #00ff00; margin: 20px 0;">"""
        
        # Add frame buttons
        regular_frames = [f for f in frames if f['frame'] != 'center']
        for frame in regular_frames:
            html_content += f'<button class="btn" onclick="showFrame({frame["frame"]})">Frame {frame["frame"]} ({frame["angle"]}°)</button>\n'
        
        if any(f['frame'] == 'center' for f in frames):
            html_content += '<button class="btn" onclick="showCenter()">📍 CENTER</button>\n'
        
        html_content += f"""
            </div>
        </div>
    </div>

    <script>
        let currentFrame = 1;
        let flyoverInterval = null;
        let totalFrames = {len(regular_frames)};
        
        function showFrame(frameNum) {{
            currentFrame = frameNum;
            document.getElementById('droneImage').src = `frame_${{frameNum}}_satellite_enhanced_hud.jpg`;
            document.getElementById('currentView').textContent = `Frame ${{frameNum}}`;
        }}
        
        function showCenter() {{
            document.getElementById('droneImage').src = 'frame_center_satellite_enhanced_hud.jpg';
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
    </script>
</body>
</html>"""
        
        html_path = os.path.join(output_dir, 'drone_simulation.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_path
