{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    agru-src = {
      url = "github:etkecc/agru";
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
          version = "0.2.1";
          src = agru-src;
          vendorHash = null;
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
            python3Packages.regex
          ];
          shellHook = ''
            echo "$(ansible --version)"
            echo "$(python3 -c 'import regex; print("Python regex lib available!")')"
          '';
        };
      }
    );
}
