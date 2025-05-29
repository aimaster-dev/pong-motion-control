# ✋ Pong Game with Hand Gesture Control

This is an AI-powered Pong game that uses real-time hand gesture recognition to control paddles using your webcam. Open hands detected on either side of the screen move the paddles up or down — no keyboard or mouse needed!

<p align="center">
  <img src="pong.gif" width=800><br/>
  <i>Demo</i>
</p>

---

## 🎮 Features

- Real-time hand detection with **TensorFlow** and pre-trained model
- Gesture-based paddle movement (open hand = move)
- Split-screen detection for two-player interaction
- Pong gameplay with paddle & ball physics in **Pygame**
- Overlays interactive regions and visual cues using **OpenCV**

---

## 🧠 Technologies Used

- **TensorFlow** for hand detection
- **OpenCV** for camera feed and visualization
- **Pygame** for game mechanics
- **NumPy** for image and numerical operations

---

## 🛠️ Installation

1. Clone this repository  
```bash
git clone https://github.com/yourusername/pong-motion-control.git
cd pong-motion-control
````

2. Install dependencies

```bash
pip install pygame opencv-python tensorflow numpy
```

3. Add your pre-trained TensorFlow model to `src/pretrained_model.pb`

---

## ▶️ Run the Game

```bash
python pong_game.py
```

Press `SPACE` to start the game
Press `ESC` to exit

---

## 🎯 Controls

* Open your hand in the **top area** → Move paddle **up**
* Open your hand in the **bottom area** → Move paddle **down**

Left hand = Player 1
Right hand = Player 2

---

## 📂 File Structure

```
├── pong_game.py              # Main game file
├── src/
│   └── utils.py              # Hand detection and prediction utilities
│   └── pretrained_model.pb   # TensorFlow frozen inference graph
```

---

## 🧪 Notes

* Ensure your webcam is working and well-lit
* You can adjust thresholds and chunk size in the `FLAGS`

---

## 📜 License

MIT License – use, modify, and play freely!

---

## 🤖 Inspired by

Gesture-based gaming, AI-powered interfaces, and classic Pong nostalgia.
