# Pygame PING-PONG (2P)

- boot.dev personal project (20~30 hours)

> My intention was building web-socket 1vs1 game, but
> it was too hard to finish basic ping pong logic in 30 hours...

1. Create Base classes (rectangle, circle)
2. Game Logic

   - Tricky Part
     - Collision Detection and fix the turnneling problem
     - How to Fix:
       - reflect with normal vector (add up way for corner detection)
       - inside handling (turnneling): throw logic (change velocity to opposite direction)
   - Player Control
     - P1: WASD, P2: Arrow Keys

3. Game UI

   - Basic Point, Reset feature

4. Additional Angle & Speed Increment
   - Add additional angle with hit position y, clamp by each 60 degrees
   - speed increment by each hit
![Uploading ScreenRecording2025-05-14at4.06.44PM-ezgif.com-video-to-gif-converter.gif…]()
