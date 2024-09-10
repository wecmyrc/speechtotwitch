let
  unstable = import (fetchTarball https://nixos.org/channels/nixos-unstable/nixexprs.tar.xz) { };
in
{ pkgs ? import <nixpkgs> {}}:
let
  fhs = pkgs.buildFHSUserEnv {
    name = "fhs-environment";

    targetPkgs = _: [
      unstable.micromamba
      unstable.portaudio
    ];

    profile = ''
      export TMPDIR='/var/tmp'
      set -e
      eval "$(micromamba shell hook --shell=posix)"
      export MAMBA_ROOT_PREFIX=${builtins.getEnv "PWD"}/.mamba
      micromamba create -f env.yml
      micromamba activate mamba-environment
      set +e
    '';
  };
in fhs.env
