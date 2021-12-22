using System.Collections.Generic;
using System.Text.RegularExpressions;

public class ReactorReboot
{
    private static Regex lineRegex = new Regex(@"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$");
    private static Cube boundingCube = new Cube(-50, 50, -50, 50, -50, 50);

    public static void Main(string[] args)
    {
        string[] commandStrings = System.IO.File.ReadAllLines(args[0]);
        Command[] commands = commandStrings.Select(s => ParseCommand(s)).ToArray();

        long sumBounded = GetTotalOn(commands, true);
        Console.WriteLine($"Part 1: Total Bounded: {sumBounded}");

        long sumUnbounded = GetTotalOn(commands, false);
        Console.WriteLine($"Part 2: Total Unbounded: {sumUnbounded}");
    }

    private static Command ParseCommand(string line)
    {
        Match match = lineRegex.Matches(line)[0];
        GroupCollection groups = match.Groups;
        
        bool state = groups[1].Value.Equals("on");

        return new Command(state, new Cube(Int32.Parse(groups[2].Value), Int32.Parse(groups[3].Value), Int32.Parse(groups[4].Value), 
                                            Int32.Parse(groups[5].Value), Int32.Parse(groups[6].Value), Int32.Parse(groups[7].Value)));
    }

    private static long GetTotalOn(Command[] commands, bool bounded)
    {
        HashSet<Cube> onCubes = new HashSet<Cube>();

        foreach(Command command in commands)
        {
            HashSet<Cube> newCubes = new HashSet<Cube>();
            Cube newCube = bounded ? command.cube.Intersect(boundingCube) : command.cube;

            // Don't bother with 0 volume cubes (caused by bounding)
            if(newCube.Volume <= 0)
            {
                continue;
            }

            // Cut out this new region from all other cubes.
            // It will either be re-added at the end or will be left disabled.
            foreach(Cube oldCube in onCubes)
            {
                Cube intersection = oldCube.Intersect(newCube);
                if(intersection.Volume > 0)
                {
                    foreach(Cube c in oldCube.Difference(intersection))
                    {
                        newCubes.Add(c);
                    }
                } 
                else 
                {
                    // If they don't intersect, no need to split
                    newCubes.Add(oldCube);
                }
            }

            // If we were enabling this cube, do it now.
            if(command.state == true)
            {
                newCubes.Add(newCube);
            }

            // Prep for next iteration
            onCubes = newCubes;
        }

        // Return the sum of all cubes
        return onCubes.Sum(c => c.Volume);
    }
}

struct Command
{
    public bool state;
    public Cube cube;

    public Command(bool state, Cube cube)
    {
        this.state = state;
        this.cube = cube;
    }
}