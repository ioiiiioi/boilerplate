# TODO: This function is defined but never used in the codebase - remove if not needed

def merge_response_dicts(*response_dicts):
    """
    Merge multiple response dictionaries into a single dictionary.

    Args:
        *response_dicts: Multiple dictionaries containing response structures.

    Returns:
        dict: A merged dictionary containing all responses.
    """
    combined_responses = {}
    for response_dict in response_dicts:
        combined_responses.update(response_dict)  # Merge dictionaries dynamically
    return combined_responses