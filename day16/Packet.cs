using System.Collections.Generic;

public abstract class Packet 
{
    public int version;
    public int typeId;
    public Packet(int version, int typeId)
    {
        this.version = version;
        this.typeId = typeId;
    }

    public abstract int VersionSum();
    public abstract long Value();
}

public class Literal : Packet
{
    public long value;
    public Literal(int version, long value) : base(version, 4)
    {
        this.value = value;
    }

    public override int VersionSum() => version;
    public override long Value() => value;
}

public class Operator : Packet
{
    public int lengthType;
    public int subpacketLength;
    public List<Packet> subpackets;
    public Operator(int version, int typeId, int lengthType, int subpacketLength, List<Packet> subpackets) : base(version, typeId)
    {
        this.lengthType = lengthType;
        this.subpacketLength = subpacketLength;
        this.subpackets = subpackets;
    }

    public override int VersionSum()
    {
        int s = version;
        foreach(Packet child in subpackets)
        {
            s += child.VersionSum();
        }
        return s;
    }

    public override long Value()
    {
        long value = 0;
        switch(typeId)
        {
            case 0: 
                value = 0;
                foreach(Packet child in subpackets)
                {
                    value += child.Value();
                }
                break;
            case 1:
                value = 1;
                foreach(Packet child in subpackets)
                {
                    value *= child.Value();
                }
                break;
            case 2:
                value = long.MaxValue;
                foreach(Packet child in subpackets)
                {
                    value = Math.Min(value, child.Value());
                }
                break;
            case 3:
                value = long.MinValue;
                foreach(Packet child in subpackets)
                {
                    value = Math.Max(value, child.Value());
                }
                break;
            case 5:
                value = subpackets[0].Value() > subpackets[1].Value() ? 1 : 0;
                break;
            case 6:
                value = subpackets[0].Value() < subpackets[1].Value() ? 1 : 0;
                break;
            case 7:
                value = subpackets[0].Value() == subpackets[1].Value() ? 1 : 0;
                break;
        }
        
        return value;
    }
}