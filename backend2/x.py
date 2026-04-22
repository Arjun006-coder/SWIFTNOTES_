import os
import shutil

def merge_datasets(src1, src2, dest):
    for split in ['train', 'valid', 'test']:
        os.makedirs(f"{dest}/{split}/images", exist_ok=True)
        os.makedirs(f"{dest}/{split}/labels", exist_ok=True)
        
        # Copy Dataset 1 (Equations -> Class 0)
        for f in os.listdir(f"{src1}/{split}/images"):
            shutil.copy(f"{src1}/{split}/images/{f}", f"{dest}/{split}/images/math_{f}")
        for f in os.listdir(f"{src1}/{split}/labels"):
            shutil.copy(f"{src1}/{split}/labels/{f}", f"{dest}/{split}/labels/math_{f}")

        # Copy Dataset 2 (Code -> Class 1)
        for f in os.listdir(f"{src2}/{split}/images"):
            shutil.copy(f"{src2}/{split}/images/{f}", f"{dest}/{split}/images/code_{f}")
        
        # Rewrite labels for class offset
        for f in os.listdir(f"{src2}/{split}/labels"):
            with open(f"{src2}/{split}/labels/{f}", 'r') as file:
                lines = file.readlines()
            with open(f"{dest}/{split}/labels/code_{f}", 'w') as file:
                for line in lines:
                    parts = line.split()
                    parts[0] = '1' # Set class to 1
                    file.write(" ".join(parts) + "\n")

merge_datasets('Mathset', 'codeset', 'merged_dataset')