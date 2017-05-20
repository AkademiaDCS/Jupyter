import subprocess
from typing import List
from dialog import Dialog


def join_list(_list: List[str]) -> str:
    result = ''
    for i in _list:
        result += i + ' '
    return result


class Installer:
    def __init__(self):
        self.password = ''
        self.dialog = Dialog(autowidgetsize=True)
        self.dialog.set_background_title('Instalacja')
        self.menu()

    def call(self, command: str, sudo=False) -> int:
        cmd = command
        if sudo == True:
            cmd = 'echo %s | su -c "%s"' % (self.password, command)
        return subprocess.call(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True)

    def menu(self) -> None:
        code, tag = self.dialog.menu('Wybierz czynność', choices=[
            ('(1)', 'Instalacja'),
            ('(2)', 'Aktualizacja komponentów')
        ])

        if code == self.dialog.CANCEL:
            exit(0)
        else:
            if tag == '(1)':
                self.ask_pass()
                self.copy_components()
                self.bashrc()
                self.install_packages()
                self.jupyter()
            elif tag == '(2)':
                self.ask_pass()
                self.copy_components()

    def goodbye(self):
        self.dialog.msgbox('Instalacja zakończona.')
        self.call('reboot', sudo=True)

    def copy_components(self):
        self.call(
            'cp -f jup.service /etc/systemd/system && systemctl enable jup',
            sudo=True)
        self.call(
            'cp -f override.conf /etc/systemd/system/getty@tty1.service.d/',
            sudo=True
            )
        self.call('cp -f .lock_remove /home/admin')
        self.call('cp -f jup.sh /home/admin')
        self.call('cp -f run.sh /home/admin')

    def ask_pass(self):
        code, password = self.dialog.passwordbox('Podaj hasło roota')
        if code != self.dialog.OK:
            self.dialog.msgbox('Nie udało się pobrać hasła roota')
            self.menu()
        else:
            self.password = password

    def bashrc(self) -> None:
        with open('/home/admin/.bashrc', 'a') as bashrc:
            bashrc.writelines([
                'export PASS=%s \n' % self.password,
                'export PYTHONWARNINGS="ignore" \n',
                'setfont lat2-16 -m 8859-2 \n',
                'echo $PASS | su -c "setterm -blank 0 -powerdown 0" \n',
                './run.sh \n'
            ])

    def jupyter(self) -> None:
        self.call('mkdir /home/admin/notebooks')
        self.call('(cd /home/admin && jupyter notebook --generate-config)')
        with open('/home/admin/.jupyter/jupyter_notebook_config.py', 'a') as jnc:
            jnc.writelines([
                'c.NotebookApp.ip = "*" \n',
                'c.NotebookApp.token = "" \n',
                'c.NotebookApp.port = 8888 \n',
                'c.NotebookApp.notebook_dir = "/home/admin/notebooks" \n'
            ])


    def install_packages(self):
        pacman_pkgs = [
            'jupyter',
            'sagemath',
            'sagemath-jupyter',
            'jupyter-widgetsnbextension',
            'python-pythondialog',
            'octave',
            'python-pip',
            'nodejs',
            'npm'
        ]

        pip_pkgs = [
            'octave_kernel'
        ]

        npm_pkgs = [
            'ijavascript'
        ]

        ret = 0

        self.dialog.infobox('Trwa instalacja wymaganych pakietów...')
        ret += self.call(
            'pacman -Sy --noconfirm && pacman --noconfirm -S %s' % join_list(pacman_pkgs),
            sudo=True)
        ret += self.call('npm install -g %s' % join_list(npm_pkgs), sudo=True)
        ret += self.call('pip install %s' % join_list(pip_pkgs), sudo=True)

        self.call('python -m octave_kernel.install', sudo=True)
        self.call('ijsinstall')

        if ret > 0:
            self.dialog.msgbox('Nie udało się zainstalować niezbędnych pakietów.')
            self.menu()

Installer()
