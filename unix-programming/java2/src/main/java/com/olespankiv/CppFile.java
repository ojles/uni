package com.olespankiv;

import java.nio.file.Path;

public class CppFile {
    enum Status {
        NOT_CHANGED,
        MOVED,
        ERROR;
    }

    private String absolutePath;
    private String relativePath;
    private boolean isChecked;
    private int lineCount;
    private int charsCount;
    private Status status;

    CppFile(String absolutePath, String relativePath, int lineCount, int charsCount) {
        this.absolutePath = absolutePath;
        this.relativePath = relativePath;
        this.lineCount = lineCount;
        this.charsCount = charsCount;
        this.isChecked = false;
        this.status = Status.NOT_CHANGED;
    }

    public String getAbsolutePath() {
        return absolutePath;
    }

    public String getRelativePath() {
        return relativePath;
    }

    public boolean isChecked() {
        return isChecked;
    }

    public void setChecked(boolean checked) {
        isChecked = checked;
    }

    public int getLineCount() {
        return lineCount;
    }

    public int getCharsCount() {
        return charsCount;
    }

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }
}
