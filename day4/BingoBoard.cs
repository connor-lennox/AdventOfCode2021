namespace Day4
{
    public class BingoBoard
    {
        private int[,] numbers;
        private bool[,] marked;

        public BingoBoard(int[,] nums)
        {
            numbers = nums;
            marked = new bool[5, 5];
        }

        public bool Mark(int num)
        {
            for(int i = 0; i < 5; i++)
            {
                for(int j = 0; j < 5; j++)
                {
                    if(numbers[i, j] == num)
                    {
                        marked[i, j] = true;
                        return CheckBingo(i, j);
                    }
                }
            }

            return false;
        }

        private bool CheckBingo(int i, int j)
        {
            bool found = true;
            for(int jx = 0; jx < 5; jx++)
            {
                if(!marked[i, jx])
                {
                    found = false;
                }
            }

            if(found == true) { return found; }

            found = true;

            for(int ix = 0; ix < 5; ix++)
            {
                if(!marked[ix, j])
                {
                    found = false;
                }
            }

            return found;
        }

        public int Score()
        {
            int sum = 0;
            for(int i = 0; i < 5; i++)
            {
                for(int j = 0; j < 5; j++)
                {
                    if(!marked[i, j])
                    {
                        sum += numbers[i, j];
                    }
                }
            }
            return sum;
        }

        public void Reset()
        {
            marked = new bool[5,5];
        }
    }
}