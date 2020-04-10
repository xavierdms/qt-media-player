![alt text](https://github.com/xavierdms/qt-media-player/blob/master/walkthrough.gif "LICEcap GIF Walkthrough")

For this assignment, I started by adding the basic layout components (play, pause, stop, volume, and progress bar), then connecting them to
    functions in the code. Play/pause/stop were straight-forward since they correspond directly to a QMediaPlayer function each. For the layout, I decided to create my own buttons to create a consistent style inspired by synthwave aesthetics. It took a few tries to 
    settle on a color scheme, and several buttons were changed a few times as more were added to maintain visual balance.
    
I initially tried using a progress bar for the track progress but found that there was no simple way to have it update continuously so that 
    the visual effect of the song progressing was smooth enough. Switching to a slider made more sense, and it was easy to have it update continuously since the units for the media player position are in milliseconds by default. For the time stamps, I converted those ms to minutes and seconds and formatted the strings to display at the corresponding QLabels so that seconds would always have two digits. 
    
After that, adding the volume slider was easy since it works the same way as the progress slider. Moving the slider position on each    is
    connected to a signal that calls a function to update the volume of the player and the position of the track, respectively. Since the progress should also move on its own, the signal for position change in the track is also connected to a function that updates the position of the progress slider.

Once I added playlist functionality, I also added the next/previous buttons, and made some changes in the layout to accommodate them, and
    removed the file extensions from the track names so it would look more like a traditional media player. There were also a few iterations
    through the formatting of the title display to ensure long titles would fit. I looked into auto-scrolling horizontally, but settled on just using word wrap to display on multiple lines.

In the future I would like to work on this more and add shuffle and repeat options, as well as a way to load in a youtube playlist.



