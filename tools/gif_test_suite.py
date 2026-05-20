""" gif tester module """
from pathlib import Path
from PIL import Image

def is_gif(file_input: Path) -> Path | None:
    """ Test if an image is a gif.
    Returns the path if true, None if not. """
    try:
        with Image.open(file_input) as gif:
            _ = gif.n_frames
        return file_input
    except Exception:
        return None

def gif_tester(paths: list[Path]) -> list[Path]:
    """ Pass a list of filepaths to test.
    Uses `ThreadPoolExecutor`. """
    valid = []
    import concurrent.futures as CF
    with CF.ThreadPoolExecutor() as executor:
        futures = [executor.submit(is_gif, g) for g in paths]
        for result in CF.as_completed(futures):
            gif_path = result.result()
            if gif_path is not None:
                valid.append(gif_path)
    return valid