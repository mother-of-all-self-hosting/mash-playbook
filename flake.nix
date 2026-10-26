{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    agru-src = {
      url = "github:etkecc/agru/v0.3.0";
      flake = false;
    };
  };
  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      agru-src,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        agru = pkgs.buildGo126Module {
          pname = "agru";
          version = "0.3.0";
          src = agru-src;
          vendorHash = null;
          # A source build carries no version stamp, so `agru -v` would print nothing,
          # and `just update -u` refuses agru versions it cannot confirm to be 0.3.0 or newer
          postPatch = ''
            substituteInPlace cmd/agru/main.go \
              --replace-fail 'kit.Version("", "")' 'kit.Version("", "", "v${version}")'
          '';
        };
      in
      with pkgs;
      {
        devShells.default = mkShell {
          buildInputs = [
            just
            mise
            ansible
            agru
            # bin/ansible-python.sh runs our scripts with the interpreter behind Ansible,
            # which on Nix does not see Ansible's own dependencies (such as PyYAML)
            python3Packages.pyyaml
          ];
          shellHook = ''
            echo "$(ansible --version)"
          '';
        };
      }
    );
}
