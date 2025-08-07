#!/bin/bash
cd ../..
CMD_NAME="neolist"
SCRIPT_NAME="neolist.py"

if [[ $EUID -ne 0 ]]; then
    INSTALL_DIR="$HOME/.local/bin"
else
    INSTALL_DIR="/usr/local/bin"
fi

if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if python3 -c "import rich" &>/dev/null; then
    echo "✅ 'rich' is already installed."
else
    if command -v pipx &>/dev/null; then
        echo "Installing 'rich' using pipx..."
        if ! pipx install rich-cli &>/dev/null; then
            echo "❌ pipx failed to install 'rich'."
            echo "Please install it manually with: pip3 install rich"
            exit 1
        fi
    else
        echo "❌ pipx is not installed."
        echo "To install pipx, run:"
        echo "  python3 -m pip install --user pipx"
        echo "  python3 -m pipx ensurepath"
        echo
        echo "Then re-run this installer. Or, install 'rich' manually with:"
        echo "  pip3 install --user rich"
        exit 1
    fi
fi

mkdir -p "$INSTALL_DIR"
chmod +x "$SCRIPT_NAME"
echo "Installing $CMD_NAME to $INSTALL_DIR..."
cp "$SCRIPT_NAME" "$INSTALL_DIR/$CMD_NAME"

echo
echo "✅ Installed! You can now run: $CMD_NAME"
echo "📌 Make sure $INSTALL_DIR is in your PATH."

