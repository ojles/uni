package com.olespankiv.java1;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.function.Function;

import static java.lang.System.err;
import static java.lang.System.out;

public class Main {
    private static final int ERR_INVALID_USAGE = 1;
    private static final int ERR_PARAM_NOT_DIR = 2;

    public static void main(String[] args) throws IOException {
        if (args.length >= 1 && args[0].equals("-h")) {
            out.println("Usage: copy-cpp SOURCE_DIR DESTINATION_DIR");
            out.println("Move all .cpp files in subdirectories of SOURCE_DIR to DESTINATION_DIR");
            System.exit(0);
        }

        if (args.length != 2) {
            err.println("Invalid number of parameters!");
            err.println("Try 'copy-cpp -h' for more information.");
            System.exit(ERR_INVALID_USAGE);
        }

        Path sourceDirectory = Paths.get(args[0]);
        Path destinationDirectory = Paths.get(args[1]);

        if (!Files.isDirectory(sourceDirectory)) {
            err.println("First parameters is not a directory!");
            System.exit(ERR_PARAM_NOT_DIR);
        }

        if (!Files.isDirectory(destinationDirectory)) {
            err.println("Second parameters is not a directory!");
            System.exit(ERR_PARAM_NOT_DIR);
        }

        Files.list(sourceDirectory)
            .filter(Files::isDirectory)
            .map(subdirectory -> {
                try {
                    return Files.find(
                            subdirectory,
                            Integer.MAX_VALUE,
                            (path, attributes) -> path.toString().endsWith(".cpp")
                    );
                } catch (IOException e) {
                    throw new RuntimeException("Unexpected I/O error!", e);
                }
            })
            .flatMap(Function.identity())
            .forEach(path -> {
                File sourceFile = path.toFile();
                File destinationFile = new File(destinationDirectory.toFile(), sourceFile.getName());
                sourceFile.renameTo(destinationFile);
            });
    }
}
