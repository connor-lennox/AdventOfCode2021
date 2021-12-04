using System;
using System.Collections.Generic;
using System.Linq;

namespace Day4
{
    public class BingoMain
    {
        public static void Main(string[] args)
        {
            string[] lines = System.IO.File.ReadAllLines(args[0]);
            int[] calls = lines[0].Split(',').Select(i => Int32.Parse(i)).ToArray();

            List<BingoBoard> boards = GenerateBoards(lines);

            int firstScore = FindFirstWinningBoard(calls, boards);

            foreach(BingoBoard b in boards)
            {
                b.Reset();
            }

            int lastScore = FindLastWinningBoard(calls, boards);

            Console.WriteLine($"Score of First Winning Board: {firstScore}");
            Console.WriteLine($"Score of Last Winning Board: {lastScore}");
        }

        private static int FindFirstWinningBoard(int[] calls, List<BingoBoard> boards)
        {
            foreach(int num in calls)
            {
                foreach(BingoBoard b in boards)
                {
                    // See if this made the board winning
                    if(b.Mark(num))
                    {
                        return(b.Score() * num);
                    }
                }
            }

            return -1;
        }

        private static int FindLastWinningBoard(int[] calls, List<BingoBoard> boards)
        {
            HashSet<BingoBoard> unfinishedBoards = new HashSet<BingoBoard>(boards);

            foreach(int num in calls)
            {
                foreach(BingoBoard b in boards)
                {
                    if(b.Mark(num))
                    {
                        unfinishedBoards.Remove(b);
                        if(unfinishedBoards.Count == 0)
                        {
                            return(b.Score() * num);
                        }
                    }
                }
            }

            return -1;
        }

        private static List<BingoBoard> GenerateBoards(string[] lines)
        {
            List<BingoBoard> boards = new List<BingoBoard>();

            int lineCount = 0;
            int[,] data = new int[5, 5];

            for(int i = 1; i < lines.Length; i++)
            {
                if(String.IsNullOrWhiteSpace(lines[i])) continue;

                string[] parts = lines[i].Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
                int[] nums = parts.Select(i => Int32.Parse(i)).ToArray();
                for(int j = 0; j < 5; j++)
                {
                    data[lineCount,j] = nums[j];
                }
                lineCount++;

                if(lineCount == 5)
                {
                    boards.Add(new BingoBoard(data));
                    lineCount = 0;
                    data = new int[5,5];
                }
            }

            return boards;
        }
    }
}