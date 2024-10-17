import difflib

def compare_metadata(metadata1, metadata2):
    diff_results = {}
    
    for metadata_type in metadata1.keys():
        diff_results[metadata_type] = []
        
        # Check for items in metadata1 that are not in metadata2
        for name, content in metadata1[metadata_type].items():
            if name not in metadata2[metadata_type]:
                diff_results[metadata_type].append({
                    "name": name,
                    "status": "Deleted",
                    "details": "Item exists in Org 1 but not in Org 2"
                })
            else:
                # Compare content
                differences = compare_content(content, metadata2[metadata_type][name])
                if differences:
                    diff_results[metadata_type].append({
                        "name": name,
                        "status": "Modified",
                        "details": differences
                    })
        
        # Check for items in metadata2 that are not in metadata1
        for name in metadata2[metadata_type].keys():
            if name not in metadata1[metadata_type]:
                diff_results[metadata_type].append({
                    "name": name,
                    "status": "Added",
                    "details": "Item exists in Org 2 but not in Org 1"
                })
    
    return diff_results

def compare_content(content1, content2):
    differences = []
    for key in set(content1.keys()) | set(content2.keys()):
        if key not in content1:
            differences.append(f"Field '{key}' added in Org 2")
        elif key not in content2:
            differences.append(f"Field '{key}' removed in Org 2")
        elif content1[key] != content2[key]:
            if isinstance(content1[key], dict) and isinstance(content2[key], dict):
                nested_diff = compare_content(content1[key], content2[key])
                if nested_diff:
                    differences.extend([f"{key}: {diff}" for diff in nested_diff])
            else:
                differences.append(f"Field '{key}' changed: '{content1[key]}' -> '{content2[key]}'")
    
    return differences
