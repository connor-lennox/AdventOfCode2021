using System.Linq;
using System.Collections.Generic;

public class Parser
{
    public static void Main(string[] args)
    {
        // Read input and convert to a binary string
        string[] input = System.IO.File.ReadAllLines(args[0]);
        foreach(string i in input)
        {
            string binInput = String.Join(String.Empty,
                i.Select(c => Convert.ToString(Convert.ToInt32(c.ToString(), 16), 2).PadLeft(4, '0'))
            );

            int idx = 0;
            Packet root = ParsePacket(binInput, ref idx);

            Console.WriteLine($"Part 1: Version Sum = {root.VersionSum()}");
            Console.WriteLine($"Part 2: Root Value = {root.Value()}");
        }
    }

    public static Packet ParsePacket(string input, ref int idx)
    {
        int typeId = GetValue(input, idx+3, 3);

        if(typeId == 4)
        {
            return ParseLiteral(input, ref idx);
        } else {
            return ParseOperator(input, ref idx);
        }
    }

    public static Operator ParseOperator(string input, ref int idx)
    {
        // Read info from operator header
        int version = GetValue(input, idx, 3);
        int typeId = GetValue(input, idx+3, 3);
        int lengthType = GetValue(input, idx+6, 1);
        idx += 7;

        // Two different subpacket modes: num bits or num packets
        int subpacketLength;
        List<Packet> subpackets = new List<Packet>();
        if(lengthType == 0)
        {
            // Read a fixed number of bits worth of packets
            subpacketLength = GetValue(input, idx, 15);
            idx += 15;
            int targetIdx = idx + subpacketLength;
            while(idx < targetIdx)
            {
                subpackets.Add(ParsePacket(input, ref idx));
            }
        } else {
            // Read a fixed number of packets
            subpacketLength = GetValue(input, idx, 11);
            idx += 11;
            for(int i = 0; i < subpacketLength; i++)
            {
                subpackets.Add(ParsePacket(input, ref idx));
            }
        }

        return new Operator(version, typeId, lengthType, subpacketLength, subpackets);
    }

    public static Literal ParseLiteral(string input, ref int idx)
    {
        // Read version, skip typeId (always 4)
        int version = GetValue(input, idx, 3);
        idx += 6;

        // Parse literal subpackets
        uint r;
        long value = 0;
        do
        {
            value <<= 4;
            r = (uint)GetValue(input, idx, 5);
            value |= (r & 0b1111);
            idx += 5;
        } while ((r & 0b10000) != 0);

        return new Literal(version, value);
    }

    private static int GetValue(string input, int idx, int length)
    {
        return Convert.ToInt32(input.Substring(idx, length), 2);
    }
}