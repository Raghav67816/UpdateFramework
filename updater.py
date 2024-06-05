# Import dependencies
from os import getcwd
from sys import argv
from time import sleep
from requests import get
from threading import Thread
from popup_dialog import Ui_UpdateDialog
from urllib.request import urlretrieve, urlcleanup
from PySide6.QtWidgets import QDialog, QApplication, QTableWidgetItem, QMessageBox


class UpdaterUi(QDialog):
    def __init__(self, updates_info: list[dict]):
        super().__init__()

        self.ui = Ui_UpdateDialog()
        self.ui.setupUi(self)
        self._updates_info = updates_info
        self._downloader_thread = None

        for index, updates in enumerate(updates_info):
            self.ui.tableWidget.insertRow(index)
            item = QTableWidgetItem()
            item.setText(updates['name'])
            self.ui.tableWidget.setItem(index, 0, item)

        for index, updates in enumerate(updates_info):
            _item = QTableWidgetItem()
            _item.setText(updates['name'])
            _item.setText(updates['version'])
            self.ui.tableWidget.setItem(index, 2, _item)            

        # Create connections
        self.ui.updateBtn.clicked.connect(self.download_files)

    def get_release_links_and_filenames(self, update_dict: list[dict]):
        links = []
        filenames = []
        for release in update_dict:
            links.append(release['release_link'])
            filenames.append(release['filename'])
        return [links, filenames]

    def _donwload_files(self):
        thread = Thread(target=self.download_files)
        
        self._downloader_thread = thread
        thread.start()

    # Download files
    def download_files(self):
        info = self.get_release_links_and_filenames(self._updates_info)
        links = info[0]
        filenames = info[1]

        for i in range(0, len(links)):
            print(f"Downloading {filenames[i]}")
            urlretrieve(links[i], filenames[i])
            sleep(1)
        urlcleanup()
        
class Updater:
    def __init__(self, request_endpoint: str, products_installed: list[dict]):

        self._cwd = getcwd()
        self._service_name = "Update Service"
        self._updates_available = []

        if request_endpoint == "":
            raise Exception("Request endpoint not specified.")
        else:
            # Get latest release
            for products in products_installed:
                response = get(request_endpoint, {
                    "product": products['name'],
                    "version": products['version']
                })
                if response.status_code == 200:
                    res_json = response.json()
                    print(res_json)
                    if res_json['release_link'] != "":
                        res_json['name'] = products['name']
                        self._updates_available.append(res_json)
                        print("Updates fetched")
                        
                    else:
                        pass
                else:
                    print(f"Server responded with an error code {response.status_code}")

            if len(self._updates_available) == 0:
                print("Up-to-date")

            else:
                self.show_dialog(self._updates_available)
        
    def show_dialog(self, fetched_updates):
        app = QApplication(argv)
        ui = UpdaterUi(fetched_updates)
        ui.show()
        app.exec()
