using System.Collections.Generic;
using System.Linq;


struct Fold
{
    public char axis;
    public int value;
    public Fold(char axis, int value)
    {
        this.axis = axis;
        this.value = value;
    }
}


public class Folding
{
    public static void Main(string[] args)
    {
        // Read in file
        string[] lines = System.IO.File.ReadAllLines(args[0]);
        List<(int, int)> points = new List<(int, int)>();
        List<Fold> folds = new List<Fold>();

        // Process input file
        foreach(string line in lines)
        {
            if(line.StartsWith("fold along"))
            {
                string[] parts = line.Split('=');
                char axis = parts[0][parts[0].Length-1];
                int value = Int32.Parse(parts[1].Trim());
                folds.Add(new Fold(axis, value));
            } 
            else if(!String.IsNullOrEmpty(line))
            {
                string[] parts = line.Split(',');
                int x = Int32.Parse(parts[0].Trim());
                int y = Int32.Parse(parts[1].Trim());
                points.Add((x, y));
            }
        }

        // Create first paper from points
        Paper paper = new Paper(points);

        // Part 1: Number of visible points after first fold:
        paper.DoFold(folds[0]);
        Console.WriteLine($"Number of points after first fold: {paper.NumPoints()}");

        // Part 2: Finish folding, display:
        foreach(Fold fold in folds.GetRange(1, folds.Count-1))
        {
            paper.DoFold(fold);
        }

        paper.Print();
    }
}


class Paper
{
    List<(int, int)> points;

    public Paper(List<(int, int)> points)
    {
        this.points = points;
    }

    public int NumPoints() => points.Count;

    public void DoFold(Fold fold)
    {
        points = points.Select(p => FoldPoint(p, fold.axis, fold.value)).Distinct().ToList();
    }

    private (int, int) FoldPoint((int, int) point, char axis, int value)
    {
        if(axis == 'x')
        {
            int diff = point.Item1 - value;
            return diff > 0 ? (value - diff, point.Item2) : point;
        }
        else 
        {
            int diff = point.Item2 - value;
            return diff > 0 ? (point.Item1, value - diff) : point;
        }
    }

    public void Print()
    {
        // Convert points to set for O(1) lookup
        HashSet<(int, int)> set = new HashSet<(int, int)>(points);
        // Find grid size
        int maxX = points.Select(p => p.Item1).Max() + 1;
        int maxY = points.Select(p => p.Item2).Max() + 1;

        for(int j = 0; j < maxY; j++)
        {
            for(int i = 0; i < maxX; i++)
            {
                Console.Write(set.Contains((i, j)) ? '#' : '.');
            }
            Console.Write('\n');
        }
    }
}