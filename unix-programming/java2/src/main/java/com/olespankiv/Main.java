package com.olespankiv;

import javax.swing.*;
import java.awt.*;

public class Main extends JFrame {
    private void initWindow() {
        setSize(800, 600);
        setTitle("Java 2 Task");
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    public Main() {
        Container contentPane = getContentPane();
        contentPane.add(new CppFileCenterPanel(), BorderLayout.CENTER);
        initWindow();
    }

    public static void main(String[] args) {
        new Main();
    }
}
