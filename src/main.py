import utils.saludo
from utils.constantes import DATA_PATH
from pathlib import Path

def main():
    utils.saludo.saludar()
    print(f"{Path.cwd()=}")
    path = DATA_PATH / "usu_hogar_T324.txt" 
    print(f"{path=}")
    f = path.open()
    print(f.readline())

#si este s el prog principal llamame
if __name__ == "__main__":
    main()  
