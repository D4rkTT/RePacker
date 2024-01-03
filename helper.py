import js2py
import zipfile
import os
import glob 
import string
import random
import shutil
import subprocess
from pathlib import Path

class rebuilder:
    def __init__(self, file, platform, idir, odir):
        if not os.path.exists(idir):
            self.idir = str(Path(idir).absolute()).replace('\\', '/')
        else:
            raise Exception("Extraction output directory is already exist.")

        if not os.path.exists(odir):
            os.mkdir(odir)
            self.odir = str(Path(odir).absolute()).replace('\\', '/')
        else:
            raise Exception("Output directory is already exist.")

        if os.path.isfile(file):
            self.file = file
        else:
            raise Exception("File not exist.")

        if platform in ["android", "ios"]:
            self.platform = platform
        else:
            raise Exception("Wrong platform.")

    def unpack(self):
        with zipfile.ZipFile(self.file, 'r') as zip_ref:
            zip_ref.extractall(self.idir)

    def clean_tmp(self):
        shutil.rmtree(self.idir)

    def get_plugins(self):
        if self.platform == "ios":
            new_app_dir = glob.glob(f"{self.idir}/Payload/*.app")[0].replace("\\","/")
        else:
            new_app_dir = f"{self.idir}/assets"
            
        if os.path.isfile(f"{new_app_dir}/www/cordova_plugins.js"):
            cordova_plugins = ""
            with open(f"{new_app_dir}/www/cordova_plugins.js", 'r') as f:
                cordova_plugins = f.read()

            cordova_plugins = cordova_plugins.replace("cordova.define", "var rebuilder = ")
            cordova_plugins += ";var result = {};rebuilder('', '', result);return result.exports.metadata;"
            result = js2py.eval_js(f"function z(){{{cordova_plugins}}};z()")
            return result
        else:
            raise Exception("Can't find cordova_plugins.js in www directory.")
    
    def new_cordova(self):
        os.chdir(self.odir)
        app_id = f'com.rebuilder.reapp.{"".join(random.choices(string.ascii_lowercase, k=8))}'
        subprocess.call(['cordova', 'create', 'ReApp', app_id , 'ReApp'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.chdir("ReApp")
    
    def move_files(self):
        if self.platform == "ios":
            app_dir = glob.glob(f"{self.idir}/Payload/*.app")[0].replace("\\","/") + "/www"
            new_app_dir = f"{self.odir}/ReApp/www"
        else:
            app_dir = f"{self.idir}/assets/www"
            new_app_dir = f"{self.odir}/ReApp/www"

        if os.path.exists(new_app_dir):
            shutil.rmtree(new_app_dir)
        shutil.move(app_dir, new_app_dir)

        # Clean unwanted files
        if os.path.isfile(new_app_dir + "/cordova_plugins.js"):
            os.remove(new_app_dir + "/cordova_plugins.js")
        if os.path.isfile(new_app_dir + "/cordova.js"):
            os.remove(new_app_dir + "/cordova.js")
        if os.path.exists(new_app_dir + "/cordova-js-src"):
            shutil.rmtree(new_app_dir + "/cordova-js-src")
        if os.path.exists(new_app_dir + "/plugins"):
            shutil.rmtree(new_app_dir + "/plugins")

    def install_plugin(self, plugin):
        # repeat the command to insure that the plugin is installed (cordova bug)
        for i in range(2):
            subprocess.call(['cordova', 'plugin', 'add', plugin], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def remove_plugin(self, plugin):
        subprocess.call(['cordova', 'plugin', 'remove', plugin], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def add_platform(self):
        # repeat the command to insure that the platform is added (cordova bug)
        for i in range(2):
            subprocess.call(['cordova', 'platform', 'add', self.platform], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def remove_platform(self):
        subprocess.call(['cordova', 'platform', 'remove', self.platform], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def cordova_prepare(self):
        subprocess.call(['cordova', 'prepare', self.platform, '--device', '--debug'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def cordova_build(self):
        subprocess.call(['cordova', 'build', self.platform, '--device', '--debug'], shell=True)
    
    def open_project(self):
        subprocess.Popen([
            'open', '-a', 'Xcode', 'platforms/ios'
        ], shell=True)

def check_cordova():
    if shutil.which("cordova"):
        return True
    return False


