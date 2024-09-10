# heavily inspired by:
# https://stackoverflow.com/questions/77835393/poetry2nix-flake-build-errors-because-the-poetry2nix-overrides-attribute-seems
# https://github.com/nix-community/poetry2nix/blob/8ffbc64abe7f432882cb5d96941c39103622ae5e/docs/edgecases.md#modulenotfounderror-no-module-named-packagename

{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
      in
      {
        packages = {
          stt = poetry2nix.mkPoetryApplication {
            packageName = "stt";
            projectDir = ./.;

            overrides = poetry2nix.overrides.withDefaults (
              self: super: {
                pyaudio = super.pyaudio.overridePythonAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ pkgs.portaudio ];
                });
                dash-mantine-components = super.dash-mantine-components.overridePythonAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                });
                twitch-chat-irc = super.twitch-chat-irc.overridePythonAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                });
                dash-iconify = super.dash-iconify.overridePythonAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                });
              }
            );
          };
          default = self.packages.${system}.stt;
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.stt ];
          packages = with pkgs; [
            poetry
          ];
        };
      }
    );
}
