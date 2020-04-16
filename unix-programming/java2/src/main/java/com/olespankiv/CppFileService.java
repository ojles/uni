package com.olespankiv;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

public class CppFileService {
    private static int countLinesInFile(Path filePath) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath.toFile()))) {
            int lines = 0;
            while (reader.readLine() != null) {
                lines++;
            }
            return lines;
        } catch (IOException e) {
            throw new RuntimeException("Failed to count lines in file!", e);
        }
    }

    private static int countCharsInFile(Path filePath) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath.toFile()))) {
            int charsCount = 0;
            String line;
            while ((line = reader.readLine()) != null) {
                charsCount += line.length() + 1;
            }
            return charsCount;
        } catch (IOException e) {
            throw new RuntimeException("Failed to count characters in file!", e);
        }
    }

    private static CppFile createCppFile(Path filePath, String folder) {
        String absolutePath = filePath.toAbsolutePath().toString();
        String relativePath = absolutePath.substring(folder.length());
        if (relativePath.charAt(0) == '/') {
            relativePath = relativePath.substring(1);
        }

        return new CppFile(
                absolutePath,
                relativePath,
                countLinesInFile(filePath),
                countCharsInFile(filePath)
        );
    }

    public static List<CppFile> searchInFolder(String folder) {
        try {
            Path folderPath = Paths.get(folder);
            return Files.find(
                        folderPath,
                        Integer.MAX_VALUE,
                        (path, attributes) -> path.toString().endsWith(".cpp")
                    )
                    .map(path -> createCppFile(path, folder))
                    .collect(Collectors.toList());
        } catch (IOException e) {
            throw new RuntimeException("Failed to search for cpp files in " + folder);
        }
    }

    public static void moveChecked(List<CppFile> files, String destinationFolder) {
        files.stream()
                .filter(CppFile::isChecked)
                .forEach(file -> {
                    File sourceFile = new File(file.getAbsolutePath());
                    File destinationFile = new File(destinationFolder, sourceFile.getName());
                    sourceFile.renameTo(destinationFile);
                    file.setStatus(CppFile.Status.MOVED);
                });
    }

    public static void returnChecked(List<CppFile> files, String destinationFolder) {
        files.stream()
                .filter(CppFile::isChecked)
                .forEach(file -> {
                    File sourceFile = new File(file.getAbsolutePath());
                    File destinationFile = new File(destinationFolder, sourceFile.getName());
                    destinationFile.renameTo(sourceFile);
                    file.setStatus(CppFile.Status.NOT_CHANGED);
                });
    }
}
