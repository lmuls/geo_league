import os

DB_HOST = '127.0.0.1'
DB_NAME = 'geoleague'
DB_PORT = '5432'
TEST_DB_PORT = '5431'
DB_USER = 'geouser'
DB_PASSWORD = 'geoPASS123'

proj_vars = {
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_URL": f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    "TEST_DB_URL": f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{TEST_DB_PORT}/{DB_NAME}',
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

proj_paths = [BASE_DIR]

def set_local():
    counter = 0
    with open(os.path.join(BASE_DIR, "env\Lib\site-packages\_set_envs.pth"), "w") as f:
        f.write("import os; ")
        for k, v in proj_vars.items():
            if "/" or "\ " in v:
                f.write("os.environ['" + k + "']=" + "r'" + v + "';")
            else:
                f.write("os.environ['" + k + "']=" + "'" + v + "';")

    with open(os.path.join(BASE_DIR, "env\Lib\site-packages\_set_path.pth"), "w") as f:
        f.write("import sys;")
        for path in proj_paths:
            f.write("sys.path.insert(" + str(counter) + "," + "r'" + path + "');" )


if __name__ == "__main__":
    set_local()
