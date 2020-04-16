package com.olespankiv.java1;

import java.nio.file.Path;

public class FileStatResult implements Comparable<FileStatResult> {
    public Path filePath;
    public int amount;

    public FileStatResult(Path filePath, int amount) {
        this.filePath = filePath;
        this.amount = amount;
    }

    @Override
    public int compareTo(FileStatResult other) {
        return -Integer.compare(this.amount, other.amount);
    }
}
