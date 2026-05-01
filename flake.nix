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

            # Add the Python dependencies listed in your requirements.txt here
            propagatedBuildInputs = with pythonPackages; [
              # pyqt6
            ];

            postPatch = ''
              # The _post_install hook attempts to write to ~/.local, which violates the Nix sandbox
              sed -i '/_post_install()/d' setup.py
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
              install -Dm644 ${manifest.program}/img/icon_1.jpg $out/share/icons/hicolor/256x256/apps/${manifest.program}.jpg
            '';
          };
        });

      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs {inherit system;};
          pythonPackages = pkgs.python3Packages;
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              (pythonPackages.python.withPackages (ps: with ps; [
                gitpython
                # pyqt6
              ]))
              ruff
              mypy
              pyright
            ];
          };
        });
    };
}