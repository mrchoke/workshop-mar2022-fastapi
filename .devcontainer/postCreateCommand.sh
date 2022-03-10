#!/usr/bin/zsh
source  $HOME/.zshrc
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting

omz plugin enable zsh-autosuggestions
omz plugin enable zsh-syntax-highlighting

python -m pip install -U autopep8
