#!/usr/bin/sh

# This demo needs interactive input on stdin AND a second terminal for
# the TCP injectors, so the script starts the app in the foreground and
# prints what to do next.

cat <<'EOF'
--- starting app.py in the foreground ---

In a SECOND terminal opened in this directory you can run:

  ./send_tcp.py          # inject 3 events via TCP listener A (port 9001)
  ./send_tcp.py 9002     # inject 3 events via TCP listener B (port 9002)

In THIS terminal, type a line and press Enter to inject a CLI event.

Press Ctrl-C to stop. The engine prints its final counts on shutdown.

EOF

./app.py
