PLAY - start video playback
PAUSE - pause the video
STOP - stop video playback

File -> New video - Select a new video for the editor
File -> Save - Save the current video

Edit -> Undo - Undo the change
Edit -> Redo - Redo the change

Actions -> Start writing - Start recording actions
Actions -> Stop writing - Stop recording actions
Actions -> Save - Save the sequence of actions for future use
Actions -> Load - Load the sequence of actions and execute it

Actions:
1) Change speed - enter the value of the new speed in the window to the left of the "Set speed" button and click "Set speed" (The two windows to the left indicate the boundaries of application). The speed value should be positive. If you leave the value in the left window as "1", nothing will happen when you click the button. The closer the value of the new speed is to "0", the longer the processing takes, so it is not recommended to set very low values.

2) Rotate the image - enter the counterclockwise rotation degree in the window to the left of the "Rotate" button and click "Rotate". Selecting the "Reshape" flag determines whether the video extension will adjust to the new image. By default, the video extension remains unchanged, so part of the image is cropped during rotation.

3) Cut a fragment - in the two windows to the left of the "Cut" button, enter the left and right boundaries of the fragment to be cut. Values in frames. The value in the left window should be >= 0 and < the value in the right window. The value in the right window should be <= the number of frames in the video and > the value in the left window. By default, the right window is set to the number of frames.

4) Insert a static image - first, choose an image to insert by clicking the "Choose photo" button, then enter the left and right boundaries in frames in the windows to the left of the "Add photo" button. Then click the "Add photo" button. Values in the windows are set similarly to the "Cut a fragment" action.

5) Merge fragments - choose the second fragment by clicking the "Choose fragment" button, then click the "Put on the left" or "Put on the right" button - insert the second fragment to the left or right of the current video. The extension of the resulting video is always equal to the extension of the first original video.

6) Crop - below the video window, copy the crop boundaries horizontally, and to the right of the video window, copy the crop boundaries vertically. Then click the "Crop" button. The boundary values should be non-negative, should not exceed the number of pixels in the video along the current axis, and the left boundary should be < the right boundary, and the top should be < the bottom, respectively.
