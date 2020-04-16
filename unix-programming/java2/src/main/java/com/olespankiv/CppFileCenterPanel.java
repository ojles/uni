package com.olespankiv;

import javax.swing.*;
import javax.swing.table.TableModel;
import java.awt.*;
import java.awt.event.ItemEvent;

public class CppFileCenterPanel extends JPanel {
    private FolderSelector sourceFolderSelector = new FolderSelector("Source folder");
    private FolderSelector destinationFolderSelector = new FolderSelector("Destination folder");
    private CppFileControls cppFileControls = new CppFileControls();
    private CppFileTable cppFileTable = new CppFileTable();

    public CppFileCenterPanel() {
        initSourceFolderSelector();
        initCppFileControls();

        setLayout(new BoxLayout(this, BoxLayout.PAGE_AXIS));
        setBorder(BorderFactory.createEmptyBorder(22, 32, 22, 32));
        add(sourceFolderSelector);
        add(Box.createRigidArea(new Dimension(0, 7)));
        add(destinationFolderSelector);
        add(Box.createRigidArea(new Dimension(0, 21)));
        add(cppFileControls);
        add(Box.createRigidArea(new Dimension(0, 7)));
        add(new JScrollPane(cppFileTable));
    }

    private void initSourceFolderSelector() {
        sourceFolderSelector.setOnFolderChanged(sourceFolder -> {
            java.util.List<CppFile> foundFiles = CppFileService.searchInFolder(sourceFolder);
            TableModel tableModel = new CppFileTableModel(foundFiles);
            cppFileTable.setModel(tableModel);
            cppFileTable.refreshLayout();
        });
    }

    private void requireSourceAndDestinationFolder() {
        if (!sourceFolderSelector.hasSelectedFolder()) {
            JOptionPane.showMessageDialog(
                    this, "Please specify source folder.", "Source folder empty", JOptionPane.ERROR_MESSAGE);
            return;
        }
        if (!destinationFolderSelector.hasSelectedFolder()) {
            JOptionPane.showMessageDialog(
                    this, "Please specify destination folder.", "Destination folder empty", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void initCppFileControls() {
        cppFileControls.setOnCheckAllToggled(e -> {
            boolean isChecked = e.getStateChange() == ItemEvent.SELECTED;
            CppFileTableModel model = (CppFileTableModel) cppFileTable.getModel();
            model.getFiles().forEach(file -> {
                file.setChecked(isChecked);
            });
            model.fireTableDataChanged();
        });
        cppFileControls.setOnMoveClicked(e -> {
            CppFileTableModel model = (CppFileTableModel) cppFileTable.getModel();
            requireSourceAndDestinationFolder();
            CppFileService.moveChecked(model.getFiles(), destinationFolderSelector.getSelectedFolder());
            model.fireTableDataChanged();
        });
        cppFileControls.setOnReturnClicked(e -> {
            CppFileTableModel model = (CppFileTableModel) cppFileTable.getModel();
            requireSourceAndDestinationFolder();
            CppFileService.returnChecked(model.getFiles(), destinationFolderSelector.getSelectedFolder());
            model.fireTableDataChanged();
        });
    }
}
