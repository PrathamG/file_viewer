import os

# Create the main directory
main_dir = 'test_directory'
os.makedirs(main_dir, exist_ok=True)

# Create 1000 subdirectories
for i in range(1, 1001):
    os.makedirs(os.path.join(main_dir, f'subdir_{i}'), exist_ok=True)

print("1000 subdirectories created in test_directory.")