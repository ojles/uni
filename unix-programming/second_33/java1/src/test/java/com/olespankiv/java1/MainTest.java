package com.olespankiv.java1;

import org.junit.Rule;
import org.junit.Test;
import org.junit.contrib.java.lang.system.ExpectedSystemExit;
import org.junit.contrib.java.lang.system.SystemOutRule;
import org.junit.rules.TemporaryFolder;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

import static org.junit.Assert.assertEquals;

public class MainTest {
    @Rule
    public ExpectedSystemExit expectedSystemExit = ExpectedSystemExit.none();
    @Rule
    public SystemOutRule systemOutRule = new SystemOutRule().enableLog();
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
    public void errorCodeIsReturnedWhenParameterIsNotDirectory() throws IOException {
        expectedSystemExit.expectSystemExitWithStatus(2);

        File file = temporaryFolder.newFile();
        Main.main(new String[]{
                file.getAbsolutePath()
        });
    }

    @Test
    public void whenDirectoryIsEmptyCorrespondingMessageIsPrinted() throws IOException {
        Main.main(new String[]{
                temporaryFolder.getRoot().getAbsolutePath()
        });

        assertEquals("No files found.\n", systemOutRule.getLog());
    }

    @Test
    public void shouldReturnMaxLinesAndMaxCharsFile() throws IOException {
        File mostLinesFile = temporaryFolder.newFile("1.txt");
        File mostCharsFile = temporaryFolder.newFile("2.txt");
        File otherFile = temporaryFolder.newFile("3.txt");

        try (PrintWriter out = new PrintWriter(mostLinesFile)) {
            out.print("1: lskjfs\n" +
                    "2: sldkflsdf\n" +
                    "3: sldfjslkdf\n" +
                    "4: sldfjslkdf\n" +
                    "5: sldkfsS sd\n" +
                    "6: sldkfs\n" +
                    "7: sldkfsl sldkf\n" +
                    "8: sldkfs\n" +
                    "9: lwweork\n" +
                    "10: sldkfs\n");
        }

        try (PrintWriter out = new PrintWriter(mostCharsFile)) {
            out.print("1: lskj'sweoirq()-3'werd)\n" +
                    "2: qpwerpoweirq()+3'cv,m)\n" +
                    "3: sldqpweoirpq()/3'erkf)\n" +
                    "4: sldqpweoirpq()/3'erkf)\n" +
                    "5: sldkf,asdfbq()&3'defg)\n" +
                    "6: 02394029341q()^3'3777)\n" +
                    "7: sldkf,asdfbq()&3'defg)\n" +
                    "8: sldkf,asdfbq()&3'defg)\n" +
                    "9: sldkf,asdfbq()&3'defg)\n");
        }

        try (PrintWriter out = new PrintWriter(otherFile)) {
            out.print("Lorem Ipsum is simply dummy text of the printing and typesetting industry.\n" +
                    "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.\n");
        }

        Main.main(new String[]{
                temporaryFolder.getRoot().getAbsolutePath()
        });

        String expectedOutput = "Most lines: 10 " + mostLinesFile.getAbsolutePath()
                + "\nMost chars: 234 " + mostCharsFile.getAbsolutePath()
                + "\n";
        assertEquals(expectedOutput, systemOutRule.getLog());
    }
}
