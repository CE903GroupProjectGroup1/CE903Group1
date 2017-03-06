python UDPlistener.py &
sleep 5
python DataTransformer.py &
python3 -m http.server 8000 &

