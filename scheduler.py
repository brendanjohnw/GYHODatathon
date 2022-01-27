"This code begins the scheduler"

import time
import schedule
import preprocessing as prepro
import constants


def scheduler():
    # schedule.every(24).hours.do(process_script)
    schedule.every(constants.TIME_INTERVAL_MINUTES).minutes.do(prepro.process_script)
    prepro.process_script()
    while True:
        schedule.run_pending()
        time.sleep(1)

try:
    scheduler()
except KeyboardInterrupt:
    print("Script Terminated...\nFeedback processing stopped.\nGoogle Sheet data will NOT be imported.\n")