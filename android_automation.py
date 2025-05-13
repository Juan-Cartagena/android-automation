import schedule
import subprocess
import time
import pytesseract
from PIL import Image



# Ruta al ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def run_adb_command(command, delay=1.0):
    """Ejecuta un comando ADB y espera el tiempo especificado."""
    print(f"Ejecutando: {command}")
    subprocess.run(command, shell=True)
    time.sleep(delay)

def login_sequence():
    print("Iniciando secuencia de Login...")
    run_adb_command("adb shell monkey -p com.processa.mobility.issuer.bancamia -c android.intent.category.LAUNCHER 1", delay=10)
    run_adb_command("adb shell input tap 300 990", delay=1)
    with open('pass.txt', 'r', encoding='utf-8') as f:
        st = f.readline().strip()

    run_adb_command(f'adb shell input text "{st}"', delay=1)
    run_adb_command("adb shell input tap 600 474", delay=20)

def qr_sequence():
    print("Iniciando secuencia de QR...")
    run_adb_command("adb shell input tap 400 1400", delay=1)
    run_adb_command("adb shell input tap 500 830", delay=10)

def account_sequence():
    print("Iniciando secuencia de Cuentas...")
    run_adb_command("adb shell input tap 600 760", delay=1)
    run_adb_command("adb shell input tap 180 900", delay=1)
    run_adb_command("adb shell input text \"1\"", delay=1)
    run_adb_command("adb shell input keyevent 4", delay=1)
    run_adb_command("adb shell input tap 368 1030", delay=30)

def otp_sequence():
    print("Iniciando secuencia de OTP...")
    run_adb_command("adb shell cmd statusbar expand-notifications", delay=1)
    run_adb_command("adb shell screencap -p /sdcard/pantalla.png", delay=1)
    run_adb_command("adb pull /sdcard/pantalla.png", delay=1)
    run_adb_command("adb shell rm /sdcard/pantalla.png", delay=1)
    # Ruta a tu imagen
    imagen = Image.open("pantalla.png")
    # imagen.show()

    # Define la región (x1, y1, x2, y2)
    # Por ejemplo, una caja desde (100, 100) hasta (300, 200)
    region = (125, 700, 220, 750)
    sub_imagen = imagen.crop(region)
    sub_imagen.show()

    # OCR sobre esa subimagen
    texto = pytesseract.image_to_string(sub_imagen, lang='spa')  # Usa 'eng' para inglés, 'spa' para español
    print("Texto reconocido:", texto)
    run_adb_command("adb shell input keyevent 4", delay=1)
    run_adb_command("adb shell input tap 180 850", delay=1)
    run_adb_command(f'adb shell input text "{texto}"', delay=1)
    run_adb_command("adb shell input tap 610 850", delay=60)

def close_app_sequence():
    print("Iniciando secuencia de Cerrar App...")
    run_adb_command("adb shell input tap 550 1560", delay=1)
    run_adb_command("adb shell input swipe 380 1160 380 200 300", delay=1)

def auto():
    login_sequence()
    qr_sequence()
    account_sequence()
    otp_sequence()
    close_app_sequence()
    print("Secuencia completa.")
    

def main():
    auto()
    schedule.every(10).minutes.do(auto)
    # schedule.every(14).seconds.do(auto)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
