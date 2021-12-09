using System.Collections.Generic;

public class LavaTube 
{
    public static void Main(string[] args)
    {
        // Read in heightmap file
        string[] lines = System.IO.File.ReadAllLines(args[0]);
        int gridHeight = lines.Length;
        int gridWidth = lines[0].Length;
        int[,] heights = new int[gridHeight,gridWidth];
        
        // Parse heightmap lines
        for(int i = 0; i < gridHeight; i++) 
        {    
            for(int j = 0; j < gridWidth; j++)
            {
                heights[i,j] = Int32.Parse(lines[i][j].ToString());
            }
        }

        HeightMap heightMap = new HeightMap(heights, gridHeight, gridWidth);

        // Part 1: Iterate through all the grid positions and find minimums
        int sumRisk = 0;
        for(int i = 0; i < gridHeight; i++)
        {
            for(int j = 0; j < gridWidth; j++)
            {
                if(heightMap.IsMinimum(i, j))
                {
                    sumRisk += heightMap.heights[i,j] + 1;
                }
            }
        }

        Console.WriteLine($"Part 1: Sum of Risk Levels: {sumRisk}");
        Console.WriteLine($"Part 2: Product of Top Three Basin Sizes: {heightMap.GetBasinProduct()}");
    }

}

class HeightMap
{
    private int gridHeight;
    private int gridWidth;
    public int[,] heights;

    public HeightMap(int[,] heights, int gridHeight, int gridWidth)
    {
        this.heights = heights;
        this.gridHeight = gridHeight;
        this.gridWidth = gridWidth;
    }

    public bool IsMinimum(int i, int j)
    {
        // Check all positions around center point (i, j)
        int center = heights[i,j];
        if(i > 0 && heights[i-1,j] <= center) return false;
        if(i < gridHeight-1 && heights[i+1,j] <= center) return false;
        if(j > 0 && heights[i,j-1] <= center) return false;
        if(j < gridWidth-1 && heights[i,j+1] <= center) return false;

        return true;
    }

    public int GetBasinProduct()
    {
        // Part 2: Floodfill to find all basins, multiply together top three sizes

        // Keep track of which positions have been assigned to a basin
        bool[,] basinAssignments = new bool[gridHeight,gridWidth];
        List<int> basinSizes = new List<int>();

        for(int i = 0; i < gridHeight; i++)
        {
            for(int j = 0; j < gridWidth; j++)
            {
                // If we're at a position that is not assigned to a basin, that isn't a 9
                if(!basinAssignments[i,j] && heights[i,j] != 9)
                {
                    // Floodfill a basin
                    basinSizes.Add(FindBasin(basinAssignments, i, j));
                }
            }
        }

        // Find the top three basin sizes
        basinSizes.Sort();
        basinSizes.Reverse();

        return basinSizes[0] * basinSizes[1] * basinSizes[2];
    }

    private int FindBasin(bool[,] assignments, int i, int j)
    {
        // Prep work: create open list for floodfill
        int size = 0;
        List<(int, int)> open = new List<(int, int)>();
        open.Add((i, j));
        assignments[i,j] = true;
        size++;
        while(open.Count > 0)
        {
            // Pop the next element from the list
            (int, int) cur = open[0];
            open.RemoveAt(0);

            int x = cur.Item1;
            int y = cur.Item2;

            // Expand position in all four directions
            // Must be 1. in bounds, 2. not already assigned, 3. not of height 9
            if(x > 0 && !assignments[x-1,y] && heights[x-1,y] != 9)
            {
                open.Add((x-1, y));
                assignments[x-1,y] = true;
                size++;
            }
            if(x < gridHeight-1 && !assignments[x+1,y] && heights[x+1,y] != 9)
            {
                open.Add((x+1, y));
                assignments[x+1,y] = true;
                size++;
            }
            if(y > 0 && !assignments[x,y-1] && heights[x,y-1] != 9)
            {
                open.Add((x, y-1));
                assignments[x,y-1] = true;
                size++;
            }
            if(y < gridWidth-1 && !assignments[x,y+1] && heights[x,y+1] != 9)
            {
                open.Add((x, y+1));
                assignments[x,y+1] = true;
                size++;
            }
        }

        return size;
    }
}