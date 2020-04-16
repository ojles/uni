package com.olespankiv.java1;

import org.junit.Rule;
import org.junit.Test;
import org.junit.contrib.java.lang.system.ExpectedSystemExit;
import org.junit.rules.TemporaryFolder;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class MainTest {
    @Rule
    public ExpectedSystemExit expectedSystemExit = ExpectedSystemExit.none();
    @Rule
    public TemporaryFolder temporaryFolder = new TemporaryFolder();

    @Test
    public void helpParameterIsRecognized() throws IOException {
        expectedSystemExit.expectSystemExitWithStatus(0);
        Main.main(new String[]{"-h"});
    }

    @Test
    public void errorCodeIsReturnedWhenInvalidNumberOfParameters() throws IOException {
        expectedSystemExit.expectSystemExitWithStatus(1);
        Main.main(new String[]{});
    }

    @Test
    public void errorCodeIsReturnedWhenFirstParameterIsNotDirectory() throws IOException {
        expectedSystemExit.expectSystemExitWithStatus(2);

        File file = temporaryFolder.newFile();
        Main.main(new String[]{
                file.getAbsolutePath(),
                temporaryFolder.getRoot().getAbsolutePath()
        });
    }

    @Test
    public void errorCodeIsReturnedWhenSecondParameterIsNotDirectory() throws IOException {
        expectedSystemExit.expectSystemExitWithStatus(2);

        File file = temporaryFolder.newFile();
        Main.main(new String[]{
                temporaryFolder.getRoot().getAbsolutePath(),
                file.getAbsolutePath()
        });
    }

    @Test
    public void cppFilesInAllSubdirectoriesShouldBeMovedToDestination() throws IOException {
        File sourceDir = temporaryFolder.newFolder();
        File destinationDir = temporaryFolder.newFolder();

        new File(sourceDir, "1.cpp").createNewFile();
        File firstSubDir = new File(sourceDir, "first"); firstSubDir.mkdir();
        new File(firstSubDir, "2.cpp").createNewFile();
        File secondSubDir = new File(sourceDir, "second"); secondSubDir.mkdir();
        new File(secondSubDir, "3.cpp").createNewFile();
        new File(secondSubDir, "4.cpp").createNewFile();

        Main.main(new String[]{
                sourceDir.getAbsolutePath(),
                destinationDir.getAbsolutePath()
        });

        assertFalse(new File(destinationDir, "1.cpp").exists());
        assertTrue(new File(destinationDir, "2.cpp").exists());
        assertTrue(new File(destinationDir, "3.cpp").exists());
        assertTrue(new File(destinationDir, "4.cpp").exists());
    }
}
