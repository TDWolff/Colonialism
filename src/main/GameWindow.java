import javax.swing.JFrame;

public class GameWindow {
    private JFrame frame;

    public GameWindow(int width, int height, String title) {
        frame = new JFrame(title); // Create a new JFrame with the given title
        frame.setSize(width, height); // Set the size
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Close on exit
        frame.setLocationRelativeTo(null); // Center the window on the screen
    }

    public void show() {
        frame.setVisible(true); // Make the window visible
    }
}
