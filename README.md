# Voice_controlled_drawing_interface

A deep neural network that recognizes voice commands embedded into a small user interface.<br>

### Demo of the app

![demo](pictures/demo.mp4)

# Run the app
To run the program just download the "model.h5" and "voice_command_app.py" in the same directory.<br>
Navigate to that directory with CMD (for windows or equivalent for your OS) and run the program with the command:<br>
"python voice_command_app.py"

# App possibilities

There are 5 default controlls ['izbrisi', 'krug', 'kvadrat', 'oboji', 'trougao'](in serbian) or ['clear', 'circle', 'square', 'color', 'triangle'](translation).<br>
The circle, square, triangle commands draw the corresponding shapes. The color command colors the corresponding shapes in a random color.<br>
The clear command clears the screen. There is a "Voice command" button which records input from the microphone for 2s, and then the recognized<br>
action is executed. Keep in mind that the neural network was recognized on my voice samples (11 for each command), so it might not perform good<br>
on you own voice.

### "Circle"

![circle](pictures/circle.jpg)

### "Color"

![color](pictures/color.jpg)

### "Color"

![color1](pictures/color1.jpg)

### "Triangle"

![triangle](pictures/triangle.jpg)

### "Square"

![square](pictures/square.jpg)

### "Clear"

![clear](pictures/clear.jpg)

A added function is the "Train 'increase'" which lets the user train the model to pronunciation of the word 'increase' or 'povecaj'.<br>
What it does is makes the shape of the currently displayed shape bigger. The accuracy of the model can't be guaranteed after training<br>
since the weights of the model changed.

## "Increase"

![increase](pictures/increase.jpg)
