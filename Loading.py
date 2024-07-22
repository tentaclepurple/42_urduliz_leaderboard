import time
from time import sleep
import shutil


def format_time(seconds):
    """
    Format the given time in seconds as MM:SS.
    """
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{int(s):02d}"


def ft_tqdm(lst: range) -> None:
    """
    Simulates a progress bar for iterating over a range of items.

    This function emulates the behavior of tqdm by displaying
     a progress bar in the terminal.
    It shows the percentage of progress, a visual progress bar,
    the current iteration count,
    elapsed time, estimated time remaining (ETA),
    and iteration speed (items per second).

    Args:
        lst (range): The range of items to iterate over.

    Yields:
        Any: The current item from the range.
    """
    total = len(lst)
    start_time = time.time()

    console_width = shutil.get_terminal_size().columns - 30
    bar_width = console_width - 10

    for i, item in enumerate(lst, start=1):
        progress = int(i / total * bar_width)
        elapsed_time = time.time() - start_time
        speed = i / elapsed_time
        eta = (total - i) / speed

        elapsed_formatted = format_time(elapsed_time)
        eta_formatted = format_time(eta)

        progress_bar = f"|{'█' * progress:<{bar_width}}|"
        progress_percentage = progress * 100 // bar_width
        progress_info = f"{progress_percentage}%{progress_bar} {i}/{total}"
        time_info = f"[{elapsed_formatted}<{eta_formatted}, {speed:.2f}it/s]"

        print(f"\r{progress_info} {time_info}", end="", flush=True)
        yield item


def main():
    for elem in ft_tqdm(range(333)):
        sleep(0.005)
    print()


if __name__ == '__main__':
    main()
