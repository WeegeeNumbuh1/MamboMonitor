# download Tenor gifs in batches
# this assumes the existence of a "links.txt" file
# with the desired URLs per line.
# by: WeegeeNumbuh1

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys
from time import perf_counter, sleep
from datetime import datetime
from tenor_downloader import fetch

print("===== Matikanetannhauser \"Mambo\" (and friends) Tenor gif downloader =====")
CURRENT_DIR = Path(__file__).resolve().parent
URL_LIST = Path(CURRENT_DIR.parent, 'links.txt')
SAVE_PATH = Path(CURRENT_DIR.parent, 'img_src')

if not URL_LIST.is_file():
    print(f"Could not find \'links.txt\' in \'{CURRENT_DIR.parent}\'")
    sys.exit(1)
if not SAVE_PATH.is_dir():
    print(f"Could not find \'{SAVE_PATH}\'")
    sys.exit(1)

start_date = datetime.now().strftime("%Y-%m-%dT%H%M%S")
url_list = []
with open(URL_LIST, 'r', encoding='utf-8') as urls:
    for line in urls:
        parsed = line.strip()
        if parsed.startswith('#'): # ignore comments
            continue
        if parsed:
            url_list.append(parsed)

url_count = len(url_list)
print(f"Parsed {url_count} line(s).")
if url_count == 0:
    print("No lines read, nothing to do. Exiting...")
    sys.exit(0)

main_threadpool = ThreadPoolExecutor(max_workers=10)
results_list = []
batchsize = 10
print("Starting in 10 seconds.")
print("Press Ctrl+C to stop/abort.")
sleep(10)
print("Beginning downloads... (this might take some time)")
start_time = perf_counter()
try:
    complete = 0
    for i in range(0, url_count, batchsize):
        batch = url_list[i:i + batchsize]
        futures = {main_threadpool.submit(fetch, url, SAVE_PATH): url for url in batch}
        for future in as_completed(futures):
            try:
                results_list.append(future.result(timeout=30))
            except Exception as e:
                print(f"Encountered an error: {e}")
        complete += len(batch)
        print(f"[{perf_counter() - start_time:.3f} sec] Completed batch "
              f"{i // batchsize + 1}: "
              f"({complete}/{url_count})")

except (KeyboardInterrupt, SystemExit):
    print("Download interrupted, exiting...")
    main_threadpool.shutdown(wait=False, cancel_futures=True)
    sys.exit(1)

print("\n=========== SUMMARY ===========")
result_len = len(results_list)
failcount = 0
total_downloaded = 0
for entry in results_list:
    if entry['failure'] is not None:
        failcount += 1
    if entry['size_MiB'] is not None:
        total_downloaded += entry['size_MiB']
string1 = (f"Successfully downloaded {result_len - failcount} out of {url_count} "
           f"({failcount} failed/skipped)")
string2 = (f"Saved {round(total_downloaded, 3)} MiB over {perf_counter() - start_time:.3f} seconds.")
print(string1)
print(string2)
date_now = datetime.now().strftime("%Y-%m-%dT%H%M%S")
logfile = Path(CURRENT_DIR.parent, f'download-log_[{date_now}].log')
print(f"Check the log at \'{logfile}\' for all the details.")
with open(logfile, 'w', encoding='utf-8') as log:
    log.write("===== Matikanetannhauser \"Mambo\" (and friends) Tenor gif downloader =====\n")
    log.write("By: WeegeeNumbuh1\n")
    log.write(f"Started on {start_date}\n")
    log.write(f"Downloads finished at {date_now}\n")
    log.write(string1)
    log.write("\n")
    log.write(string2)
    log.write("\n\n")
    for entry in results_list:
        log.write(f'{entry}\n')
print("""
⠄⠄⠄⠠⠄⢕⠱⠨⠪⣨⢢⢣⢓⣕⣕⢕⢜⢌⢎⢎⢎⢎⢎⠎⢎⠪⡪⡘⡌⢎⢢⠱⡨⢂⠅⠄⠄⠄⠄⠠⠄⠄⠂⠠⠠⠄⠄⠠⠐⠠⠄⠄⠄⠄
⠄⠄⠄⠄⢘⢌⢪⢪⢣⢣⢣⠣⣣⡿⣟⣿⢾⣼⢼⢘⠜⡌⢆⠣⡃⢇⠪⡘⡨⣪⣠⠡⠪⠰⡐⡀⡀⠄⠐⠈⡀⠂⡈⠄⡂⠁⡐⠄⠂⠨⠄⠄⠄⠄
⠄⠄⠄⠄⠄⡇⡗⡕⢼⠸⡐⡵⣯⣟⣯⣟⣿⡺⡑⢅⠣⠪⠘⣌⡬⣦⣷⣿⣽⣿⣽⢐⠅⠕⢌⠢⡑⢔⢄⠁⠠⠐⠄⢁⠄⠂⠄⢈⠄⠅⠄⠄⠄⠄
⠄⠄⠄⠄⡔⡎⡎⢎⠪⡘⡌⣚⢓⢟⢞⣗⢷⡑⡌⡢⡥⣧⣟⣾⣿⢿⣿⣾⣿⣟⣿⢂⠕⡩⠢⠱⠨⡂⡑⡱⡠⡀⠈⠠⠄⡁⠐⢀⠐⠄⠄⠄⠄⠄
⠄⠄⠄⢔⠯⡪⡨⡂⡣⡑⡌⢆⠕⡡⢑⢌⣗⣟⣮⣿⣽⣷⣿⣿⣻⣿⣿⣽⠾⢛⠊⡔⢅⠪⡨⠪⡘⡌⡢⢂⢑⠜⡄⡁⠄⠐⠈⡀⠂⠄⠄⠄⠄⠄
⠄⠄⠄⠈⡇⡇⢎⢜⠰⠑⡨⣰⣰⣜⣮⣷⣯⣿⣽⣾⣿⣽⣷⣿⣟⡯⡷⠍⢌⠢⡊⡢⡑⠕⡌⢕⡑⡌⡪⠢⡂⡪⠘⢔⢔⠄⠁⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠈⢪⠢⢑⡠⣧⣗⣷⢷⣻⣷⢿⣾⣯⣿⢿⡾⣟⣟⣮⢷⣯⠟⢌⠢⡑⡑⡌⡪⡘⡌⡒⡜⡰⡑⣑⢑⢌⠬⠠⢑⠱⡠⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⢃⣾⣻⣯⣿⣻⣟⣿⣽⣿⡻⠝⠝⡙⣨⢾⡾⣾⢿⢹⠨⡪⡸⡐⢕⢸⢘⢌⢎⢜⠰⡑⢌⠢⡑⡅⢕⠅⡂⠌⢜⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢀⠸⣟⣿⣽⣿⣻⡻⠫⢓⠡⠨⠨⡂⣶⣟⣯⣿⣻⠫⡪⣊⢲⢨⠪⡪⠢⡣⣑⠜⡔⢕⢅⢕⠬⡘⡌⠢⡱⢨⢈⠐⢅⠄⠄⠄⠄⠄⠄
⠄⠄⠄⢠⢠⢑⠌⠙⢝⠱⡑⢄⢂⢅⠢⠪⣘⣬⣾⢿⣾⣻⢽⢘⠌⡆⢆⢣⠱⡑⡅⣧⣓⣫⣪⢘⢔⠱⡐⢕⢐⠅⠑⢜⠨⢢⠄⠡⡑⡀⠄⠄⠄⠄
⠄⠄⢠⠱⡘⠄⠄⣮⣢⣕⣌⣆⣦⣦⣧⢿⣽⣯⣿⣻⠝⢕⠱⡰⣑⢅⢇⢕⢥⣳⢯⡿⣽⢷⡯⣷⢬⢊⠎⡘⢀⠂⠅⠅⠑⢅⢕⠄⠄⢇⢄⠄⠄⠄
⠄⢠⠣⠁⠄⢀⢔⠄⠝⠷⢿⢽⣷⢿⣾⢿⡻⡚⡫⠊⠜⠈⠊⡎⣎⢦⡵⣽⡽⣯⢿⣽⡋⠋⠋⠁⠉⠂⠂⢐⠄⠡⠨⡠⡑⡑⢔⠄⠄⠂⠱⡀⠄⠄
⠄⠨⠪⠠⠄⢜⠪⡨⢊⠪⡢⢡⢑⠉⠈⢤⡬⡄⠄⠄⠈⠲⡦⣯⢷⣻⣽⢯⡿⣽⣻⡮⣴⢶⣥⠄⠁⠄⠠⠄⠄⠅⡑⢔⢑⠌⡢⢁⠄⠄⠁⡕⡀⠄
⠄⠄⠈⠡⡱⡡⡣⡊⡂⡇⢎⠢⡅⠄⡔⠋⠛⠁⠄⠁⠄⡀⠘⣿⢽⣻⢾⣻⣽⢯⣷⣻⠛⠿⠻⠄⠂⠄⠂⠑⡄⠐⢌⠢⠢⠡⡊⠔⡠⠂⢂⠕⡂⠄
⠄⠄⠄⠈⡎⣇⢧⠢⡊⢎⢪⠸⡐⢀⡇⢔⠢⡃⢇⠇⢖⢄⠄⣟⣿⡽⣿⢽⣾⣻⣽⡽⠠⡐⡒⡒⣒⠢⡂⡄⣳⢀⠣⠡⠣⡑⠌⢌⢂⠄⠄⠈⠄⠄
⠄⠄⠄⠄⢇⡇⠧⡱⢸⢸⠜⢕⢅⢤⡿⠐⢕⢕⢕⠕⡕⡌⣰⣽⢾⡯⣟⣯⡷⡿⣞⣿⡈⢎⢜⠌⡆⡣⡣⢡⢗⠄⠕⡡⢑⠨⠨⡂⡂⡂⠄⠄⠄⠄
⠄⠄⠄⠄⠑⢭⢱⢘⢌⢎⢎⠢⡃⠯⣟⣷⢤⣑⣘⣈⣪⣴⢿⣞⣿⢽⣯⡷⣟⡿⣯⢯⡿⣌⣂⠣⠊⣂⡥⣯⢟⢌⠌⡂⢅⠪⡈⡢⢂⠂⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠑⠑⡢⢱⠸⡰⡑⠜⢌⠎⡯⣫⡻⣺⢝⢟⣞⣯⢗⣋⣛⣚⣙⣋⡛⡝⣯⣟⡿⡽⣫⡟⣵⢫⡫⡑⡑⢌⢐⠅⡪⡐⢌⠢⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠠⠠⢊⠢⡑⠔⡌⡊⢆⠕⢍⢮⡪⣗⡽⣝⡾⣵⡳⡳⣕⢞⡼⣜⢮⡺⢸⡺⣽⡺⡵⡽⡜⣎⢊⢂⠊⢔⢐⠨⢐⢐⠁⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠐⠄⢁⠪⡨⢂⢊⢢⢑⠑⠑⢝⢎⢯⡺⣝⢞⣬⣋⠮⠫⠞⠮⣓⣹⢮⢯⣳⡫⡯⡺⠸⠐⠡⢂⢑⠐⡐⠨⢐⠐⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⠄⠄⢊⢌⠢⢱⡈⢄⠠⡀⠄⠈⡕⡝⣎⢗⠳⡹⠻⡫⡻⠝⠗⡝⡪⢓⢕⢕⠅⠁⠄⠠⡈⠔⠠⢁⠂⠅⡂⠂⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⡀⠄⠄⠄⠄⡀⣆⠕⢸⢜⡮⣪⠂⠐⠄⣕⢽⢮⢯⢊⠆⢕⢌⠢⣑⢑⠔⡸⡐⡽⡺⡌⠄⠄⢡⢢⢡⠡⡂⠌⡐⠠⠁⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠠⠐⢈⣀⡦⣟⡾⡽⣤⣟⣮⠗⠈⠄⢱⢼⣕⡯⣗⣅⢇⠕⡔⢕⠱⡨⡊⡆⣪⣫⣳⣕⢅⠈⡀⡇⡧⢑⠠⡡⣔⣬⡢⡀⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⢀⣴⣧⣷⣿⢯⣟⡯⡗⢛⠪⠅⢌⢄⢓⢟⢞⢽⡳⣵⣸⣘⣌⢎⢇⣣⡱⣱⡱⣗⢗⣗⠵⡠⡂⡪⠪⠲⢝⣾⣳⣯⢿⣺⣤⠄⠄⠄⠄⠄
⠄⠄⠄⠄⡜⣿⣻⡿⣾⡛⡋⢂⠐⡀⠂⠌⡀⢂⠱⢀⠂⠁⠈⠠⠠⠑⣕⢍⢧⠃⢍⠐⠑⠓⡓⢅⠇⢂⠡⠐⡈⠈⠄⠑⢛⢾⢿⣽⢛⠄⠄⠄⠄⠄
⠄⠄⠄⣌⠳⡙⢿⡽⡳⢀⠂⡐⢀⠂⡁⢂⠐⡀⢂⢑⠄⠐⠄⠨⠨⢐⢠⠲⣐⠈⡂⠄⠈⡠⡊⡂⠌⡀⢂⠡⠄⠅⡈⠐⢀⠙⠟⣰⠘⣤⡢⠄⠄⠄
⠄⠄⣠⣿⣮⠑⠢⡋⡎⢀⠂⢐⠄⢂⠐⡀⢂⠐⠠⠐⢅⠄⠄⠅⠌⡰⢢⢥⠆⡢⠢⠠⠐⡈⠢⠐⡀⢂⠐⡀⠅⢂⠠⠁⠄⢈⠢⢡⢜⢮⠓⣄⡀⠄
""")
main_threadpool.shutdown(wait=False, cancel_futures=True)
print("Done.")