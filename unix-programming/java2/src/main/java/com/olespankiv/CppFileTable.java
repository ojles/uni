package com.olespankiv;

import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.TableColumn;
import javax.swing.table.TableColumnModel;
import java.util.ArrayList;

public class CppFileTable extends JTable {
    public CppFileTable() {
        super(new CppFileTableModel(new ArrayList<>()));
        refreshLayout();
    }

    public void refreshLayout() {
        TableColumnModel columnModel = getColumnModel();

        TableColumn checkedColumn = columnModel.getColumn(0);
        checkedColumn.setPreferredWidth(25);
        checkedColumn.setMinWidth(25);
        checkedColumn.setMaxWidth(25);

        TableColumn lineCountColumn = columnModel.getColumn(2);
        lineCountColumn.setPreferredWidth(80);
        lineCountColumn.setMinWidth(80);
        lineCountColumn.setMaxWidth(120);

        TableColumn charsCountColumn = columnModel.getColumn(3);
        charsCountColumn.setPreferredWidth(100);
        charsCountColumn.setMinWidth(100);
        charsCountColumn.setMaxWidth(100);
        charsCountColumn.setMaxWidth(150);

        TableColumn statusColumn = columnModel.getColumn(4);
        statusColumn.setPreferredWidth(60);
        statusColumn.setMinWidth(60);
        statusColumn.setMaxWidth(60);
        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(JLabel.CENTER);
        statusColumn.setCellRenderer(centerRenderer);
    }
}
