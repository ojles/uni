using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;

namespace dotnet
{
    class Program
    {
        private const int ERR_INVALID_PARAM_NUMBER = 1;
        private const int ERR_PARAM_NOT_DIR = 2;

        static int Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.Error.WriteLine("Invalid number of parameters!");
                return ERR_INVALID_PARAM_NUMBER;
            }
            if (args[0].Equals("-h"))
            {
                Console.WriteLine("Usage: search-files DIRECTORY");
                Console.WriteLine("Searches for files in DIRECTORY with most lines and most characters");
                return 0;
            }
            if (!Directory.Exists(args[0]))
            {
                Console.Error.WriteLine($"'{args[0]}' is not a directory!");
                return ERR_PARAM_NOT_DIR;
            }

            var fileList = new List<string>(Directory.GetFiles(args[0]));
            if (fileList.Count == 0)
            {
                Console.WriteLine("No files found.");
                return 0;
            }

            var mostLinesFile = fileList
                .Select(filePath =>
                    new
                    {
                        FilePath = filePath,
                        LineCount = File.ReadLines(filePath).Count()
                    })
                .OrderBy(file => file.LineCount)
                .Last();

            var mostCharsFile = fileList
                .Select(filePath =>
                    new
                    {
                        FilePath = filePath,
                        CharsCount = File.ReadLines(filePath).Select(line => line.Length + 1).Sum()
                    })
                .OrderBy(file => file.CharsCount)
                .Last();

            Console.WriteLine($"Most lines: {mostLinesFile.LineCount} {mostLinesFile.FilePath}");
            Console.WriteLine($"Most chars: {mostCharsFile.CharsCount} {mostCharsFile.FilePath}");
            return 0;
        }
    }
}

