using System.Collections.Generic;

public struct Cube
{
    public long minX, maxX, minY, maxY, minZ, maxZ;

    public Cube(long minX, long maxX, long minY, long maxY, long minZ, long maxZ)
    {
        this.minX = minX;
        this.maxX = maxX;
        this.minY = minY;
        this.maxY = maxY;
        this.minZ = minZ;
        this.maxZ = maxZ;
    }

    public long Volume
    {
        get {
            if (maxX >= minX && maxY >= minY && maxZ >= minZ) 
            {
                return (maxX - minX + 1) * (maxY - minY + 1) * (maxZ - minZ + 1);
            }
            else
            {
                return 0;
            }
        }
    }

    public Cube Intersect(Cube other)
    {
        return new Cube(
            Math.Max(this.minX, other.minX),
            Math.Min(this.maxX, other.maxX),
            Math.Max(this.minY, other.minY),
            Math.Min(this.maxY, other.maxY),
            Math.Max(this.minZ, other.minZ),
            Math.Min(this.maxZ, other.maxZ)
        );
    }

    public List<Cube> Difference(Cube other)
    {
        // Subtract the "other" cube from this one, and return a collection of cubes.
        List<Cube> cubes = new List<Cube>();

        (long,long)[] xranges = new (long,long)[] {(this.minX, other.minX-1), (other.minX, other.maxX), (other.maxX+1, this.maxX)};
        (long,long)[] yranges = new (long,long)[] {(this.minY, other.minY-1), (other.minY, other.maxY), (other.maxY+1, this.maxY)}; 
        (long,long)[] zranges = new (long,long)[] {(this.minZ, other.minZ-1), (other.minZ, other.maxZ), (other.maxZ+1, this.maxZ)}; 

        foreach((long,long) xrange in xranges)
        {
            foreach((long,long) yrange in yranges)
            {
                foreach((long,long) zrange in zranges)
                {
                    Cube c = new Cube(xrange.Item1, xrange.Item2, yrange.Item1, yrange.Item2, zrange.Item1, zrange.Item2);
                    if(!c.Equals(other) && c.Volume > 0)
                    {
                        cubes.Add(c);
                    }
                }
            }
        }

        return cubes;
    }

    public override bool Equals(object? obj)
    {
        return obj is Cube cube &&
               minX == cube.minX &&
               maxX == cube.maxX &&
               minY == cube.minY &&
               maxY == cube.maxY &&
               minZ == cube.minZ &&
               maxZ == cube.maxZ;
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(minX, maxX, minY, maxY, minZ, maxZ);
    }
}