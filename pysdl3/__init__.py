import shutil

from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.logger import info, shprint
from pythonforandroid.util import current_directory
import os
import sh

class PySDL3Recipe(PythonRecipe):
    version = '0.9.12b1'
    # modify the patch's file path too if you want to change version

    url = 'https://v4.gh-proxy.org/https://github.com/Aermoss/PySDL3/archive/refs/tags/v{version}.tar.gz'

    depends = ['android', 'sdl3']
    patches = [
        'patches/android.patch',
    ]

    site_packages_name = 'sdl3'

    # def build_arc(self, arch):
    #     build = "build_{}".format(arch.arch)
    #     if hasattr(self, build):
    #         getattr(self, build)()

    def build_arch(self, arch):
        """imitate the android environment and import the pysdl3 package in a tmp script."""
        super().build_arch(arch)
        env = self.get_recipe_env(arch)
        build_dir = self.get_build_dir(arch)
        site_packages_dir = self.ctx.get_site_packages_dir(arch)
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{site_packages_dir}:{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = site_packages_dir
        python_binary = self.hostpython_location

        script_path = os.path.join(build_dir, 'test_pysdl3_import.py')
        script = """
import os
os.environ["SDL_DISABLE_METADATA"] = "0"
os.environ["SDL_FIND_BINARIES"] = "1"
import sdl3
print("successfully imported pysdl3")
sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO)
print("video successfully initialized")
sdl3.LP_SDL_FRect()
print("doc successfully initialized")
        """

        with open(script_path, 'w') as f:
            f.write(script)
        try:
            shprint(sh.Command(python_binary), script_path, _env=env,)
        finally:
            if os.path.exists(script_path):
                os.remove(script_path)

        doc_file = os.path.join(build_dir, '__doc__.py')
        if os.path.exists(doc_file):
            env = self.get_recipe_env(arch)
            shprint(sh.Command(self.hostpython_location), '-m', 'compileall', '-b', '-f', doc_file, _env=env)

        with current_directory(self.get_build_dir(arch.arch)):
            shutil.rmtree(os.path.join(self.ctx.get_python_install_dir(arch.arch), "sdl3"))
            shprint(self._host_recipe.pip, 'install', '.',
                    '--compile', '--target',
                    self.ctx.get_python_install_dir(arch.arch),
                    _env=env, *self.setup_extra_args
            )

        # input("press Enter to continue")

recipe = PySDL3Recipe()
