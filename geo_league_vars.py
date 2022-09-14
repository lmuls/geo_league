import os

proj_vars = {
    "DB_NAME": 'geoleague',
    "DB_USER": 'gl_user',
    "DB_PASSWORD": 'glPASS123',
}

BASE_DIR = os.getcwd()

def set_local():
    counter = 0
    with open(os.path.join(BASE_DIR, "venv\Lib\site-packages\_set_envs.pth"), "w") as f:
        f.write("import os; ")
        for k,v in proj_vars.items():
            if "/" or "\ " in v:
                f.write("os.environ['" + k + "']=" + "r'" + v + "';" )
            else:
                f.write("os.environ['" + k + "']=" + "'" + v + "';" )


