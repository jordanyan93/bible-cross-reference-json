#!/usr/bin/env python3
"""
Bible Cross-Reference Merger
Merges multiple JSON files containing Bible verse cross-references into a single file.
Works on Windows, Mac, and Linux.
"""

import json
import os
from pathlib import Path

def merge_json_files(input_dir, output_file):
    """
    Merge all JSON files from input_dir into a single output file.
    
    Args:
        input_dir: Directory containing JSON files
        output_file: Path to output merged JSON file
    """
    merged_data = {}
    
    # Get all JSON files in the directory
    input_path = Path(input_dir)
    json_files = sorted(input_path.glob('*.json'))
    
    print(f"Found {len(json_files)} JSON files to merge")
    print(f"Looking in: {input_path.absolute()}")
    
    if len(json_files) == 0:
        print(f"\nNo JSON files found in: {input_path.absolute()}")
        print("Please check that:")
        print("  1. The directory path is correct")
        print("  2. There are .json files in the directory")
        return merged_data
    
    for json_file in json_files:
        print(f"Processing: {json_file.name}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Merge the data
                for verse_id, verse_data in data.items():
                    if verse_id in merged_data:
                        print(f"  Warning: Duplicate verse ID {verse_id} found in {json_file.name}")
                        # Merge references if they exist
                        if 'r' in verse_data and 'r' in merged_data[verse_id]:
                            merged_data[verse_id]['r'].update(verse_data['r'])
                    else:
                        merged_data[verse_id] = verse_data
                        
        except Exception as e:
            print(f"  Error processing {json_file.name}: {e}")
            continue
    
    # Count statistics
    total_verses = len(merged_data)
    total_references = sum(len(v.get('r', {})) for v in merged_data.values())
    
    print(f"\nMerge complete!")
    print(f"Total verses: {total_verses:,}")
    print(f"Total cross-references: {total_references:,}")
    
    # Save merged data
    print(f"\nSaving to: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, separators=(',', ':'))
        
        file_size_kb = os.path.getsize(output_file) / 1024
        print(f"Done! File size: {file_size_kb:.1f} KB")
    except Exception as e:
        print(f"Error saving file: {e}")
        return merged_data
    
    return merged_data

def analyze_data(merged_data):
    """Print some statistics about the merged data."""
    
    if not merged_data:
        print("\nNo data to analyze.")
        return
    
    # Parse verse references to get book information
    books = {}
    for verse_id, verse_data in merged_data.items():
        verse_ref = verse_data.get('v', '')
        if verse_ref:
            book = verse_ref.split()[0]
            if book not in books:
                books[book] = 0
            books[book] += 1
    
    print(f"\n=== Book Statistics ===")
    print(f"Total books: {len(books)}")
    print(f"\nTop 10 books by verse count:")
    for book, count in sorted(books.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {book}: {count} verses")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Look for JSON files in the same directory as the script
    input_directory = script_dir
    
    # Save the output in the same directory
    output_file = script_dir / "merged_bible_references.json"
    
    print("=" * 60)
    print("Bible Cross-Reference Merger")
    print("=" * 60)
    print(f"Script location: {script_dir.absolute()}")
    print(f"Looking for JSON files in: {input_directory.absolute()}")
    print(f"Output file will be: {output_file.absolute()}")
    print("=" * 60)
    print()
    
    merged_data = merge_json_files(input_directory, output_file)
    analyze_data(merged_data)
    
    print("\n" + "=" * 60)
    print("Complete!")
    print("=" * 60)