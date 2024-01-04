import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def click_play_button(driver):
    try:
        play_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".PlayHint-sc-121lzq-0.ixmQLY"))
        )
        play_button.click()
        return True
    except Exception as e:
        print("Play button not found or not clickable, Refreshing page...")
        driver.refresh()
        time.sleep(1)
        try:
            play_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".PlayHint-sc-121lzq-0.ixmQLY"))
            )
            play_button.click()
            return True
        except:
            print("Play button still not found after refresh. Reopening tab.")
            return False

def play_video(driver, url, jumlah_tab):
    main_window = driver.current_window_handle
    i = 1
    while i <= jumlah_tab:
        driver.execute_script("window.open(arguments[0]);", url)
        driver.switch_to.window(driver.window_handles[-1])

        if click_play_button(driver):
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "video"))
                )
                driver.execute_script("document.getElementById('video').play();")
                print(f"Play button clicked - Video di tab {i} diputar.")
                i += 1
            except Exception as e:
                print(f"Tidak dapat memutar video di tab {i}")
        else:
            driver.close()

        driver.switch_to.window(main_window)
        time.sleep(0)

def main():
    jumlah_tab_awal = int(input("Berapa tab yang ingin dibuka? "))
    url = input("Masukkan URL yang ingin dibuka: ")

    while True:
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--mute-audio')
        options.add_argument("--headless")  # Menjalankan browser dalam mode headless
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument('--no-sandbox')  # Opsi penting untuk lingkungan tanpa GUI
        options.add_argument('--disable-dev-shm-usage')  # Membantu dalam lingkungan dengan sumber daya terbatas

        # Additional Linux-specific options
        options.add_argument('--single-process')  # Avoids subprocess spawning
        options.add_argument('--disable-setuid-sandbox')  # Avoids sandboxing issues
        options.add_argument('--remote-debugging-port=9222')  # For debugging if needed
        options.binary_location = "/usr/bin/google-chrome"  # Replace with the actual path


        driver = uc.Chrome(options=options)

        jumlah_tab = random.randint(int(jumlah_tab_awal * 0.8), jumlah_tab_awal)
        print(f"Membuka {jumlah_tab} tab pada iterasi ini.") 

        play_video(driver, url, jumlah_tab)

        wait_time_after_playing = random.randint(60, 120)
        print(f"Menunggu {wait_time_after_playing} detik sebelum memulai ulang...")
        time.sleep(wait_time_after_playing)

        wait_time_before_closing = random.randint(60, 120)
        print(f"Menunggu {wait_time_before_closing} detik sebelum menutup browser...")
        time.sleep(wait_time_before_closing)

        driver.quit()

if __name__ == "__main__":
    main()



#wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#sudo apt install ./google-chrome-stable_current_amd64.deb
