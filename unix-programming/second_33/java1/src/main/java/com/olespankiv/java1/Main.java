package com.olespankiv.java1;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Optional;

import static java.lang.System.err;
import static java.lang.System.out;


public class Main {
    private static final int ERR_INVALID_PARAM_NUMBER = 1;
    private static final int ERR_PARAM_NOT_DIR = 2;

    public static FileStatResult countLinesInFile(Path filePath) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath.toFile()))) {
            int lines = 0;
            while (reader.readLine() != null) {
                lines++;
            }
            return new FileStatResult(filePath, lines);
        } catch (IOException e) {
            throw new RuntimeException("Failed to count lines in file!", e);
        }
    }

    public static FileStatResult countCharsInFile(Path filePath) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath.toFile()))) {
            int characters = 0;
            String line;
            while ((line = reader.readLine()) != null) {
                characters += line.length() + 1;
            }
            return new FileStatResult(filePath, characters);
        } catch (IOException e) {
            throw new RuntimeException("Failed to count characters in file!", e);
        }
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            err.println("Invalid number of parameters!");
            System.exit(ERR_INVALID_PARAM_NUMBER);
        }

        if (args[0].equals("-h")) {
            out.println("Usage: search-files DIRECTORY");
            out.println("Searches for files in DIRECTORY with most lines and most characters");
            System.exit(0);
        }

        Path directoryPath = Paths.get(args[0]);

        if (!Files.isDirectory(directoryPath)) {
            err.println(directoryPath + " is not a directory!");
            System.exit(ERR_PARAM_NOT_DIR);
        }

        Optional<FileStatResult> mostLinesFile = Files.list(directoryPath)
            .filter(Files::isRegularFile)
            .map(Main::countLinesInFile)
            .sorted()
            .findFirst();

        Optional<FileStatResult> mostCharactersFile = Files.list(directoryPath)
            .filter(Files::isRegularFile)
            .map(Main::countCharsInFile)
            .sorted()
            .findFirst();

        if (!mostLinesFile.isPresent() && !mostCharactersFile.isPresent()) {
            out.println("No files found.");
        } else {
            FileStatResult mostLines = mostLinesFile.get();
            FileStatResult mostCharacters = mostCharactersFile.get();
            out.println("Most lines: " + mostLines.amount + " " + mostLines.filePath);
            out.println("Most chars: " + mostCharacters.amount + " " + mostCharacters.filePath);
        }
    }
}
