import script
import schedule
import time


programms_lists = script.get_all_lists()

def get():
    return programms_lists

def job():
    global programms_lists
    programms_lists = script.get_all_lists()

def main():
    schedule.every(30).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
