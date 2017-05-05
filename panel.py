import locale
from os import popen
from dialog import Dialog
from subprocess import call, DEVNULL


locale.setlocale(locale.LC_ALL, '')


# Uruchamia komendę jako root i nie wyświetla wyjścia.
def silent_call(command):
    return call(
        "echo $PASS | su -c '%s'" % command,
        shell=True,
        stdout=DEVNULL,
        stderr=DEVNULL
    )


class Panel:
    def __init__(self):
        self.start()

    def start(self):
        self.d = Dialog(dialog='dialog', autowidgetsize=True)
        self.d.set_background_title('Administracja')
        self.help_me()

    def menu(self):
        code, tag = self.d.menu(
            "Wybierz czynność",
            choices=[
                ("(1)", "Jak uruchomić program?"),
                ("(2)", "Wykonaj aktualizację systemu"),
                ("(3)", "Wyłącz")
            ]
        )
        if code == self.d.OK:
            if tag == "(1)":
                self.help_me()
            elif tag == "(2)":
                self.update()
            elif tag == "(3)":
                self.shutdown()
        else:
            self.menu()

    def help_me(self):
        ipv4 = popen('hostname -i').read().strip()

        # Import .jupyter/jupyter_notebook_config.py nie działa.
        # Trzeba posłużyć się wyrażeniami regularnymi.
        port = popen(
            'cat .jupyter/jupyter_notebook_config.py | '
            + 'grep "^c.NotebookApp.port = *" '
            + '| cut -c 21-26'
        ).read().strip()
        self.d.msgbox("W przeglądarce należy wpisać: %s:%s" % (ipv4, port))
        self.menu()

    def update(self):
        self.d.gauge_start('Trwa aktualizacja systemu...')
        silent_call('pacman -Syu --noconfirm')
        self.d.gauge_update(50)
        silent_call('npm update -g')
        self.d.gauge_update(75)
        silent_call('pip install --upgrade octave_kernel')
        self.d.msgbox(
            'Aktualizacja zakończona. Zalecany jest restart systemu.'
        )
        self.menu()

    def shutdown(self):
        self.d.infobox('Usuwanie plików tymczasowych...')
        silent_call('rm -rf /tmp/*')
        silent_call('rm -rf /home/admin/.sage/temp/*')
        self.d.infobox('Zamykanie systemu...')
        silent_call('poweroff')


panel = Panel()
