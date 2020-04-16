package com.olespankiv;

import javax.swing.table.AbstractTableModel;
import java.util.List;

public class CppFileTableModel extends AbstractTableModel {
    private final String[] columnNames = {"", "Name", "Line count", "Chars count", "Status"};
    private final List<CppFile> files;

    public CppFileTableModel(List<CppFile> files) {
        this.files = files;
    }

    public void updateFiles(List<CppFile> files) {
        this.files.clear();
        this.files.addAll(files);
    }

    public List<CppFile> getFiles() {
        return files;
    }

    @Override
    public int getRowCount() {
        return files.size();
    }

    @Override
    public int getColumnCount() {
        return columnNames.length;
    }

    @Override
    public Object getValueAt(int row, int column) {
        CppFile file = files.get(row);
        switch (column) {
            case 0:
                return file.isChecked();
            case 1:
                return file.getRelativePath();
            case 2:
                return file.getLineCount();
            case 3:
                return file.getCharsCount();
            case 4:
                return file.getStatus() == CppFile.Status.MOVED
                    ? "✓"
                    : "";

            default:
                throw new RuntimeException("Invalid get table column = " + column);
        }
    }

    @Override
    public String getColumnName(int column) {
        return columnNames[column];
    }

    @Override
    public Class getColumnClass(int column) {
        return getValueAt(0, column).getClass();
    }

    @Override
    public boolean isCellEditable(int row, int column) {
        return column == 0;
    }

    @Override
    public void setValueAt(Object value, int row, int column) {
        CppFile file = files.get(row);
        if (column == 0) {
            file.setChecked((boolean) value);
        } else {
            throw new RuntimeException("Invalid edit table column = " + column);
        }
    }
}
