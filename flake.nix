{
  description = "Cromulant - Python+Qt application";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {self, nixpkgs}:
    let
      supportedSystems = ["x86_64-linux" "aarch64-linux"];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs {inherit system;};
          pythonPackages = pkgs.python3Packages;
          manifest = builtins.fromJSON (builtins.readFile ./cromulant/manifest.json);

          wonderwords = pythonPackages.buildPythonPackage rec {
            pname = "wonderwords";
            version = "2.2.0";
            format = "setuptools";
            src = pythonPackages.fetchPypi {
              inherit pname version;
              sha256 = "0b7ec6f591062afc55603bfea71463afbab06794b3064d9f7b04d0ce251a13d0";
            };
            doCheck = false;
          };
        in
        {
          default = pythonPackages.buildPythonApplication rec {
            pname = manifest.program;
            version = manifest.version;

            src = ./.;

            format = "setuptools";

            nativeBuildInputs = with pkgs; [
              qt6.wrapQtAppsHook
              copyDesktopItems
            ];

            buildInputs = with pkgs; [
              qt6.qtbase
              qt6.qtwayland
            ];

            propagatedBuildInputs = with pythonPackages; [
              pyside6
              appdirs
              fonttools
              wonderwords
            ];

          postPatch = ''
              # Remove the invocation of _post_install() at the bottom of the file
              # The function definition is left intact but harmless
              sed -i 's/^_post_install()//g' setup.py
            '';

            desktopItems = [
              (pkgs.makeDesktopItem {
                name = manifest.program;
                exec = manifest.program;
                icon = manifest.program;
                desktopName = manifest.title;
                terminal = false;
                categories = ["Utility"];
              })
            ];

            postInstall = ''
              install -Dm644 ${manifest.program}/img/icon.jpg $out/share/icons/hicolor/256x256/apps/${manifest.program}.jpg
            '';
          };
        });

      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs {inherit system;};
          pythonPackages = pkgs.python3Packages;

          wonderwords = pythonPackages.buildPythonPackage rec {
            pname = "wonderwords";
            version = "2.2.0";
            format = "setuptools";
            src = pythonPackages.fetchPypi {
              inherit pname version;
              sha256 = "0b7ec6f591062afc55603bfea71463afbab06794b3064d9f7b04d0ce251a13d0";
            };
            doCheck = false;
          };
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              (pythonPackages.python.withPackages (ps: with ps; [
                gitpython
                pyside6
                appdirs
                fonttools
                wonderwords
              ]))
              ruff
              mypy
              pyright
            ];
          };
        });
    };
}