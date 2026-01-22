import base64


def image_to_base64(image_path):
    """
    Converts an image file to a Base64 encoded string.
    """
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

            encoded_bytes = base64.b64encode(image_data)

            # Decode the bytes into a human-readable string using 'utf-8'
            base64_string = encoded_bytes.decode("utf-8")

            return base64_string
    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
