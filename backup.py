import os
import shutil
from datetime import datetime
import time
import logging

class BackupManager:
    def __init__(self, source_path, backup_path):
        self.source_path = source_path
        self.backup_path = backup_path
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('backup-log.log'),
                logging.StreamHandler()
            ]
        )
    
    def create_backup(self):
        try:
            os.makedirs(self.backup_path, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if os.path.isdir(self.source_path):
                return self._backup_directory(timestamp)
            elif os.path.isfile(self.source_path):
                return self._backup_file(timestamp)
            else:
                logging.error(f"Path sumber {self.source_path} tidak ditemukan!")
                return False
        except Exception as e:
            logging.error(f"Terjadi kesalahan saat backup: {str(e)}")
            return False
    
    def _backup_directory(self, timestamp):
        backup_name = f"backup_{timestamp}.zip"
        backup_file = os.path.join(self.backup_path, backup_name)
        try:
            shutil.make_archive(backup_file.replace('.zip', ''), 'zip', self.source_path)
            logging.info(f"Backup folder berhasil: {backup_file}")
            return True
        except Exception as e:
            logging.error(f"Gagal backup folder: {str(e)}")
            return False
    
    def _backup_file(self, timestamp):
        file_name = os.path.basename(self.source_path)
        backup_name = f"{file_name}_{timestamp}"
        backup_file = os.path.join(self.backup_path, backup_name)
        try:
            shutil.copy2(self.source_path, backup_file)
            logging.info(f"Backup file berhasil: {backup_file}")
            return True
        except Exception as e:
            logging.error(f"Gagal backup file: {str(e)}")
            return False

def main():
    # Konfigurasi path
    source_path = r"C:\Users\lenovo\Downloads\backup\target"
    backup_path = r"C:\Users\lenovo\Downloads\backup\Hasil_backup"
    backup_interval = 60  # dalam detik

    backup_manager = BackupManager(source_path, backup_path)
    
    logging.info("Sistem backup otomatis dimulai...")
    try:
        while True:
            if backup_manager.create_backup():
                logging.info(f"Menunggu {backup_interval} detik untuk backup berikutnya...")
            else:
                logging.warning("Backup gagal, mencoba lagi pada interval berikutnya...")
            time.sleep(backup_interval)
    except KeyboardInterrupt:
        logging.info("Sistem backup otomatis dihentikan.")

if __name__ == "__main__":
    main()
