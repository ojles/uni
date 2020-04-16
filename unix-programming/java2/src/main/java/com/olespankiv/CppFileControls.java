package com.olespankiv;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ItemEvent;
import java.util.function.Consumer;

public class CppFileControls extends JPanel {
    private JCheckBox checkAllCheckBox = new JCheckBox();
    private JButton moveButton = new JButton();
    private JButton returnButton = new JButton();

    public CppFileControls() {
        checkAllCheckBox.setText("Check all");

        moveButton.setMaximumSize(new Dimension(200, 200));
        moveButton.setPreferredSize(new Dimension(101, 25));
        moveButton.setText("Move");

        returnButton.setMaximumSize(new Dimension(200, 200));
        returnButton.setPreferredSize(new Dimension(101, 25));
        returnButton.setText("Return");

        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        add(Box.createRigidArea(new Dimension(2, 0)));
        add(checkAllCheckBox);
        add(Box.createHorizontalGlue());
        add(moveButton);
        add(Box.createRigidArea(new Dimension(7, 0)));
        add(returnButton);
    }

    public void setOnCheckAllToggled(Consumer<ItemEvent> eventHandler) {
        checkAllCheckBox.addItemListener(eventHandler::accept);
    }

    public void setOnMoveClicked(Consumer<ActionEvent> eventHandler) {
        moveButton.addActionListener(eventHandler::accept);
    }

    public void setOnReturnClicked(Consumer<ActionEvent> eventHandler) {
        returnButton.addActionListener(eventHandler::accept);
    }
}
