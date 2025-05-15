import json

def load_config(file_path: str):
    """
    Load configuration from a JSON file.
    
    Args:
        file_path (str): Path to the JSON configuration file.
        
    Returns:
        dict: Configuration data as a dictionary.
    """
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config
