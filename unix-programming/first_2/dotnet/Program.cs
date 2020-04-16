using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;

namespace dotnet
{
    class Program
    {
        private const int ERR_INVALID_USAGE = 1;
        private const int ERR_PARAM_NOT_DIR = 2;

        static int Main(string[] args)
        {
            if (args.Length >= 1 && args[0].Equals("-h"))
            {
                Console.WriteLine("Usage: copy-cpp SOURCE_DIR DESTINATION_DIR");
                Console.WriteLine("Move all .cpp files in subdirectories of SOURCE_DIR to DESTINATION_DIR");
                return 0;
            }
            if (args.Length != 2)
            {
                Console.Error.WriteLine("Invalid number of parameters!");
                Console.Error.WriteLine("Try 'copy-cpp -h' for more information.");
                return ERR_INVALID_USAGE;
            }
            if (!Directory.Exists(args[0]))
            {
                Console.Error.WriteLine($"{args[0]} parameters is not a directory!");
                return ERR_PARAM_NOT_DIR;
            }
            if (!Directory.Exists(args[1]))
            {
                Console.Error.WriteLine("Second parameters is not a directory!");
                return ERR_PARAM_NOT_DIR;
            }

            new List<string>(Directory.GetDirectories(args[0]))
                .SelectMany(Directory.GetFiles)
                .Where(file => file.EndsWith(".cpp"))
                .ToList()
                .ForEach(file => File.Move(file, Path.Combine(args[1], Path.GetFileName(file))));

            return 0;
        }
    }
}
