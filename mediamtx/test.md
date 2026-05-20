ffmpeg -re -i test.mp4 -c copy -f rtsp rtsp://localhost:666/mystream
vlc -I dummy "test.mp4" --sout "#transcode{vcodec=h264,venc=x264{preset=ultrafast}}:rtp{sdp=rtsp://:6666/mystream}" --loop
vlc -I dummy "test.mp4" --sout "#transcode{vcodec=h264,venc=x264{preset=ultrafast,tune=zerolatency}}:rtp{mux=ts,sdp=rtsp://:6666/mystream}" --sout-mux-caching=5000 --loop

❯ mediamtx ./test.yml