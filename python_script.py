import pandas as pd
from pathlib import Path
from glob import glob

import cv2
import matplotlib.pyplot as plt
import tifffile

# Set your folder path
folder_path = r"C:\Users\YourUsername\Documents\YourFolder" 

print("COLLECTING IMAGE FILES")

# Collect all TIF files
tif_files = glob(f"{folder_path}/**/*.tif", recursive=True)

# Collect all PNG files
png_files = glob(f"{folder_path}/**/*.png", recursive=True)

# Collect all CSV files
csv_files = glob(f"{folder_path}/**/*.csv", recursive=True)

print(f"\nFound {len(tif_files)} TIF files")
print(f"Found {len(png_files)} PNG files")
print(f"Found {len(csv_files)} CSV files")

# Display image file paths
if tif_files:
    print(f"\nFirst few TIF files:")
    for f in tif_files[:3]:
        print(f"  - {Path(f).name}")

if png_files:
    print(f"\nFirst few PNG files:")
    for f in png_files[:3]:
        print(f"  - {Path(f).name}")

print("READING IMAGES")

# Read and display first image if available
all_image_files = tif_files + png_files

if all_image_files:
    print(f"\nReading first image: {Path(all_image_files[0]).name}")
    
    # Read TIFF files with tifffile, PNG with OpenCV
    if all_image_files[0].lower().endswith('.tif'):
        try:
            img_tif = tifffile.imread(all_image_files[0])
            print(f"Tifffile shape: {img_tif.shape}")
            print(f"Data type: {img_tif.dtype}")
            
            # Show statistics
            print(f"\nImage statistics:")
            print(f"  Min pixel value: {img_tif.min()}")
            print(f"  Max pixel value: {img_tif.max()}")
            print(f"  Mean pixel value: {img_tif.mean():.2f}")
            
            if len(img_tif.shape) == 3:
                print(f"\nHyperspectral info:")
                print(f"  Height: {img_tif.shape[0]} pixels")
                print(f"  Width: {img_tif.shape[1]} pixels")
                print(f"  Spectral bands: {img_tif.shape[2]}")
        except Exception as e:
            print(f"Tifffile couldn't read: {e}")
    else:
        # PNG files
        img_cv2 = cv2.imread(all_image_files[0], cv2.IMREAD_UNCHANGED)
        if img_cv2 is not None:
            print(f"OpenCV shape: {img_cv2.shape}")
            print(f"Data type: {img_cv2.dtype}")
            
            print(f"\nImage statistics:")
            print(f"  Min pixel value: {img_cv2.min()}")
            print(f"  Max pixel value: {img_cv2.max()}")
            print(f"  Mean pixel value: {img_cv2.mean():.2f}")
            
            # Also try matplotlib
            try:
                img_mpl = plt.imread(all_image_files[0])
                print(f"\nMatplotlib shape: {img_mpl.shape}")
                print(f"Data type (mpl): {img_mpl.dtype}")
            except Exception as e:
                print(f"\nMatplotlib couldn't read: {e}")
        else:
            print(f"OpenCV couldn't load the image")

print("READING ALL FILES (DETAILED)")

file_count = 0

# Loop over all files
for item in Path(folder_path).rglob('*'):
    
    # Check if it's a file and not a folder
    if item.is_file():
        file_count += 1
        
        # Handle CSV files with pandas
        if item.suffix == '.csv':
            try:
                print(f"\nFile #{file_count}: {item.name} [CSV]")
                
                # Read CSV with pandas
                df = pd.read_csv(item)
                
                print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
                print(f"  Columns: {list(df.columns)}")
                print(f"\n  Preview:")
                print(df.head(3))  # Show first 3 rows
                
            except Exception as e:
                print(f"\nFile #{file_count}: {item.name} - Could not read: {e}")
        
        # Handle TIF files
        elif item.suffix.lower() == '.tif':
            try:
                print(f"\nFile #{file_count}: {item.name} [TIFF Image]")
                
                # Read TIFF with tifffile
                img = tifffile.imread(str(item))
                
                if img is not None:
                    if len(img.shape) == 3:
                        print(f"  Dimensions: {img.shape[1]}x{img.shape[0]} pixels")
                        print(f"  Spectral bands: {img.shape[2]}")
                    else:
                        print(f"  Dimensions: {img.shape[1]}x{img.shape[0]} pixels")
                        print(f"  Channels: 1 (grayscale)")
                    print(f"  Data type: {img.dtype}")
                    print(f"  File size: {item.stat().st_size / 1024:.2f} KB")
                else:
                    print(f"  Could not load image data")
                
            except Exception as e:
                print(f"\nFile #{file_count}: {item.name} - Could not read: {e}")
        
        # Handle PNG files
        elif item.suffix.lower() == '.png':
            try:
                print(f"\nFile #{file_count}: {item.name} [PNG Image]")
                
                # Read PNG with OpenCV
                img = cv2.imread(str(item), cv2.IMREAD_UNCHANGED)
                
                if img is not None:
                    print(f"  Dimensions: {img.shape[1]}x{img.shape[0]} pixels")
                    print(f"  Channels: {img.shape[2] if len(img.shape) == 3 else 1}")
                    print(f"  Data type: {img.dtype}")
                    print(f"  File size: {item.stat().st_size / 1024:.2f} KB")
                else:
                    print(f"  Could not load image data")
                
            except Exception as e:
                print(f"\nFile #{file_count}: {item.name} - Could not read: {e}")
        
        # Handle regular text files
        else:
            try:
                # Read the file
                with open(item, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Print what we read
                    print(f"\nFile #{file_count}: {item.name}")
                    print(f"  Size: {len(content)} characters")
                    print(f"  First 100 chars: {content[:100]}")
                    
            except Exception as e:
                # Handle errors (binary files, permission issues, etc.)
                print(f"\nFile #{file_count}: {item.name} - Could not read: {e}")
                print("-" * 60)

print(f"FINISHED! Read {file_count} files total.")
