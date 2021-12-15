using System.Collections.Generic;


// Read in file
string[] lines = System.IO.File.ReadAllLines(args[0]);
int gridWidth = lines[0].Length;
int gridHeight = lines.Length;
int[,] risks = new int[gridHeight, gridWidth];
for(int i = 0; i < gridHeight; i++)
{
    for(int j = 0; j < gridWidth; j++)
    {
        risks[i,j] = Int32.Parse(lines[i][j].ToString());
    }
}


// Part 1: Find the minimum risk path from (0, 0) to (height, width)
// Just a regular A* implementation
int CalcH((int, int) coord, int height, int width)
{
    // Manhattan Distance Heuristic
    // return ((height - 1 - coord.Item1) + (width - 1 - coord.Item2));

    // For some reason this was not admissible. However, the following is:
    // It runs a little slower, but it's at least correct
    return 0;
}

AStarNode Expand(int[,] risks, AStarNode source, (int, int) d, int height, int width)
{
    (int, int) newCoord = (source.coordinate.Item1 + d.Item1, source.coordinate.Item2 + d.Item2);
    return new AStarNode(newCoord, source.g + risks[newCoord.Item1, newCoord.Item2], CalcH(newCoord, height, width));
}

// This is a pretty messy implementation due to having two different grids passed in with different sizes.
// In hindsight, I should have just put this in its own class and let it process that way
int DoAStar(int[,] risks, int height, int width)
{
    List<AStarNode> open = new List<AStarNode>();
    HashSet<(int, int)> closed = new HashSet<(int, int)>();

    AStarNode start = new AStarNode((0, 0), 0, CalcH((0, 0), height, width));
    open.Add(start);
    closed.Add(start.coordinate);
    while(open.Count > 0)
    {
        AStarNode cur = open[0];
        open.RemoveAt(0);

        if(cur.coordinate == (height-1, width-1))
        {
            return cur.g;
        }

        if(cur.coordinate.Item1 > 0)
        {
            AStarNode newNode = Expand(risks, cur, (-1, 0), height, width);
            if(!closed.Contains(newNode.coordinate))
            {
                open.Add(newNode);
                closed.Add(newNode.coordinate);
            }
        }
        if(cur.coordinate.Item2 > 0)
        {
            AStarNode newNode = Expand(risks, cur, (0, -1), height, width);
            if(!closed.Contains(newNode.coordinate))
            {
                open.Add(newNode);
                closed.Add(newNode.coordinate);
            }
        }
        if(cur.coordinate.Item1 < height-1)
        {
            AStarNode newNode = Expand(risks, cur, (1, 0), height, width);
            if(!closed.Contains(newNode.coordinate))
            {
                open.Add(newNode);
                closed.Add(newNode.coordinate);
            }
        }
        if(cur.coordinate.Item2 < width-1)
        {
            AStarNode newNode = Expand(risks, cur, (0, 1), height, width);
            if(!closed.Contains(newNode.coordinate))
            {
                open.Add(newNode);
                closed.Add(newNode.coordinate);
            }
        }

        open.Sort();
    }

    return -1;
}

Console.WriteLine($"Part 1: Corner-to-Corner Risk: {DoAStar(risks, gridHeight, gridWidth)}");

// Part 2: Expanded grid
int[,] p2Risk = new int[gridHeight*5, gridWidth*5];
for(int i = 0; i < gridHeight*5; i++)
{
    for(int j = 0; j < gridWidth*5; j++)
    {
        p2Risk[i,j] = Int32.Parse(lines[i%gridHeight][j%gridWidth].ToString()) + ((i / gridHeight) + (j / gridWidth));
        if(p2Risk[i,j] >= 10)
        {
            p2Risk[i,j] = p2Risk[i,j] % 10 + 1;
        }
    }
}

Console.WriteLine($"Part 2: Corner-to-Corner Risk: {DoAStar(p2Risk, gridHeight*5, gridWidth*5)}");