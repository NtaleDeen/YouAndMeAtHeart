import os
from PIL import Image, ImageDraw, ImageFont
import glob

def create_favicon_ico(input_path, output_dir):
    """Create .ico file with multiple standard sizes"""
    try:
        # Open and ensure RGBA mode for transparency
        img = Image.open(input_path).convert('RGBA')
        
        # Standard favicon sizes
        sizes = [16, 32, 48, 64, 128, 256]
        
        # Create resized versions
        icons = []
        for size in sizes:
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            icons.append(resized_img)
        
        # Save as .ico (supports multiple sizes in one file)
        ico_path = os.path.join(output_dir, 'favicon.ico')
        icons[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes], append_images=icons[1:])
        print(f"✅ Created: {ico_path}")
        
        # Also create individual PNG files for specific use cases
        for size in [16, 32, 180]:  # Common web sizes
            individual_path = os.path.join(output_dir, f'favicon-{size}x{size}.png')
            img.resize((size, size), Image.Resampling.LANCZOS).save(individual_path, 'PNG')
            print(f"✅ Created: {individual_path}")
            
    except Exception as e:
        print(f"❌ Error creating favicon for {input_path}: {e}")

def create_standard_logo_sizes(input_path, output_dir, logo_type):
    """Create standard logo sizes for web and print"""
    try:
        img = Image.open(input_path).convert('RGBA')
        
        # Standard web and organizational sizes
        sizes = {
            'small': (150, 150),      # Small web elements
            'medium': (300, 300),     # Medium web display
            'large': (600, 600),      # Large web display
            'header': (800, 200),     # Website header (maintains aspect ratio)
            'social': (1200, 630),    # Social media sharing
            'print_small': (300, 300), # Print materials small
            'print_large': (600, 600)  # Print materials large
        }
        
        for size_name, (width, height) in sizes.items():
            # Maintain aspect ratio for resizing
            if logo_type in ['long_logo', 'short_logo']:
                # For logos with text, maintain aspect ratio
                img_ratio = img.width / img.height
                target_ratio = width / height
                
                if img_ratio > target_ratio:
                    # Image is wider than target
                    new_height = int(width / img_ratio)
                    resized_img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                    # Create canvas with target size
                    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    # Center the image
                    y_offset = (height - new_height) // 2
                    canvas.paste(resized_img, (0, y_offset))
                    output_img = canvas
                else:
                    # Image is taller than target
                    new_width = int(height * img_ratio)
                    resized_img = img.resize((new_width, height), Image.Resampling.LANCZOS)
                    # Create canvas with target size
                    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    # Center the image
                    x_offset = (width - new_width) // 2
                    canvas.paste(resized_img, (x_offset, 0))
                    output_img = canvas
            else:
                # For favicon, simple resize
                output_img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            output_path = os.path.join(output_dir, f'{logo_type}_{size_name}.png')
            output_img.save(output_path, 'PNG', optimize=True)
            print(f"✅ Created: {output_path}")
            
    except Exception as e:
        print(f"❌ Error processing {logo_type}: {e}")

def create_apple_touch_icon(input_path, output_dir):
    """Create Apple Touch Icon (180x180 for iOS)"""
    try:
        img = Image.open(input_path).convert('RGBA')
        apple_icon = img.resize((180, 180), Image.Resampling.LANCZOS)
        apple_path = os.path.join(output_dir, 'apple-touch-icon.png')
        apple_icon.save(apple_path, 'PNG')
        print(f"✅ Created: {apple_path}")
    except Exception as e:
        print(f"❌ Error creating Apple touch icon: {e}")

def create_android_icons(input_path, output_dir):
    """Create Android app icons"""
    try:
        img = Image.open(input_path).convert('RGBA')
        android_sizes = {
            'android-chrome-192x192': 192,
            'android-chrome-512x512': 512,
        }
        
        for name, size in android_sizes.items():
            android_icon = img.resize((size, size), Image.Resampling.LANCZOS)
            android_path = os.path.join(output_dir, f'{name}.png')
            android_icon.save(android_path, 'PNG')
            print(f"✅ Created: {android_path}")
    except Exception as e:
        print(f"❌ Error creating Android icons: {e}")

def create_web_app_manifest(output_dir):
    """Create web app manifest for PWA compatibility"""
    manifest_content = {
        "name": "YouAndMeAtHeart Community Center",
        "short_name": "YouAndMeAtHeart",
        "description": "Building Community Through Connection",
        "icons": [
            {
                "src": "favicon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "favicon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "theme_color": "#e63946",
        "background_color": "#f1faee",
        "display": "standalone"
    }
    
    import json
    manifest_path = os.path.join(output_dir, 'site.webmanifest')
    with open(manifest_path, 'w') as f:
        json.dump(manifest_content, f, indent=2)
    print(f"✅ Created: {manifest_path}")

def main():
    # Create output directory
    output_dir = 'converted_logos'
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 Starting logo conversion for YouAndMeAtHeart...")
    print("=" * 50)
    
    # Define your input files (update these paths to match your actual files)
    logo_files = {
        'favicon': 'favicon_no_bg.png',
        'short_logo': 'short_logo_no_bg.png', 
        'long_logo': 'long_logo_no_bg.png'
    }
    
    # Check which files exist
    existing_logos = {}
    for logo_type, filename in logo_files.items():
        if os.path.exists(filename):
            existing_logos[logo_type] = filename
            print(f"📁 Found: {filename}")
        else:
            print(f"⚠️  Missing: {filename}")
    
    if not existing_logos:
        print("❌ No logo files found! Please ensure your PNG files are in the same directory.")
        return
    
    print("\n" + "=" * 50)
    
    # Process each logo type
    for logo_type, filename in existing_logos.items():
        print(f"\n🎨 Processing {logo_type}...")
        
        if logo_type == 'favicon':
            # Create favicon.ico and standard sizes
            create_favicon_ico(filename, output_dir)
            create_apple_touch_icon(filename, output_dir)
            create_android_icons(filename, output_dir)
        else:
            # Create standard logo sizes for short and long logos
            create_standard_logo_sizes(filename, output_dir, logo_type)
    
    # Create web app manifest
    create_web_app_manifest(output_dir)
    
    print("\n" + "=" * 50)
    print("🎉 Conversion complete!")
    print(f"📁 All files saved to: {output_dir}/")
    print("\n📋 Files created:")
    
    # List all created files
    created_files = glob.glob(os.path.join(output_dir, '*'))
    for file in sorted(created_files):
        file_size = os.path.getsize(file) / 1024  # Size in KB
        print(f"   📄 {os.path.basename(file)} ({file_size:.1f} KB)")
    
    print("\n🔗 HTML code for your website:")
    print("""
<!-- Favicon and App Icons -->
<link rel="icon" type="image/x-icon" href="converted_logos/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="converted_logos/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="converted_logos/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="converted_logos/apple-touch-icon.png">
<link rel="manifest" href="converted_logos/site.webmanifest">
    
<!-- Logo for header (use appropriate size) -->
<img src="converted_logos/short_logo_medium.png" alt="YouAndMeAtHeart" class="logo">
    """)

if __name__ == "__main__":
    # Check if PIL is installed
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow library is required. Install it with:")
        print("   pip install Pillow")
        exit(1)
    
    main()