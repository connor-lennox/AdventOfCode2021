public class AStarNode : IComparable<AStarNode>
{
    public (int, int) coordinate;
    public int g;
    public int h;

    public AStarNode((int, int) coordinate, int g, int h)
    {
        this.coordinate = coordinate;
        this.g = g;
        this.h = h;
    }

    public int CompareTo(AStarNode? other)
    {
        if(other == null) return 1;
        return f().CompareTo(other.f());
    }

    public override bool Equals(object? obj)
    {
        return obj is AStarNode node &&
               coordinate.Equals(node.coordinate) &&
               g == node.g &&
               h == node.h;
    }

    public int f()
    {
        return g + h;
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(coordinate, g, h);
    }


}