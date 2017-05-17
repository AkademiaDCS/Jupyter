# Jupyter
Repozytorium zawiera pliki użyte do konfiguracji
maszyny wirtualnej z zainstalowanym Jupyterem.
Zainstalowany system to Arch Linux.
Wybór padł na Arch Linuksa ze względu na system wydań (rolling release)
i najnowszą wersję SageMath w repozytorium.

Typ karty sieciowej w programie VirtualBox to `bridged`.

Szybka instalacja
---
Należy zainstalować system i utworzyć użytkownika `admin`.
Następnie jako `admin` trzeba sklonować repozytorium do dowolnego katalogu
i uruchomić instalator (wymagany pakiet `python-pythondialog`):
```
python3 install.py
```

### Aktualizacja komponentów
Należy wejść do katalogu, w którym znajduje się katalog z plikami instalacyjnymi,
zsynchronizować repozytorium (`git pull`) i uruchomić instalator.
W menu znajduje się opcja `Aktualizacja komponentów`.

Ręczna instalacja
---

## Pakiety
`jupyter`, `sagemath`, `sagemath-jupyter`,
`jupyter-widgetsnbextension`, `python-pythondialog`, `octave`,
`python-pip`, `nodejs`, `npm`.

`octave_kernel` przez `pip`.
```
# pip install octave_kernel
# python -m octave_kernel.install
```

`ijavascript` przez `npm`.
```
# npm install -g ijavascript
$ ijsinstall
```

## Działanie
Zgodnie z instrukcjami z [ArchWiki](https://wiki.archlinux.org/index.php/Getty#Automatic_login_to_virtual_console)
ustawić należy automatyczne logowanie do `tty1`.
Użytkownik musi nazywać się `admin`.

Do bliku `.bashrc` dodać należy następujące instrukcje:
```bash
export PASS=HASŁO_ROOTA
export PYTHONWARNINGS="ignore"
setfont lat2-16 -m 8859-2
echo $PASS | su -c "setterm -blank 0 -powerdown 0"
./run.sh
```
Dzięki temu możliwa jest pełna automatyzacja zadań administracyjnych
(`echo $PASS | su -c 'KOMENDY'`).

Skrypt `run.sh` sprawdza, czy w folderze `/home/admin`
istnieje już folder `.juplock`.
Jeśli tak, przerywa pracę. Dzięki temu mamy pewność, że Jupyter nie zostanie
równolegle uruchomiony kilka razy.

Jeśli folder nie istnieje, jest tworzony;
uruchomione zostają Jupyter i panel sterowania.
Panel sterowania zaimplementowany jest w języku Python z użyciem biblioteki
`pythondialog`.

Żeby mieć pewność, że `.juplock` jest usuwany po każdym wyłączeniu maszyny,
uruchomiona jest usługa `jup.service`.
```
# cp jup.service /etc/systemd/system
# systemctl enable jup
```
Wykonuje ona skrypt `.lock_remove` z katalogu `/home/admin`
po każdym uruchomieniu systemu, ale przed logowaniem.

## Konfiguracja Jupytera
```
$ jupyter notebook --generate-config
```
Ta komenda powinna stworzyć plik `~/.jupyter/jupyter_notebook_config.py`.

Trzeba w nim dodać następujące linijki:
```python
c.NotebookApp.ip = '*'
c.NotebookApp.token = ''
c.NotebookApp.port = 8888
c.NotebookApp.notebook_dir = '/home/admin/notebooks' # Wcześniej należy utworzyć ten folder
```

## Użycie
Po uruchomieniu systemu pokazuje się okienko z informacją o adresie IP
w sieci lokalnej.
![W przeglądarce należy wpisać...](img/welcome.png)

Po wciśnięciu przycisku ENTER pokazuje się proste menu
(menu jest idiotoodporne, więc przycisk `Anuluj` nic nie robi).
![Wybierz czynność...](img/menu.png)

A tak wygląda sytuacja po stronie hosta:
![Jupyter widziany oczami końcowego użytkownika](img/jupyter.png)
