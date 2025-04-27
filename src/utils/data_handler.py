def get_data_points(input_data):
    """
    Parses the user input data and converts it into a list of tuples.
    
    Args:
        input_data (str): A string of comma-separated values representing data points.
        
    Returns:
        list: A list of tuples containing the data points as floats.
    """
    try:
        data_points = [tuple(map(float, point.split(','))) for point in input_data.split(';')]
        return data_points
    except ValueError:
        raise ValueError("Invalid input format. Please enter data points as 'x,y;x,y;...'.")

def format_data_for_ahc(data_points):
    """
    Formats the data points for processing by the AHC algorithm.
    
    Args:
        data_points (list): A list of tuples containing the data points.
        
    Returns:
        np.ndarray: A NumPy array of the data points.
    """
    import numpy as np
    return np.array(data_points)

def save_data_to_file(data_points, filename):
    """
    Saves the data points to a specified file.
    
    Args:
        data_points (list): A list of tuples containing the data points.
        filename (str): The name of the file to save the data points.
    """
    import json
    with open(filename, 'w') as file:
        json.dump(data_points, file)

def load_data_from_file(filename):
    """
    Loads data points from a specified file.
    
    Args:
        filename (str): The name of the file to load the data points from.
        
    Returns:
        list: A list of tuples containing the data points.
    """
    import json
    with open(filename, 'r') as file:
        data_points = json.load(file)
    return [tuple(point) for point in data_points]