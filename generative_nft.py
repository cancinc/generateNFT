import os
import random
import hashlib
import argparse
from PIL import Image, ImageDraw, ImageFont

def generate_nft_images(prompt, image_size=(500, 500), num_images=10, output_dir="nft_images"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(num_images):
        # Combine prompt with image index to create a unique seed per image
        seed_str = f"{prompt}_{i}"
        seed = int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest(), 16) % (10**8)
        random.seed(seed)
        
        # Generate a random background color
        bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        img = Image.new("RGB", image_size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw a few random shapes
        for _ in range(5):
            shape_type = random.choice(["ellipse", "rectangle"])
            x0 = random.randint(0, image_size[0] - 1)
            y0 = random.randint(0, image_size[1] - 1)
            x1 = random.randint(x0, image_size[0])
            y1 = random.randint(y0, image_size[1])
            shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            if shape_type == "ellipse":
                draw.ellipse([x0, y0, x1, y1], outline=shape_color, width=3)
            else:
                draw.rectangle([x0, y0, x1, y1], outline=shape_color, width=3)
        
        # Overlay the prompt text as a signature
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        draw.text((10, 10), prompt, fill=(255, 255, 255), font=font)
        
        # Save the image
        img_path = os.path.join(output_dir, f"nft_{i+1}.png")
        img.save(img_path)
        print(f"Generated {img_path}")
    
    print(f"\nAll done! {num_images} NFT images have been saved in the '{output_dir}' folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generative NFT Art Creator")
    parser.add_argument("--prompt", type=str, required=False, default="Generative Art", help="The prompt to seed the NFT generator")
    args = parser.parse_args()
    
    generate_nft_images(args.prompt)
