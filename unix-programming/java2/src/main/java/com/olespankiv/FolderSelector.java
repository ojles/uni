package com.olespankiv;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.File;
import java.util.function.Consumer;

public class FolderSelector extends JPanel {
    private JLabel folderPathLabel = new JLabel();
    private JButton browseButton = new JButton();

    private String prefix;
    private String selectedFolder = null;
    private Consumer<String> onFolderChanged;

    public FolderSelector(String prefix) {
        this.prefix = prefix;

        browseButton.setText("Browse...");
        browseButton.setMaximumSize(new Dimension(200, 200));
        browseButton.setPreferredSize(new Dimension(102, 25));
        browseButton.addActionListener(this::browseButtonClickHandler);

        Font oldFond = folderPathLabel.getFont();
        Font newFont = oldFond.deriveFont(oldFond.getStyle() | Font.ITALIC);
        folderPathLabel.setFont(newFont);

        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        add(new JLabel(prefix + ":"));
        add(Box.createRigidArea(new Dimension(10, 0)));
        add(folderPathLabel);
        add(Box.createHorizontalGlue());
        add(browseButton);
    }

    public String getSelectedFolder() {
        return selectedFolder;
    }

    public boolean hasSelectedFolder() {
        return selectedFolder != null;
    }

    public void setOnFolderChanged(Consumer<String> onFolderChanged) {
        this.onFolderChanged = onFolderChanged;
    }

    private void browseButtonClickHandler(ActionEvent event) {
        JFileChooser chooser = new JFileChooser();
        chooser.setCurrentDirectory(new File("."));
        chooser.setDialogTitle(prefix);
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        chooser.setAcceptAllFileFilterUsed(false);

        if (chooser.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
            selectedFolder = chooser.getSelectedFile().getAbsolutePath();
            folderPathLabel.setText(selectedFolder);
            if (onFolderChanged != null) {
                onFolderChanged.accept(selectedFolder);
            }
        }
    }
}
