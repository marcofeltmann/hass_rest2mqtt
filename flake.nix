{
  description = "REST2MQTT - Home Assistant integration";

  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlays.default ];
        };

        python = pkgs.python312;

        devPython = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          python = python;
          extraPackages = ps: with ps; [
            pytest
            pytest-asyncio
            mypy
            pylint
            ruff
            black
          ];
          overrides = pkgs.poetry2nix.overrides.withDefaults (self': super': {
            "pytest-homeassistant-custom-component" = super'.fetchPypi {
              pname = "pytest-homeassistant-custom-component";
              version = "0.2.0";
              sha256 = "sha256-example-replace-with-actual-checksum";
            };
          });
        };
      in
      {
        packages.default = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          python = python;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            devPython
            pkgs.poetry
          ];

          shellHook = ''
            echo "REST2MQTT dev shell loaded"
            echo "Python: $(python --version)"
          '';
        };
      }
    )
}