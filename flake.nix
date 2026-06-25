{
  description = "REST2MQTT - Home Assistant integration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
    pre-commit-hooks.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, pre-commit-hooks }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        python = pkgs.python313;

        pythonWithDeps = pkgs.python313.withPackages (ps: with ps; [
          homeassistant
          paho-mqtt
          aiohttp
        ]);

        devPython = pkgs.python313.withPackages (ps: with ps; [
          pytest
          pytest-asyncio
          mypy
          pylint
          ruff
          black
        ]);
      in
      {
        packages.default = pythonWithDeps;

        devShells.default = pkgs.mkShell {
          buildInputs = [
            devPython
            pkgs.pre-commit
            pkgs.git
          ];

          shellHook = ''
            echo "REST2MQTT dev shell loaded"
            echo "Python: $(python --version)"
          '';
        };
      }
    );
}
