import locale
from os import popen
import re
from subprocess import call, DEVNULL
from dialog import Dialog


locale.setlocale(locale.LC_ALL, '')


# Uruchamia komendę jako root i nie wyświetla wyjścia.
def silent_call(command: str) -> int:
    return call(
        "echo $PASS | su -c '%s'" % command,
        shell=True,
        stdout=DEVNULL,
        stderr=DEVNULL
    )


class Panel:
    def __init__(self):
        self.start()

    def start(self) -> None:
        self.dialog = Dialog(dialog='dialog', autowidgetsize=True)
        self.dialog.set_background_title('Administracja')
        self.help_me()

    def latex(self) -> None:
        self.dialog.infobox('Trwa instalacja pakietów texlive...')
        ret = silent_call(
            'pacman -Sy --noconfirm && pacman -S --noconfirm texlive-most'
            )
        if ret != 0:
            self.dialog.msgbox('Nie udało się zainstalować pakietów texlive.')
        else:
            self.dialog.msgbox('Pomyślnie zainstalowano pakiety texlive.')
            self.menu()

    def menu(self) -> None:
        code, tag = self.dialog.menu(
            "Wybierz czynność",
            choices=[
                ("(1)", "Jak uruchomić program?"),
                ("(2)", "Wykonaj aktualizację systemu"),
                ("(3)", "Wyłącz"),
                ("(4)", "Zainstaluj TeXLive")
            ]
        )
        if code == self.dialog.OK:
            if tag == "(1)":
                self.help_me()
            elif tag == "(2)":
                self.update()
            elif tag == "(3)":
                self.shutdown()
            elif tag == "(4)":
                self.latex()
        else:
            self.menu()

    def help_me(self) -> None:
        ipv4 = popen('hostname -i').read().strip()

        # Import .jupyter/jupyter_notebook_config.py nie działa.
        # Trzeba posłużyć się wyrażeniami regularnymi.
        config = open(
            '/home/admin/.jupyter/jupyter_notebook_config.py',
            'r'
        ).read()

        port_match = re.compile(
            r'^c.NotebookApp.port\s?=\s?\d{1,5}',
            re.MULTILINE
        ).search(config)
        port = re.split(r'\D+', port_match.group())[-1]

        self.dialog.msgbox("W przeglądarce należy wpisać: %s:%s" % (ipv4, port))
        self.menu()

    def update(self) -> None:
        self.dialog.gauge_start('Trwa aktualizacja systemu...')
        silent_call('pacman -Syu --noconfirm')
        self.dialog.gauge_update(50)
        silent_call('npm update -g')
        self.dialog.gauge_update(75)
        silent_call('pip install --upgrade octave_kernel')
        silent_call('pip install --upgrade jupyter_contrib_nbextensions')
        self.dialog.msgbox(
            'Aktualizacja zakończona. Zalecany jest restart systemu.'
        )
        self.menu()

    def shutdown(self) -> None:
        self.dialog.infobox('Usuwanie plików tymczasowych...')
        silent_call('rm -rf /tmp/*')
        silent_call('rm -rf /home/admin/.sage/temp/*')
        self.dialog.infobox('Zamykanie systemu...')
        silent_call('poweroff')


Panel()
