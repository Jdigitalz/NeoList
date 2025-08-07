#!/bin/bash
cd ../..
CMD_NAME="neolist"

if [[ $EUID -ne 0 ]]; then
    INSTALL_DIR="$HOME/.local/bin"
else
    INSTALL_DIR="/usr/local/bin"
fi

if [[ -f "$INSTALL_DIR/$CMD_NAME" ]]; then
    echo "Removing $CMD_NAME from $INSTALL_DIR..."
    rm "$INSTALL_DIR/$CMD_NAME"
    echo "✅ Uninstalled $CMD_NAME."
else
    echo "❌ $CMD_NAME is not installed in $INSTALL_DIR."
fi

