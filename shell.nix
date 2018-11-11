let
  pkgs = import <nixpkgs> {};
  python = import ./requirements.nix { inherit pkgs; };
in python.mkDerivation {
  name = "havesnippet";
  src = ./.;
  propagatedBuildInputs = builtins.attrValues python.packages;
}
