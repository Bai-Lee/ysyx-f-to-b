marco(){ MARCO_DIR=$PWD; }
polo(){ [[ -v MARCO_DIR ]] && cd -- "$MARCO_DIR"; }
